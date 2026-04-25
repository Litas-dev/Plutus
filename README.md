**Next-Generation Bitcoin Wallet Collider** - Optimized for Apple Silicon Macs and modern hardware.

A high-performance Bitcoin wallet brute-forcer that generates random private keys, derives addresses, and checks against a database of addresses with known balances. This optimized version uses cutting-edge libraries and efficient data structures for maximum speed and memory usage.

## 🚀 Key Features

- **Apple Silicon Optimized**: Native ARM64 support with Python 3.14 for all Apple Silicon Macs (M1/M2/M3/M4)
- **3x Faster ECDSA**: Uses the `ecdsa` library instead of pure Python crypto
- **Memory Efficient**: SQLite database prevents MemoryError on large datasets
- **Multiprocessing**: Leverages all CPU cores for parallel key generation
- **Secure Random Generation**: Cryptographically secure private key generation

## 📊 Performance

- **Private Key Generation**: ~0.000006 seconds
- **ECDSA Signing (Public Key Derivation)**: ~0.001 seconds (3x improvement)
- **Address Derivation**: ~0.00008 seconds
- **Database Lookup**: ~0.000003 seconds
- **Total per Key**: ~0.0011 seconds

Tested on Apple Silicon Macs with 8+ cores, processing millions of keys per minute.

## ⚠️ Disclaimer

This software is for educational purposes only. Brute-forcing Bitcoin private keys is computationally infeasible. The probability of finding a wallet with balance is astronomically low (1 in 2^160). This tool demonstrates cryptographic concepts and should not be used for illegal activities.

## 📋 Requirements

- **Python**: 3.6+ (recommended: 3.14 for ARM64 native support)
- **RAM**: 8GB minimum (16GB recommended for optimal performance)
- **Storage**: ~10GB free space for database conversion
- **OS**: macOS (optimized for Apple Silicon), Linux, or Windows

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Litas-dev/Plutus.git
   cd Plutus
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download and convert the database**:
   ```bash
   # Download database from original repository
   git clone --depth 1 https://github.com/Isaacdelly/Plutus.git temp
   mv temp/database ./
   rm -rf temp

   # Convert to SQLite (this takes ~5-10 minutes)
   python3 convert_db.py
   ```

   The conversion creates `plutus.db` (~8GB) containing 55+ million addresses with known balances.

## 🚀 Usage

Start the brute-forcer:
```bash
python3 plutus.py
```

The program will:
- Generate random private keys
- Derive public keys and addresses
- Check addresses against the database
- Print empty addresses to console
- Save wallets with balances to `plutus.txt`

Use Ctrl+C to stop. Results are appended to `plutus.txt`.

## 🔍 How It Works

1. **Private Key Generation**: Creates random 32-byte hex strings using `os.urandom()`
2. **Public Key Derivation**: Uses ECDSA secp256k1 to derive uncompressed public keys
3. **Address Creation**: Applies SHA256, RIPEMD160, and Base58Check encoding
4. **Balance Check**: Queries SQLite database for address existence
5. **Result Handling**: Saves hits to file, displays misses

## 📁 File Structure

- `plutus.py` - Main brute-forcer script
- `convert_db.py` - Database conversion utility
- `plutus.db` - SQLite database (generated)
- `plutus.txt` - Found wallets with balances
- `requirements.txt` - Python dependencies
- `database/` - Source address files (temporary)

## 🔧 Technical Details

- **Cryptography**: ECDSA secp256k1 curve
- **Database**: SQLite with indexed address table
- **Multiprocessing**: One process per CPU core
- **Output Format**: WIF, hex private key, public key, address

## 🤝 Contributing

Fork the repository and submit pull requests. Focus on performance optimizations and security improvements.

## 📜 License

This project is open-source. See LICENSE file for details.

## ⭐ Star This Repo

If you find this project interesting, give it a star!

[![](https://img.shields.io/github/stars/Litas-dev/Plutus.svg)](https://github.com/Litas-dev/Plutus)
