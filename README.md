# Plutus Bitcoin Brute Forcer

A Bitcoin wallet collider that brute forces random wallet addresses

**Optimized for Apple Silicon M1**: This version uses native ARM64 Python and optimized ECDSA libraries for maximum performance on M1 Macs.

# Like This Project? Give It A Star

[![](https://img.shields.io/github/stars/Isaacdelly/Plutus.svg)](https://github.com/Isaacdelly/Plutus)

# Dependencies

<a href="https://www.python.org/downloads/">Python 3.6</a> or higher (tested with Python 3.14 on Apple Silicon M1)

Python modules listed in the <a href="requirements.txt">requirements.txt</a>
  
Minimum <a href="#memory-consumption">RAM requirements</a>

# Installation

```
$ git clone https://github.com/Litas-dev/Plutus.git plutus

$ cd plutus

# Download the database from the original repository
$ git clone https://github.com/Isaacdelly/Plutus.git temp
$ mv temp/database ./
$ rm -rf temp

$ pip3 install -r requirements.txt

$ python3 convert_db.py  # Convert pickle database to SQLite for memory efficiency
```

# Quick Start

```
$ python3 plutus.py
```

# Proof Of Concept

A private key is a secret number that allows Bitcoins to be spent. If a wallet has Bitcoins in it, then the private key will allow a person to control the wallet and spend whatever balance the wallet has. So this program attempts to find Bitcoin private keys that correlate to wallets with positive balances. However, because it is impossible to know which private keys control wallets with money and which private keys control empty wallets, we have to randomly look at every possible private key that exists and hope to find one that has a balance.

This program is essentially a brute forcing algorithm. It continuously generates random Bitcoin private keys, converts the private keys into their respective wallet addresses, then checks the balance of the addresses. If a wallet with a balance is found, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence. 

# How It Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys using the `ecdsa` Python module. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii` and `hashlib` standard libraries.

A pre-calculated SQLite database of every P2PKH Bitcoin address with a positive balance is included in this project. The generated address is searched within the database, and if it is found that the address has a balance, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `multiprocessing.Process()` function in order to make concurrent calculations.

# Efficiency

It takes approximately `0.0012` seconds for this program to brute force a __single__ Bitcoin address (optimized for modern hardware including Apple Silicon M1). 

However, through `multiprocessing.Process()` a concurrent process is created for every CPU your computer has. So this program can brute force addresses at a rate of `cpu_count() ÷ 0.0012` addresses per second.

# Database FAQ

An offline SQLite database is used to find the balance of generated Bitcoin addresses. Run `python3 convert_db.py` to convert the included pickle files to SQLite format. This provides fast lookups with minimal memory usage.

# Expected Output

Every time this program checks the balance of a generated address, it will print the result to the user. If an empty wallet is found, then the wallet address will be printed to the terminal. An example is:

>1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45

However, if a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `plutus.txt`. An example is:

>hex private key: 5A4F3F1CAB44848B2C2C515AE74E9CC487A9982C9DD695810230EA48B1DCEADD<br/>
>WIF private key: 5JW4RCAXDbocFLK9bxqw5cbQwuSn86fpbmz2HhT9nvKMTh68hjm<br/>
>public key: 04393B30BC950F358326062FF28D194A5B28751C1FF2562C02CA4DFB2A864DE63280CC140D0D540EA1A5711D1E519C842684F42445C41CB501B7EA00361699C320<br/>
>address: 1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45<br/>

# Memory Consumption

This program uses minimal RAM as the database is stored in SQLite on disk rather than loaded into memory. Each process uses approximately 50-100MB of RAM, making it suitable for systems with limited memory.

# Recent Improvements & TODO

- [X] Fixed typos/formatting

- [ ] Update database

- [ ] Pickle loader

<a href="https://github.com/Isaacdelly/Plutus/issues">Create an issue</a> so I can add more stuff to improve

