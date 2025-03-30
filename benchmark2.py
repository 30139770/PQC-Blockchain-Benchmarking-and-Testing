import time
import statistics
import csv
import os
from datetime import datetime
import random
import oqs

# Use the same base directory logic as the other scripts
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "Benchmark_Results")
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

def generate_random_data(size):
    """Generate random data for testing."""
    return bytes([random.randint(0, 255) for _ in range(size)])

def benchmark_crystals_dilithium(iterations=10000):
    sigalg = "Dilithium2"

    sign_times_ns = []
    sign_result_data = []
    messages = []

    with oqs.Signature(sigalg) as signer:
        public_key = signer.generate_keypair()

        for _ in range(iterations):
            message = generate_random_data(32)
            messages.append(message)

            start = time.perf_counter_ns()
            signature = signer.sign(message)
            end = time.perf_counter_ns()

            sign_result_data.append(signature.hex())
            sign_times_ns.append(end - start)

    sign_times_ms = [t / 1_000_000 for t in sign_times_ns]

    sign_results = {
        "algorithm": "CRYSTALS-Dilithium",
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

    with oqs.Signature(sigalg) as verifier:
        for i in range(iterations):
            message = messages[i]
            signature = bytes.fromhex(sign_result_data[i])

            start = time.perf_counter_ns()
            valid = verifier.verify(message, signature, public_key)
            end = time.perf_counter_ns()

            verify_times_ns.append(end - start)

    verify_times_ms = [t / 1_000_000 for t in verify_times_ns]

    verify_results = {
        "algorithm": "CRYSTALS-Dilithium",
        "operation": "Verify",
        "iterations": iterations,
        "average_ms": statistics.mean(verify_times_ms),
        "min_ms": min(verify_times_ms),
        "max_ms": max(verify_times_ms),
        "stdev_ms": statistics.pstdev(verify_times_ms),
        "raw_times_ms": verify_times_ms,
        "data": sign_result_data
    }

    return [sign_results, verify_results]

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
    with open(output_file, 'w') as f:
        f.write(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(header)) + "\n")
        f.write("-+-".join("-" * col_widths[i] for i in range(len(header))) + "\n")
        for row in rows:
            f.write(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + "\n")

def main():
    algorithm_choice = input("Select an algorithm to benchmark:\n1. CRYSTALS-Dilithium\nEnter choice: ")
    if algorithm_choice == "1":
        algorithm_name = "CRYSTALS-Dilithium"
        algorithm_results = benchmark_crystals_dilithium()
    else:
        print("Invalid choice.")
        return
    algorithm_directory = os.path.join(OUTPUT_DIRECTORY, algorithm_name)
    os.makedirs(algorithm_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    summary_file = os.path.join(algorithm_directory, f"benchmark_table_{timestamp}.csv")
    detailed_file = os.path.join(algorithm_directory, f"benchmark_output_{timestamp}.csv")
    write_results_to_csv(algorithm_results, detailed_file)
    print_summary_table(algorithm_results, summary_file)
    print(f"Benchmark saved to {algorithm_directory}")

if __name__ == "__main__":
    main()
