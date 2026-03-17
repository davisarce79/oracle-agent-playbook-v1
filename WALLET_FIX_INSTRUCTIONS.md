# How to Fix the $GUNNA Wallet Address

## Problem
The current deployment wallet address `dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW` is **invalid**:
- Length: 49 characters (should be exactly 44)
- Solana RPC rejects it: `Invalid param: WrongSize`
- Result: token deployment will fail; wallet monitor cannot check balance

## Solution
1. **Get your correct Solana wallet pubkey**
   - If you already have a Solana wallet, open it and copy the **public key** (also called "address" or "pubkey"). It must be exactly 44 base58 characters.
   - If you need to create a new wallet: use Phantom, Solflare, or any Solana wallet. Create a new wallet, then copy the **public key**.
   - **Do not** use a private key or secret key here — only the public address.

2. **Run the fix script**
   ```bash
   python3 fix_gunna_wallet.py <YOUR_CORRECT_PUBKEY> --apply
   ```
   Example:
   ```bash
   python3 fix_gunna_wallet.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU --apply
   ```

   This will update the wallet address in:
   - `deploy_gunna_token.py`
   - `monitor_gunna_wallet.py`
   - `COMMITMENTS.md`
   - `REVENUE_TRACK_STATUS.md`

3. **Verify the fix**
   ```bash
   grep WALLET_PUBKEY deploy_gunna_token.py
   ```
   Should show the new 44-char address.

4. **Fund the wallet**
   - Buy ~0.05–0.1 SOL on an exchange (Coinbase, Binance, etc.)
   - Withdraw to your wallet address (the same pubkey you just set)
   - Wait for confirmation (~1–2 minutes)

5. **Deploy the token**
   - Option A: Run `python3 deploy_gunna_token.py` (if Solana CLI installed)
   - Option B: Go to pump.fun, connect your wallet, and create token manually using the prepared metadata (symbol GUNNA, supply 1B, logo at `memory/uploads/gunna_token_logo_clean.png`)

6. **Monitor balance**
   The wallet monitor cron (`monitor_gunna_wallet.py`) will now work and alert when balance ≥ 0.05 SOL.

## Notes
- Keep your private key secure. Never share it.
- The fix script saves a log entry to `memory/wallet_address_fix_log.txt`.
- After deployment, update `REVENUE_TRACK_STATUS.md` to reflect success.

---

**Created:** 2026-03-17  
**Owner:** Agent Gunna
