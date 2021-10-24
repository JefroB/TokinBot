from cryptography.fernet import Fernet
from globals import globals as g
import os
import struct

def generate_key_file():
	key = Fernet.generate_key()
	filename = './breakfast/hashbrowns.txt'
	f = open(filename,"wb")
	f.write(key)
	f.close()
	os.chmod(filename, 0o600)


def load_key():
	filename = './breakfast/hashbrowns.txt'
	return open(filename, "rb").read()


def encrypt_file(message, filename):
	key = load_key()
	encoded_message = message.encode()
	f = Fernet(key)
	encrypted_message = f.encrypt(encoded_message)
	f = open(filename,"wb")
	f.write(encrypted_message)
	f.close()
	os.chmod(filename, 0o600)


def decrypt_file(filename):
	f = open(filename, "r")
	if f.mode == 'r':
		message =f.read()
		decrypt_this = rawbytes(message)

	key = load_key()
	f = Fernet(key)
	decrypted_message = f.decrypt(decrypt_this)

	return decrypted_message.decode()


def rawbytes(s):
	outlist = []
	for cp in s:
		num = ord(cp)
		if num < 255:
			outlist.append(struct.pack('B', num))
		elif num < 65535:
			outlist.append(struct.pack('>H', num))
		else:
			b = (num & 0xFF0000) >> 16
			H = num & 0xFFFF
			outlist.append(struct.pack('>bH', b, H))
	return b''.join(outlist)