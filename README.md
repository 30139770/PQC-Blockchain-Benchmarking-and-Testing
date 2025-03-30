# PQC Blockchain Benchmarking and Testing

This repository contains all the code, tests, and benchmarks used as the end deliverable for my dissertation, **“Future Challenges of Quantum Computing in Blockchain Technology.”**

## Overview:

The primary objective of this project is to benchmark traditional cryptographic algorithms (such as SHA-256, RSA-2048, and ECC on the secp256k1 curve) and compare their performance with CRYSTALS-Dilithium2—a quantum-resistant digital signature algorithm approved by NIST. In addition to raw cryptographic performance, the repository also includes a simulation of a standard Ethereum transaction using ECDSA (secp256k1) and a proof-of-concept implementation where ECDSA is replaced with Dilithium2. This comparison provides insights into key sizes, signing and verification speeds, and overall performance implications in a blockchain environment.

## Repository Contents:
**Benchmarking Scripts**
The repository includes Python scripts to perform benchmarking:
* **Benchmark 1**: Tests SHA-256, RSA-2048, and ECC (secp256k1) for signing and verification, logging detailed timing and statistical data.
* **Benchmark 2**: Uses [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) to benchmark the post-quantum algorithm [Dilithium2](https://openquantumsafe.org/liboqs/algorithms/sig/dilithium.html)
>*Benchmarks produce CSV files that summarize statistical metrics (average, minimum, maximum, and standard deviation) and log raw execution times for each iteration.*

- **Ethereum Transaction Simulation**
Two separate demos simulate the signing and verification processes:
  * **Standard Ethereum Demo**: Uses the [web3.py](https://github.com/ethereum/web3.py) library along with ECDSA (seckp256k1) to generate Ethereum addresses, sign transactions and verify signatures.
  * **Ethereum Dilithium2 Demo:** Replaces the classical ECDSA approach with CRYSTALS-Dilithium2 (via liboqs-python), simulating address generation by hashing a post-quantum public key and demonstrating the transaction signing/verification flow.
> *Creates a public/private keypair, hashes public key to get a valid 20-byte Ethereum address, and performs a mock ETH transfer, hashes transaction data, and is signed with the private key then verified where all relevant metrics are recorded.*

## Libraries and Tools
  * **Standard Libraries**: `time`, `hashlib`, `statistics`, `csv`, `os`, `datetime`, and `random`
- **Cryptographic Libraries**:
  * `ECDSA` for ECC operations using the secp256k1 curve.
  * `pycryptodome` for RSA and SHA-256 benchmarks.
  * `liboqs-python` for testing CRYSTALS-Dilithium2, the NIST approved quantum-resistant algorithm.
* **Ethereum Tools**: `web3.py` and `eth_account` for simulating standard Ethereum transactions.

## How to Use
- **Pre-Requisites**:
  * [liboqs](https://github.com/open-quantum-safe/liboqs): Visit [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) repository for liboqs python installation
  * [git](https://git-scm.com/)
  * [CMake](https://cmake.org/)
  * [gcc](https://gcc.gnu.org/)
  * [Python3](https://www.python.org/)
  * [pip](https://pip.pypa.io/en/stable/installation/)
  * [Docker](https://www.docker.com/) (optional)
- Install Libraries: `pip install -r requirements.txt`

## Benchmarking
- **Classical Algorithms** *(RSA-2048, SHA-256, ECC-secp256k1)*
  * Run `python3 benchmark1.py`
  * Select algorithm using number keys (1-3) and hit  enter. It will parse 10,000 iterations of randomly generated data, unique for each iteration.
- **PQC-algorithm** *(Dilithium2)*
  * Run `python3 benchmark2.py`
  * Select Dilithium2 using the number keys and hit enter. It will parse 10,000 iterations of randomly generated data, unique for each iteration.

*Raw output of ECC (secp256k1) benchmark test:*
![Raw output of ECC (secp256k1) benchmark test.](https://i.imgur.com/JMA7VPq.png)

*Summary of ECC (secp256k1) benchmark test:*
![Summary of ECC (secp256k1) benchmark test.](https://i.imgur.com/cQPotmp.png)

*Raw output of Dilithium2 benchmark test:*
![Raw output of Dilithium2 benchmark test.](https://i.imgur.com/SJyNhDJ.png)

*Summary of Dilithium2 benchmark test:*
![Summary of Dilithium2 benchmark test.](https://i.imgur.com/BL4EWDS.png)

> *Outputs are saved as CSV files to the _Benchmark_Results_ folder. Each benchmark produces two CSV files, one has a table style summary and the other contains the raw data processed.*

## Ethereum and Dilithium2 Demo
- **Standard Ethereum Transaction Demo**:
  * Run `python3 ethereum_simulation.py`
  * The results are output in the terminal.

 *Standard Ethereum transaction demo:*
 ![Standard Ethereum transaction demo](https://i.imgur.com/7Cqp14s.png)

- **Dilithium2 Ethereum Transaction Demo**:
  * Run `python3 ethereum_dilithium.py`
  * The results are output in the terminal.

*Dilithium2 Ethereum transaction demo*
![Dilithium2 Ethereum transaction demo](https://i.imgur.com/tqClUjk.png)

> ## License
*This repository is provided as is for educational and research purposes. Please refer to the LICENSE file for more details.*
