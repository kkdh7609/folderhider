#-*- coding: utf-8 -*-

# Python 3.6.4
# author: Kim Do Hyeon
# date: 2018.5.28

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256, md5
import os
import pickle


class AESmanager:
    def __init__(self, key):
        self.BLOCK_SIZE = 32
        self.MODE = AES.MODE_CBC
        self.PADDER = "|"
        self.key = bytes(key, 'utf-8')
        self.iv = bytes(chr(0) * 16, 'utf-8')

    def enc_AES(self, message):
        padd_message = self.padding(message)
        crypt_box = AES.new(self.key, self.MODE, self.iv)
        enc_message = crypt_box.encrypt(padd_message)
        return enc_message

    def dec_AES(self, message):
        crypt_box = AES.new(self.key, self.MODE, self.iv)
        dec_message = crypt_box.decrypt(message)
        dec_message = dec_message.decode('utf-8')
        dec_message = dec_message.rstrip(dec_message[-1])
        return dec_message

    def enc_file(self, file_name):
        crypt_box = AES.new(self.key, self.MODE, self.iv)
        out_file_name = file_name + '.encrypt'
        group_size = self.BLOCK_SIZE * 1024
        file_size = str(os.path.getsize(file_name))
        file_size = file_size.zfill(32)

        with open(file_name, 'rb') as inputFile:
            with open(out_file_name, 'wb') as outputFile:
                outputFile.write(file_size.encode())
                while True:
                    group = inputFile.read(group_size)
                    if len(group) == 0:
                        break
                    elif len(group) % self.BLOCK_SIZE != 0:
                        group = self.padding(group)
                    outputFile.write(crypt_box.encrypt(group))

    def dec_file(self, file_name):
        crypt_box = AES.new(self.key, self.MODE, self.iv)
        out_file_name = ".".join(file_name.split('.')[:-1])
        group_size = self.BLOCK_SIZE * 1024
        with open(file_name, 'rb') as inputFile:
            file_size = int(inputFile.read(32))
            with open(out_file_name, 'wb') as outputFile:
                while True:
                    group = inputFile.read(group_size)
                    if len(group) == 0:
                        break
                    outputFile.write(crypt_box.decrypt(group))
                outputFile.truncate(file_size)

    def padding(self, message):
        PADDER = self.PADDER
        if message[-1] == "|":
            PADDER = chr(0)
        #print(type(message))
        if type(message) != type(b"b"):
            message = message.encode()
        return message + (self.BLOCK_SIZE - (len(message) % self.BLOCK_SIZE)) * PADDER.encode()


class RSAmanager:
    def __init__(self):
        self.KEY_LENGTH = 2048

    def enc_RSA(self, message, pubkey):
        encrypter = PKCS1_OAEP.new(pubkey)
        enc_message = 0
        if type(message) != type(b"b"):
            enc_message = encrypter.encrypt(message.encode())
        else:
            enc_message = encrypter.encrypt(message)
        return enc_message

    def dec_RSA(self, message, prikey):
        decrypter = PKCS1_OAEP.new(prikey)
        try:
            dec_message = decrypter.decrypt(message)
        except ValueError:
            return b"b"
        try:
            return dec_message.decode('utf-8')
        except Exception:
            return dec_message

    def gen_key(self):
        rd_gen = Random.new().read
        prikey = RSA.generate(self.KEY_LENGTH, rd_gen)
        pubkey = prikey.publickey()
        return prikey, pubkey


def make_sha_key(password):
    try:
        key = sha256(password.encode("utf-8")).hexdigest()
    except Exception:
        key = sha256(password).hexdigest()
    return key


def make_md5_key(password):
    try:
        key = md5(password.encode("utf-8")).hexdigest()
    except Exception:
        key = md5(password).hexdigest()
    return key


def test():
    """
    rsa = RSAmanager()
    (prikey, pubkey) = rsa.gen_key()
    print(prikey.exportKey('DER'))
    print(pubkey.exportKey('DER'))
    pubkey = RSA.importKey(pubkey)
    prikey = RSA.importKey(prikey)
    """
    key = "password"
    message = "asdf"
    key = make_sha_key(key)
    md5_key = make_md5_key(key)
    crypt = AESmanager(md5_key)
    enc = crypt.enc_AES(message)
    print(enc)
    dec = crypt.dec_AES(enc)
    print(dec)
    rsa = RSAmanager()
    (prikey, pubkey) = rsa.gen_key()
    enc_r = rsa.enc_RSA(message, pubkey)
    print(enc_r)
    dec_r = rsa.dec_RSA(enc_r, prikey)
    print(dec_r)
    #file = "D:\\aaaaaaaa\\asdfdafdaf.zip"
    #crypt.enc_file(file)
    #file = "D:\\aaaaaaaa\\asdfdafdaf.zip.encrypt"
    #crypt.dec_file(file)


if __name__ == "__main__":
    test()