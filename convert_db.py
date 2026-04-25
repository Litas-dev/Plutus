#!/usr/bin/env python3
"""
Convert the pickle database to SQLite for memory efficiency.
"""
import os
import pickle
import sqlite3

DATABASE_DIR = r'database/MAR_23_2019/'
DB_FILE = 'plutus.db'

def convert_to_sqlite():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS addresses (address TEXT PRIMARY KEY)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_address ON addresses (address)')

    count = len(os.listdir(DATABASE_DIR))
    total_addresses = 0

    for i, p in enumerate(os.listdir(DATABASE_DIR)):
        print(f'\rProcessing {i+1}/{count} files...', end='')
        with open(DATABASE_DIR + p, 'rb') as file:
            address_set = pickle.load(file)
            addresses = list(address_set)
            c.executemany('INSERT OR IGNORE INTO addresses (address) VALUES (?)', [(addr,) for addr in addresses])
            total_addresses += len(addresses)

    conn.commit()
    conn.close()
    print(f'\nDone! Total addresses: {total_addresses}')

if __name__ == '__main__':
    convert_to_sqlite()