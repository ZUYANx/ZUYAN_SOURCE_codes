#!/usr/bin/env python3
"""
Lightweight TRC20 Wallet CLI for Termux
Uses only built-in Python modules + TronGrid API
Optimized for low RAM/storage devices
"""

import os
import json
import hashlib
import secrets
import urllib.request
import urllib.parse
from typing import Dict, Optional

class TronWallet:
    def __init__(self):
        self.wallet_file = "wallet.json"
        self.api_url = "https://api.trongrid.io"
        self.usdt_contract = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    
    def create_wallet(self):
        """Generate new TRON wallet (simplified)"""
        # Generate 64-character hex private key
        private_key = secrets.token_hex(32)
        
        # Simple address generation (for demo - real implementation needs secp256k1)
        # This is a placeholder - in production you'd need proper key derivation
        temp_hash = hashlib.sha256(private_key.encode()).hexdigest()
        address = "T" + temp_hash[:33]  # Simplified address format
        
        wallet_data = {
            "private_key": private_key,
            "address": address
        }
        
        # Save wallet
        with open(self.wallet_file, 'w') as f:
            json.dump(wallet_data, f)
        
        print(f"✅ Wallet Created!")
        print(f"Address: {address}")
        print(f"Private Key: {private_key}")
        print(f"⚠️  Save your private key securely!")
        return private_key, address
    
    def load_wallet(self):
        """Load existing wallet"""
        try:
            with open(self.wallet_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def api_request(self, endpoint, data=None, method="GET"):
        """Simple API request handler"""
        url = f"{self.api_url}/{endpoint}"
        
        try:
            if method == "POST":
                req_data = json.dumps(data).encode() if data else None
                headers = {'Content-Type': 'application/json'}
                req = urllib.request.Request(url, req_data, headers)
            else:
                if data:
                    url += "?" + urllib.parse.urlencode(data)
                req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"❌ API Error: {e}")
            return None
    
    def check_balance(self):
        """Check TRX and USDT balance"""
        wallet = self.load_wallet()
        if not wallet:
            print("❌ No wallet found. Create one first.")
            return
        
        address = wallet["address"]
        print(f"📍 Address: {address}")
        print("🔍 Checking balances...")
        
        # Get TRX balance
        trx_data = self.api_request(f"v1/accounts/{address}")
        if trx_data and trx_data.get("success"):
            balance = trx_data.get("data", [{}])[0].get("balance", 0)
            trx_balance = balance / 1_000_000  # Convert from sun to TRX
            print(f"💎 TRX Balance: {trx_balance:.6f} TRX")
        else:
            print("💎 TRX Balance: 0.000000 TRX")
        
        # Get USDT balance (TRC20)
        usdt_data = self.api_request("v1/accounts/{}/tokens".format(address))
        usdt_balance = 0
        if usdt_data and usdt_data.get("success"):
            tokens = usdt_data.get("data", [])
            for token in tokens:
                if token.get("tokenId") == self.usdt_contract:
                    usdt_balance = float(token.get("balance", 0)) / 1_000_000
                    break
        
        print(f"💵 USDT Balance: {usdt_balance:.6f} USDT")
    
    def send_trx(self):
        """Send TRX transaction"""
        wallet = self.load_wallet()
        if not wallet:
            print("❌ No wallet found. Create one first.")
            return
        
        try:
            to_address = input("📤 To Address: ").strip()
            amount = float(input("💰 Amount (TRX): "))
            
            if amount <= 0:
                print("❌ Amount must be positive")
                return
            
            # Convert TRX to sun
            amount_sun = int(amount * 1_000_000)
            
            # Create transaction data
            tx_data = {
                "to_address": to_address,
                "owner_address": wallet["address"],
                "amount": amount_sun
            }
            
            # Create transaction
            result = self.api_request("wallet/createtransaction", tx_data, "POST")
            if result:
                print("✅ Transaction prepared (Note: Signing not implemented in demo)")
                print(f"📋 TX Data: {json.dumps(result, indent=2)}")
            else:
                print("❌ Failed to create transaction")
                
        except ValueError:
            print("❌ Invalid amount")
        except KeyboardInterrupt:
            print("\n❌ Cancelled")
    
    def send_trc20(self):
        """Send TRC20 tokens (USDT)"""
        wallet = self.load_wallet()
        if not wallet:
            print("❌ No wallet found. Create one first.")
            return
        
        try:
            to_address = input("📤 To Address: ").strip()
            amount = float(input("💰 Amount (USDT): "))
            
            if amount <= 0:
                print("❌ Amount must be positive")
                return
            
            # Convert to smallest unit
            amount_unit = int(amount * 1_000_000)
            
            # TRC20 transfer function signature
            function_selector = "a9059cbb"  # transfer(address,uint256)
            
            # Encode parameters (simplified)
            to_hex = to_address[1:].encode().hex().zfill(64)  # Remove T prefix, pad to 64 chars
            amount_hex = hex(amount_unit)[2:].zfill(64)
            
            parameter = function_selector + to_hex + amount_hex
            
            tx_data = {
                "contract_address": self.usdt_contract,
                "function_selector": function_selector,
                "parameter": parameter,
                "owner_address": wallet["address"],
                "call_value": 0
            }
            
            result = self.api_request("wallet/triggersmartcontract", tx_data, "POST")
            if result:
                print("✅ TRC20 transaction prepared (Note: Signing not implemented in demo)")
                print(f"📋 TX Data: {json.dumps(result, indent=2)}")
            else:
                print("❌ Failed to create TRC20 transaction")
                
        except ValueError:
            print("❌ Invalid amount")
        except KeyboardInterrupt:
            print("\n❌ Cancelled")

def print_banner():
    """Print CLI banner"""
    print("=" * 50)
    print("🚀 TRC20 Wallet CLI for Termux")
    print("💾 Lightweight • 🔥 Fast • 🔐 Secure")
    print("=" * 50)

def print_menu():
    """Print command menu"""
    print("\n📋 Commands:")
    print("1️⃣  create_wallet  - Generate new wallet")
    print("2️⃣  check_balance  - Check TRX + USDT balance") 
    print("3️⃣  send_trx       - Send TRX")
    print("4️⃣  send_trc20     - Send USDT (TRC20)")
    print("5️⃣  exit           - Quit CLI")
    print("-" * 40)

def main():
    """Main CLI loop"""
    wallet = TronWallet()
    print_banner()
    
    # Check if wallet exists
    existing_wallet = wallet.load_wallet()
    if existing_wallet:
        print(f"👛 Wallet loaded: {existing_wallet['address'][:10]}...")
    else:
        print("💡 No wallet found. Use 'create_wallet' to start.")
    
    while True:
        print_menu()
        try:
            command = input("🎯 Enter command: ").strip().lower()
            
            if command in ['1', 'create_wallet']:
                wallet.create_wallet()
            
            elif command in ['2', 'check_balance']:
                wallet.check_balance()
            
            elif command in ['3', 'send_trx']:
                wallet.send_trx()
            
            elif command in ['4', 'send_trc20']:
                wallet.send_trc20()
            
            elif command in ['5', 'exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid command. Try again.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()