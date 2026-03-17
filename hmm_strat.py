import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import os
import json
import sys
from pathlib import Path

# Import centralized trade executor
WORKSPACE = Path('/home/opc/.openclaw/workspace')
sys.path.insert(0, str(WORKSPACE))
from trade_executor import TradeExecutor

class HMMTradingEngine:
    """
    AGENT INSTRUCTION: Use this class to manage the Baum-Welch lifecycle:
    1. Train models on Daily and Intraday data.
    2. Detect Regimes (Bull/Bear/Sideways).
    3. Apply Volatility Filters and Risk Management.
    4. Execute via Alpaca using TradeExecutor (safe, validated orders).
    """
    def __init__(self, api_key=None, secret_key=None, base_url='https://paper-api.alpaca.markets'):
        # TradeExecutor handles credential loading internally if keys not provided
        self.executor = TradeExecutor(dry_run=False)
        self.api = self.executor.api  # for data fetching
        self.model = None
        self.state_file = 'hmm_convergence_state.json'

    def _get_failure_count(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f).get('failures', 0)
        return 0

    def _update_failure_count(self, count):
        with open(self.state_file, 'w') as f:
            json.dump({'failures': count}, f)

    def prepare_data(self, df):
        """Standardizes features for Baum-Welch ingestion."""
        df.columns = [c.lower() for c in df.columns]
        df['returns'] = np.log(df['close'] / df['close'].shift(1))
        df['range'] = (df['high'] - df['low']) / df['close']
        df.dropna(inplace=True)
        return df[['returns', 'range']].values, df

    def train_baum_welch(self, data, n_states=3):
        """Runs the EM algorithm to find hidden market regimes."""
        failures = self._get_failure_count()
        if failures >= 3:
            print("ALERT: HMM Halt. Multiple convergence failures detected.")
            return None

        model = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000)
        model.fit(data)
        
        if not model.monitor_.converged:
            failures += 1
            self._update_failure_count(failures)
            print(f"LOG: Baum-Welch did not converge (Failure {failures}/3).")
            if failures >= 3:
                print(">>> CRITICAL: HMM HALTED. Notify Boss immediately.")
            return model
        
        # Reset failures on success
        self._update_failure_count(0)
        return model

    def get_regime_labels(self, model, data):
        """Identifies which state is 'Bull' based on highest mean return."""
        if model is None: return None, None, None, 0
        state_means = model.means_[:, 0]
        bull_state = np.argmax(state_means)
        bear_state = np.argmin(state_means)
        current_state = model.predict(data)[-1]
        confidence = model.predict_proba(data)[-1].max()
        return current_state, bull_state, bear_state, confidence

    def volatility_filter(self, df, percentile=90):
        """Returns True if market is calm enough to trade."""
        recent_vol = df['returns'].rolling(20).std().iloc[-1]
        threshold = df['returns'].rolling(20).std().quantile(percentile/100)
        return recent_vol < threshold

    def execute_logic(self, symbol, qty):
        """The Master Multi-Timeframe Execution Loop."""
        if self._get_failure_count() >= 3:
            return

        # 1. Get Data
        daily_bars = self.api.get_bars(symbol, '1Day', limit=100).df
        intraday_bars = self.api.get_bars(symbol, '5Min', limit=100).df
        
        if daily_bars.empty or intraday_bars.empty:
            return

        # 2. Process Daily (The Anchor)
        d_obs, d_df = self.prepare_data(daily_bars)
        d_model = self.train_baum_welch(d_obs)
        if d_model is None: return
        d_state, d_bull, _, _ = self.get_regime_labels(d_model, d_obs)

        # 3. Process Intraday (The Signal)
        i_obs, i_df = self.prepare_data(intraday_bars)
        i_model = self.train_baum_welch(i_obs)
        if i_model is None: return
        i_state, i_bull, _, i_conf = self.get_regime_labels(i_model, i_obs)

        # 4. Check Safety Filters
        is_safe = self.volatility_filter(i_df)

        # 5. Trading Decision
        if d_state == d_bull and i_state == i_bull and i_conf > 0.75 and is_safe:
            self.place_order(symbol, qty, 'buy')
        else:
            self.place_order(symbol, qty, 'sell')

    def place_order(self, symbol, qty, side):
        """Manages orders via TradeExecutor with safety checks."""
        try:
            pos = self.executor.get_position(symbol)
            if side == 'buy' and pos and int(pos['qty']) > 0:
                return
            if side == 'sell' and (not pos or int(pos['qty']) == 0):
                return
        except Exception:
            if side == 'sell':
                return

        result = self.executor.place_order(symbol, qty, side, order_type='market', time_in_force='day')
        if result['success']:
            print(f"ORDER SENT: {side} {qty} {symbol} (id {result['order_id']})")
        else:
            print(f"ORDER FAILED: {side} {qty} {symbol} — {result['message']}")
