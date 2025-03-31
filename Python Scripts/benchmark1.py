import time
import hashlib
import statistics
import csv
import os
from datetime import datetime
import random

# ECC
from ecdsa import SigningKey, SECP256k1

# SHA-256 & RSA
from Crypto.PublicKey import RSA 
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256 as RSA_SHA256

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "Benchmark_Results")
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

def generate_random_data(size):
    return bytes([random.randint(0, 255) for _ in range(size)])

def benchmark_sha256(iterations=10000, data_size=128):
    print("Benchmarking SHA-256 with 10,000 iterations of random data...")
    times_ns = []
    result_data = []
    for _ in range(iterations):
        data = generate_random_data(data_size)
        start = time.perf_counter_ns()
        hashed_data = hashlib.sha256(data).digest()
        result_data.append(hashed_data.hex())
        end = time.perf_counter_ns()
        times_ns.append(end - start)

    times_ms = [t / 1_000_000 for t in times_ns]
    return [{
        "algorithm": "SHA-256",
        "operation": "Hash",
        "iterations": iterations,
        "average_ms": statistics.mean(times_ms),
        "min_ms": min(times_ms),
        "max_ms": max(times_ms),
        "stdev_ms": statistics.pstdev(times_ms),
        "raw_times_ms": times_ms,
        "data": result_data
    }]

def benchmark_ecc(iterations=5000):
    print("Benchmarking ECC with 10,000 iterations of random data...")
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    message = os.urandom(32) # Generate random 32 bytes of data for the ECC test
    sign_times_ns = []
    sign_result_data = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        signature = sk.sign(message)
        sign_result_data.append(signature.hex())
        end = time.perf_counter_ns()
        sign_times_ns.append(end - start)
    
    sign_times_ms = [t / 1_000_000 for t in sign_times_ns]
    sign_results = {
        "algorithm": "ECC (Secp256k1)",
        "operation": "Sign",
        "iterations": iterations,
        "average_ms": statistics.mean(sign_times_ms),
        "min_ms": min(sign_times_ms),
        "max_ms": max(sign_times_ms),
        "stdev_ms": statistics.pstdev(sign_times_ms),
        "raw_times_ms": sign_times_ms,
        "data": sign_result_data
    }

    signature = sk.sign(message)
    verify_times_ns = []
    verify_result_data = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        vk.verify(signature, message)
        verify_result_data.append(signature.hex())
        end = time.perf_counter_ns()
        verify_times_ns.append(end - start)
    
    verify_times_ms = [t / 1_000_000 for t in verify_times_ns]
    verify_results = {
        "algorithm": "ECC (Secp256k1)",
        "operation": "Verify",
        "iterations": iterations,
        "average_ms": statistics.mean(verify_times_ms),
        "min_ms": min(verify_times_ms),
        "max_ms": max(verify_times_ms),
        "stdev_ms": statistics.pstdev(verify_times_ms),
        "raw_times_ms": verify_times_ms,
        "data": verify_result_data
    }

    return [sign_results, verify_results]

def benchmark_rsa(iterations=1000, key_size=2048):
    print("Benchmarking RSA-2048 with 10,000 iterations of random data...")
    key = RSA.generate(key_size)
    pub_key = key.publickey()
    signer = pkcs1_15.new(key)
    verifier = pkcs1_15.new(pub_key)
    
    sign_times_ns = []
    sign_result_data = []
    for _ in range(iterations): # Generate new random data for each interation to simulate real scenario
        message = os.urandom(32)
        hasher = RSA_SHA256.new(message)
        
        start = time.perf_counter_ns()
        signature = signer.sign(hasher)
        sign_result_data.append(signature.hex())
        end = time.perf_counter_ns()
        sign_times_ns.append(end - start)

    sign_times_ms = [t / 1_000_000 for t in sign_times_ns]
    sign_result = {
        "algorithm": f"RSA-{key_size}",
        "operation": "Sign",
        "iterations": iterations,
        "average_ms": statistics.mean(sign_times_ms),
        "min_ms": min(sign_times_ms),
        "max_ms": max(sign_times_ms),
        "stdev_ms": statistics.pstdev(sign_times_ms),
        "raw_times_ms": sign_times_ms,
        "data": sign_result_data 
    }

    verify_times_ns = []
    verify_result_data = []
    for i in range(iterations): # Generate new random data for each iteration during verification as well
        message = os.urandom(32)
        hasher = RSA_SHA256.new(message)
        signature = signer.sign(hasher)  # Re-generate signature for the new message
        start = time.perf_counter_ns()
        verifier.verify(hasher, signature)  
        verify_result_data.append(signature.hex()) 
        end = time.perf_counter_ns()
        verify_times_ns.append(end - start)

    verify_times_ms = [t / 1_000_000 for t in verify_times_ns]
    verify_result = {
        "algorithm": f"RSA-{key_size}",
        "operation": "Verify",
        "iterations": iterations,
        "average_ms": statistics.mean(verify_times_ms),
        "min_ms": min(verify_times_ms),
        "max_ms": max(verify_times_ms),
        "stdev_ms": statistics.pstdev(verify_times_ms),
        "raw_times_ms": verify_times_ms,
        "data": verify_result_data 
    }
    return [sign_result, verify_result]

def write_results_to_csv(results_list, output_file):
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Algorithm", "Operation", "Iterations", "Average_ms", "Min_ms", "Max_ms", "Stdev_ms"])
        for result in results_list:
            writer.writerow([  
                result["algorithm"],
                result["operation"],
                result["iterations"],
                f"{result['average_ms']:.6f}",
                f"{result['min_ms']:.6f}",
                f"{result['max_ms']:.6f}",
                f"{result['stdev_ms']:.6f}",
            ])

        writer.writerow([])
        writer.writerow(["Algorithm", "Operation", "IterationIndex", "Time_ms", "Hashed_Data"])
        for result in results_list:
            times = result.get("raw_times_ms", [])
            for i, t in enumerate(times):
                data_hex = result.get("data", [])[i] 
                writer.writerow([
                    result["algorithm"],
                    result["operation"],
                    i,
                    f"{t:.6f}",
                    data_hex 
                ])

def print_summary_table(results_list, output_file):
    header = ["Algorithm", "Operation", "Iterations", "Average_ms", "Min_ms", "Max_ms", "Stdev_ms"]
    rows = []
    for r in results_list:
        row = [
            r["algorithm"],
            r["operation"],
            str(r["iterations"]),
            f"{r['average_ms']:.6f}",
            f"{r['min_ms']:.6f}",
            f"{r['max_ms']:.6f}",
            f"{r['stdev_ms']:.6f}"
        ]
        rows.append(row)
    
    all_data = [header] + rows
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*all_data)]
    
    # Create the formatted table output
    with open(output_file, 'w') as f:
        f.write(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(header)) + "\n")
        f.write("-+-".join("-" * col_widths[i] for i in range(len(header))) + "\n")
        for row in rows:
            f.write(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + "\n")

def format_row(row_data):
    return " | ".join(cell.ljust(15) for cell in row_data)

def main():
    BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "Benchmark_Results")
    algorithm_choice = input("Select an algorithm to benchmark:\n1. SHA-256\n2. ECC (Secp256k1)\n3. RSA\nEnter choice: ")
    if algorithm_choice == "1":
        algorithm_name = "SHA-256"
        algorithm_results = benchmark_sha256()
    elif algorithm_choice == "2":
        algorithm_name = "ECC"
        algorithm_results = benchmark_ecc()
    elif algorithm_choice == "3":
        algorithm_name = "RSA-2048"
        algorithm_results = benchmark_rsa()
    else:
        print("Invalid choice, select 1-3")
        return
    algorithm_directory = os.path.join(OUTPUT_DIRECTORY, algorithm_name)
    os.makedirs(algorithm_directory, exist_ok=True)

    timestamp = datetime.now().strftime("%d.%m.%y_%H-%M")
    summary_file = os.path.join(algorithm_directory, f"{algorithm_name}_benchmark_table_{timestamp}.csv")
    detailed_file = os.path.join(algorithm_directory, f"{algorithm_name}_benchmark_output_{timestamp}.csv")

    # Benchmark output
    write_results_to_csv(algorithm_results, detailed_file)

    # Benchmark table
    print_summary_table(algorithm_results, summary_file)
    print(f"\nBenchmark Complete!\nOutput saved to: {algorithm_directory}\n")

if __name__ == "__main__":
    main()
