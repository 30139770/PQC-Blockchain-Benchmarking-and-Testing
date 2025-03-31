import oqs
import hashlib
import time

# Dilithium2
SIG_ALG = 'Dilithium2'

# Address Generation
def generate_address():
    with oqs.Signature(SIG_ALG) as signer:
        public_key = signer.generate_keypair()
        private_key = signer.export_secret_key()

    # Simulate blockchain address by hashing public key
    address = '0x' + hashlib.sha256(public_key).digest()[-20:].hex()

    print(f"\n[Address Generation]")
    print(f"Public Key size: {len(public_key)} bytes")
    print(f"Private Key size: {len(private_key)} bytes")
    print(f"Blockchain Address: {address}\n")

    return public_key, private_key, address

# Transaction Signing
def sign_transaction(private_key, transaction_message):
    with oqs.Signature(SIG_ALG, secret_key=private_key) as signer:
        tx_hash = hashlib.sha256(transaction_message.encode()).digest()

        start_time = time.perf_counter_ns()
        signature = signer.sign(tx_hash)
        end_time = time.perf_counter_ns()

    elapsed_ms = (end_time - start_time) / 1_000_000  # ns to ms

    print(f"[Transaction Signing]")
    print(f"Transaction Message: '{transaction_message}'")
    print(f"Transaction Hash: {tx_hash.hex()}")
    print(f"Signature size: {len(signature)} bytes")
    print(f"Time taken to sign: {elapsed_ms:.4f} ms\n")

    return signature, tx_hash

# Transaction Verification
def verify_transaction(public_key, signature, tx_hash):
    with oqs.Signature(SIG_ALG) as verifier:
        start_time = time.perf_counter_ns()
        valid = verifier.verify(tx_hash, signature, public_key)
        end_time = time.perf_counter_ns()

    elapsed_ms = (end_time - start_time) / 1_000_000  # ns to ms

    print(f"[Transaction Verification]")
    print(f"Time taken to verify: {elapsed_ms:.4f} ms")
    print(f"Signature Valid: {valid}\n")

    return valid

def main():
    print("\n--- PQC Blockchain Simulation (Dilithium2 via liboqs) ---")

    # Address Generation
    public_key, private_key, address = generate_address()

    # Sign a simulated transaction
    transaction_message = "transfer(10000000000000000000, 0x8461278E68e6200034babEFc1f17787fDeeB5198)"
    signature, tx_hash = sign_transaction(private_key, transaction_message)

    # Verify the transaction
    verify_transaction(public_key, signature, tx_hash)

if __name__ == "__main__":
    main()
