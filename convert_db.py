#!/usr/bin/env python3
"""
Convert the pickle database to SQLite for memory efficiency.
"""
import os
import pickle
import sqlite3

DATABASE_DIR = r'database/12_26_2025/'
DB_FILE = 'plutus.db'

def convert_to_sqlite():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS addresses (address TEXT PRIMARY KEY)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_address ON addresses (address)')

    count = len(os.listdir(DATABASE_DIR))
    total_addresses = 0

    for i, p in enumerate(os.listdir(DATABASE_DIR)):
        print(f'\rProcessing {i+1}/{count} files...', end='', flush=True)
        with open(DATABASE_DIR + p, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
            c.executemany('INSERT OR IGNORE INTO addresses (address) VALUES (?)', [(addr,) for addr in addresses])
            total_addresses += len(addresses)
            print(f' - {len(addresses)} addresses added (total: {total_addresses})', flush=True)
        conn.commit()  # Commit after each file

    conn.commit()
    conn.close()
    print(f'\nDone! Total addresses: {total_addresses}')

if __name__ == '__main__':
    convert_to_sqlite()