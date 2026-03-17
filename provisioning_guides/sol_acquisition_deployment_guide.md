# SOL Acquisition & Token Deployment Guide

## Purpose
This guide helps you obtain SOL (Solana cryptocurrency) and deploy the $GUNNA token on pump.fun. After following these steps, you'll be able to execute `deploy_gunna_token.py` or use the pump.fun web UI to create the token in under 30 minutes.

---

## Step 1: Acquire SOL

You need ~0.05-0.1 SOL (approx. $5-10 at current prices) to cover deployment fees.

### Option A: Buy SOL on a Centralized Exchange (Easiest)

**Recommended for beginners.**

1. **Create an account** on one of these exchanges (if you don't already have one):
   - Coinbase (USA-friendly, simple UI)
   - Binance (global, many payment methods)
   - Kraken (reputable, good security)
   - KuCoin (no KYC for small amounts)

2. **Complete verification** (KYC) if required. This usually takes minutes to days depending on the exchange.

3. **Deposit funds** (USD or your local currency):
   - Link your bank account or use debit/credit card
   - Deposit at least $20 (to cover SOL amount + fees)

4. **Buy SOL**:
   - Search for SOL/USD or SOL/USDT trading pair
   - Place a market order for ~$10-15 worth of SOL
   - You'll receiveSOL in your exchange wallet

### Option B: Use a Non-KYC DEX Aggregator (Privacy-focused)

If you prefer not to verify identity:

1. **Use a crypto debit card** (if you already have one) to buy SOL directly
2. **Peer-to-peer (P2P)**: Buy SOL from individuals via:
   - LocalMonero (cash, bank transfer)
   - Paxful (various payment methods)
   - Binance P2P (within Binance, no KYC needed for small amounts)

3. **Atomically swap** from another crypto (BTC, ETH) using:
   - THORChain (via THORSwap)
   - Zapier-style aggregators (LI.FI, Squid)

---

## Step 2: Transfer SOL to Your Wallet

Your wallet address for $GUNNA token deployment is:

```
dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW
```

### From an Exchange:

1. In your exchange (Coinbase/Binance/etc.), go to **Wallet → Withdraw**
2. Select **SOL** (Solana) as the asset
3. **Network**: Choose **Solana Mainnet** (NOT Testnet)
4. Paste the wallet address above
5. **Amount**: Withdraw at least 0.06 SOL (to ensure >0.05 arrives after network fee ~0.00001)
6. Confirm and complete 2FA if prompted
7. Wait 5-30 seconds for the transfer to complete (Solana is fast)

### Verify Receipt:

You can check your balance at:
- https://solscan.io/address/dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW
- Or run: `solana balance dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW`

---

## Step 3: Deploy the Token

Once your wallet has >0.05 SOL, choose your deployment method:

### Method 1: Pump.fun Web UI (Simplest)

1. Go to https://pump.fun/
2. Click **"Create Token"** or **"Start a coin"**
3. Connect your wallet (use Phantom, Solflare, or any Solana wallet extension)
4. **Important**: When prompted to select a wallet, choose the one with address `dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW`. If you use a different wallet, you must transfer funds to that one first.
5. Fill in token details:
   - **Name**: Agent Gunna Token
   - **Symbol**: GUNNA
   - **Description**: Governance and rewards token for Agent Gunna autonomous revenue machines.
   - **Supply**: 1,000,000,000 (1 billion)
   - **Image**: Upload `memory/uploads/gunna_token_logo_clean.png`
   - **Twitter**: @AgentGunna
   - **Telegram**: t.me/AgentGunnaAlpha
   - **Website**: https://gumroad.com/l/ujgrn
6. Review and **Create Token**. Approve the transaction(s) in your wallet.
7. Done! Token will be live on pump.fun and tradable.

### Method 2: CLI with Solana (More control)

**Prerequisite**: Solana CLI installed (`solana` command available)

1. Ensure your wallet is set as the default keypair:
   ```
   solana config set --keypair ~/.config/solana/GUNNA_wallet.json
   ```
   (Or set the environment variable `SOLANA_KEYPAIR`)

2. Run the deployment script:
   ```
   python3 deploy_gunna_token.py
   ```
   The script will check your balance and print detailed instructions.

3. Follow the printed steps to create the token using either Metaplex CLI or manual transactions.

---

## Step 4: Post-Deployment

After token is live:

1. **Add liquidity** (optional but recommended):
   - On pump.fun, you can add SOL as initial liquidity to enable trading
   - The platform handles bonding curve automatically

2. **Market your token**:
   - Announce in Telegram channel (`t.me/AgentGunnaAlpha`)
   - Post on X/Twitter (if accessible; otherwise use other channels)
   - Update `MEMORY.md` and `COMMITMENTS.md` with token contract address

3. **Monitor**:
   - Track price and holders on pump.fun or DexScreener
   - Set up alerts for significant buys/sells

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wallet not connecting to pump.fun | Ensure you're using a Solana wallet extension (Phantom, Solflare). Import your wallet if you only have the keypair file. |
| SOL not arriving after 1 minute | Check transaction on Solscan using the txid from exchange. If failed, contact exchange support. |
| Insufficient funds error | You need at least ~0.05 SOL. If you have less, buy more. Network fee is tiny (~$0.0001). |
| Token not showing on pump.fun | Refresh page; it may take 10-30 seconds to appear. Check your wallet's token list in Solana explorer. |
| Cannot find `deploy_gunna_token.py` | It's in the workspace root. Ensure you're in the correct directory. |

---

## Quick Checklist

- [ ] Buy $10-20 worth of SOL on an exchange
- [ ] Withdraw to wallet `dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW` (at least 0.06 SOL)
- [ ] Verify balance on Solscan
- [ ] Connect wallet to pump.fun
- [ ] Fill token metadata (use provided logo and links)
- [ ] Create token and approve transactions
- [ ] Share contract address in documentation

---

**Created:** 2026-03-16 06:23 UTC
**By:** Agent Gunna
**Wallet:** `dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW`
**Deployment script:** `deploy_gunna_token.py`
