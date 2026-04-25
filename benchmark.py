#!/usr/bin/env python3
"""
Quick performance test for Plutus on Apple Silicon
Compares Python3 vs PyPy3 performance
"""
import os
import hashlib
import binascii
import ecdsa
import sqlite3
import time
import multiprocessing

DATABASE = 'plutus.db'

def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('ascii').upper()

def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_secret_exponent(int(private_key, 16), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x().to_bytes(32, 'big')
    y = vk.pubkey.point.y().to_bytes(32, 'big')
    return '04' + binascii.hexlify(x + y).decode('ascii')

def public_key_to_address(public_key):
    """
    Accept a public key and convert it to its respective P2PKH wallet address.
    """
    output = []
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    encoding = binascii.unhexlify(public_key.encode())
    var.update(hashlib.sha256(encoding).digest())
    var_encoded = ('00' + var.hexdigest()).encode()
    digest = hashlib.sha256(binascii.unhexlify(var_encoded)).digest()
    var_hex = '00' + var.hexdigest() + hashlib.sha256(digest).hexdigest()[0:8]
    count = [char != '0' for char in var_hex].index(True) // 2
    n = int(var_hex, 16)
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    for i in range(count): output.append(alphabet[0])
    return ''.join(output[::-1])

def process(private_key, public_key, address, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM addresses WHERE address = ? LIMIT 1", (address,))
    result = cursor.fetchone()
    if result:
        print(f"FOUND: {address}")
        with open('plutus.txt', 'a') as f:
            f.write(f"Address: {address}\nPrivate Key: {private_key}\nPublic Key: {public_key}\n\n")
    else:
        print(address)

def benchmark_keys(count=100):
    """Benchmark key generation and processing"""
    print(f"Benchmarking {count} keys...")

    # Create database connection
    conn = sqlite3.connect(DATABASE)

    start_time = time.time()
    for i in range(count):
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        process(private_key, public_key, address, conn)

    end_time = time.time()
    total_time = end_time - start_time
    keys_per_second = count / total_time

    conn.close()
    return keys_per_second

if __name__ == '__main__':
    print("Apple Silicon Plutus Performance Test")
    print("=" * 40)

    keys_per_second = benchmark_keys(100)
    print(".1f")

    # Estimate full multiprocessing performance
    cpu_count = multiprocessing.cpu_count()
    estimated_total = keys_per_second * cpu_count
    print(f"Estimated with multiprocessing ({cpu_count} cores): {estimated_total:.1f} keys/second")
    print(f"That's {estimated_total * 3600:.0f} keys/hour or {estimated_total * 86400 / 1000000:.1f} million keys/day")