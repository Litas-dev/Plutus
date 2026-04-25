# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import os
import time
import pickle
import hashlib
import argparse
import binascii
import multiprocessing
from pathlib import Path
from ellipticcurve.privateKey import PrivateKey

DATABASE = Path('database/MAR_23_2019')

def generate_private_key(): 
	"""
	Generate a random 32-byte hex integer which serves as a randomly 
	generated Bitcoin private key.
	Average Time: 0.0000061659 seconds
	"""
	return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def private_key_to_public_key(private_key):
	"""
	Accept a hex private key and convert it to its respective public key. 
	Because converting a private key to a public key requires SECP256k1 ECDSA 
	signing, this function is the most time consuming and is a bottleneck in 
	the overall speed of the program.
	Average Time: 0.0031567731 seconds
	"""
	pk = PrivateKey().fromString(bytes.fromhex(private_key))
	return '04' + pk.publicKey().toString().hex().upper()

def public_key_to_address(public_key):
	"""
	Accept a public key and convert it to its resepective P2PKH wallet address.
	Average Time: 0.0000801390 seconds
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

def process(private_key, public_key, address, database):
	"""
	Accept an address and query the database. If the address is found in the 
	database, then it is assumed to have a balance and the wallet data is 
	written to the hard drive. If the address is not in the database, then it 
	is assumed to be empty and printed to the user.
	Average Time: 0.0000026941 seconds
	"""
	if any(address in partition for partition in database):
		with open('plutus.txt', 'a') as file:
			file.write('hex private key: ' + str(private_key) + '\n' +
				   'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
			      	   'public key: ' + str(public_key) + '\n' +
			           'address: ' + str(address) + '\n\n')
		return True
	return False

def private_key_to_WIF(private_key):
	"""
	Convert the hex private key into Wallet Import Format for easier wallet 
	importing. This function is only called if a wallet with a balance is 
	found. Because that event is rare, this function is not significant to the 
	main pipeline of the program and is not timed.
	"""
	digest = hashlib.sha256(binascii.unhexlify('80' + private_key)).hexdigest()
	var = hashlib.sha256(binascii.unhexlify(digest)).hexdigest()
	var = binascii.unhexlify('80' + private_key + var[0:8])
	alphabet = chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	value = pad = 0
	result = ''
	for i, c in enumerate(var[::-1]): value += 256**i * c
	while value >= len(alphabet):
		div, mod = divmod(value, len(alphabet))
		result, value = chars[mod] + result, div
	result = chars[value] + result
	for c in var:
		if c == 0: pad += 1
		else: break
	return chars[0] * pad + result

def main(database, print_addresses=False, report_every=0):
	"""
	Create the main pipeline by using an infinite loop to repeatedly call the 
	functions, while utilizing multiprocessing from __main__. Because all the 
	functions are relatively fast, it is better to combine them all into 
	one process.
	"""
	count = 0
	start = time.time()
	while True:
		private_key = generate_private_key()			# 0.0000061659 seconds
		public_key = private_key_to_public_key(private_key) 	# 0.0031567731 seconds
		address = public_key_to_address(public_key)		# 0.0000801390 seconds
		found = process(private_key, public_key, address, database) 	# 0.0000026941 seconds
		count += 1
		if print_addresses and not found:
			print(str(address))
		if report_every and count % report_every == 0:
			elapsed = max(time.time() - start, 1e-9)
			print(f'pid={os.getpid()} checked={count} rate={count/elapsed:.2f}/s')
									# --------------------
									# 0.0032457721 seconds

def load_database(database_dir):
	"""
	Deserialize the database and read into a list of sets for easier selection 
	and O(1) complexity.
	"""
	database = [set() for _ in range(4)]
	files = sorted(database_dir.glob('*.pickle'))
	count = len(files)
	if count == 0:
		raise FileNotFoundError(f'No .pickle files found in database path: {database_dir}')

	half = count // 2
	quarter = half // 2
	for c, file_path in enumerate(files):
		print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
		with file_path.open('rb') as file:
			if c < half:
				if c < quarter: database[0] = database[0] | pickle.load(file)
				else: database[1] = database[1] | pickle.load(file)
			else:
				if c < half + quarter: database[2] = database[2] | pickle.load(file)
				else: database[3] = database[3] | pickle.load(file)
	print('DONE')
	return tuple(database)

def parse_args():
	parser = argparse.ArgumentParser(description='Plutus Bitcoin Brute Forcer')
	parser.add_argument(
		'--database',
		default=str(DATABASE),
		help='Path to folder containing .pickle address files (default: database/MAR_23_2019)'
	)
	parser.add_argument(
		'--workers',
		type=int,
		default=multiprocessing.cpu_count(),
		help='Number of worker processes to start (default: cpu_count)'
	)
	parser.add_argument(
		'--print-addresses',
		action='store_true',
		help='Print each checked empty address (disabled by default for better performance)'
	)
	parser.add_argument(
		'--report-every',
		type=int,
		default=0,
		help='Print progress every N generated addresses in each worker (default: disabled)'
	)
	return parser.parse_args()

if __name__ == '__main__':
	"""
	Initialize the multiprocessing to target the main function with a configurable
	number of concurrent processes.
	"""
	args = parse_args()
	database_path = Path(args.database)
	database = load_database(database_path)

	# To verify the database size, remove the # from the line below
	#print('database size: ' + str(sum(len(i) for i in database))); quit()

	processes = []
	for _ in range(max(args.workers, 1)):
		proc = multiprocessing.Process(
			target=main,
			args=(database, args.print_addresses, args.report_every),
		)
		processes.append(proc)
		proc.start()

	try:
		for proc in processes:
			proc.join()
	except KeyboardInterrupt:
		for proc in processes:
			proc.terminate()
		for proc in processes:
			proc.join()
