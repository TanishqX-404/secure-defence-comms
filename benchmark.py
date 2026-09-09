import os
import time
from web3 import Web3

# ==========================================
# 1. CONFIGURATION
# ==========================================
RPC_URL = os.getenv("BENCHMARK_RPC_URL", "http://127.0.0.1:8545")
# This key belongs to the disposable local test network only.
PRIVATE_KEY = os.getenv(
    "BENCHMARK_PRIVATE_KEY",
    "0xcd0df6fa5d0bd9f0e4240b024878d1612a7900bc19c09f8989a3e57e44986a9a",
)

# Connect
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- THE FIX: Handle Web3 v6 vs v7 Middleware ---
try:
    # Try v6 import
    from web3.middleware import geth_poa_middleware
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print("Loaded Middleware (v6 Style)")
except ImportError:
    # Try v7 import (New Name)
    try:
        from web3.middleware import ExtraDataToPOAMiddleware
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        print("Loaded Middleware (v7 Style)")
    except Exception as e:
        print(f"Middleware warning: {e}")

def run_benchmark():
    print("\n--- STARTING RESEARCH BENCHMARK ---")
    
    if not w3.is_connected():
        print("CRITICAL: Cannot connect to Node. Is Docker running?")
        return

    node_chain_id = w3.eth.chain_id
    print(f"Connected. Chain ID: {node_chain_id}")
    
    account = w3.eth.account.from_key(PRIVATE_KEY)
    
    # 1. Check Balance
    try:
        balance = w3.eth.get_balance(account.address)
        print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")
    except Exception as e:
        print(" Wallet Error. Genesis reset required.")
        return

    # 2. LOAD TEST (10 Txs for Sample)
    print("\n STARTING LOAD TEST...")
    
    nonce = w3.eth.get_transaction_count(account.address)
    latencies = []
    
    for i in range(10):
        loop_start = time.time()
        
        tx = {
            'to': account.address,
            'value': 0,
            'gas': 21000,
            'gasPrice': 0,
            'nonce': nonce,
            'chainId': node_chain_id
        }
        
        try:
            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            
            latency = (time.time() - loop_start) * 1000
            latencies.append(latency)
            
            print(f"   Tx #{i+1}: {latency:.2f} ms")
            nonce += 1
        except Exception as e:
            print(f"   Tx Failed: {e}")
            break

    # 4. RESULTS
    if latencies:
        print("\n=== FINAL RESULTS ===")
        print(f"Average Latency: {sum(latencies)/len(latencies):.2f} ms")
        print("SUCCESS")

if __name__ == "__main__":
    run_benchmark()
