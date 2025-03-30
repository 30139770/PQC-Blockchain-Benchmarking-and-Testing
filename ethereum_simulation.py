from web3 import Web3
from eth_account import Account
import time

# Ethereum (secp256k1 ECDSA) Address Generation
def generate_eth_address():
    # Generate random Ethereum account
    acct = Account.create()

    print(f"\n[Ethereum Address Generation (ECDSA-secp256k1)]")
    print(f"Public Address: {acct.address}")
    print(f"Private Key: {acct.key.hex()}\n")

    return acct

# Ethereum Transaction Signing
def sign_eth_transaction(acct, tx_data):
    tx_hash = Web3.keccak(text=tx_data)

    start_time = time.perf_counter_ns()
    signed_message = Account._sign_hash(tx_hash, acct.key)
    end_time = time.perf_counter_ns()

    elapsed_ms = (end_time - start_time) / 1_000_000  # ns to ms

    print(f"[Ethereum Transaction Signing (ECDSA-secp256k1)]")
    print(f"Transaction Data: '{tx_data}'")
    print(f"Transaction Hash (Keccak-256): {tx_hash.hex()}")
    print(f"Signature size: {len(signed_message.signature)} bytes")
    print(f"Signing Time: {elapsed_ms:.4f} ms\n")

    return signed_message, tx_hash


# Ethereum Transaction Verification
def verify_eth_transaction(signed_message, tx_hash, expected_address):
    start_time = time.perf_counter_ns()
    recovered_address = Account._recover_hash(tx_hash, signature=signed_message.signature)
    end_time = time.perf_counter_ns()

    elapsed_ms = (end_time - start_time) / 1_000_000  # ns to ms
    valid = recovered_address.lower() == expected_address.lower()

    print(f"[Ethereum Transaction Verification (ECDSA-secp256k1)]")
    print(f"Recovered Address: {recovered_address}")
    print(f"Expected Address: {expected_address}")
    print(f"Verification Time: {elapsed_ms:.4f} ms")
    print(f"Signature Valid: {valid}\n")

    return valid

def main():
    print("\n--- Ethereum Standard Simulation (ECDSA-secp256k1 via web3) ---")

    # Generate Ethereum Address
    acct = generate_eth_address()

    # Sign a transaction
    tx_data = "transfer(10000000000000000000, 0x8461278E68e6200034babEFc1f17787fDeeB5198)"
    signed_message, tx_hash = sign_eth_transaction(acct, tx_data)

    # Verify the Ethereum transaction
    verify_eth_transaction(signed_message, tx_hash, acct.address)

if __name__ == "__main__":
    main()
