"""Module for RSA encrypting and decryption"""
import math
import random
from sympy import randprime


def power(number, power_num, modulo):
    """
    >>> power(15, 98, 17)
    4"""
    result = 1
    temp_var = number % modulo

    while power_num > 0:
        if power_num % 2:
            result = (result * temp_var) % modulo
        temp_var = (temp_var * temp_var) % modulo
        power_num = power_num >> 1

    return result % modulo



class RSA:
    """Rsa algorithm for encryption"""
    def __init__(self, bits):
        self._public_key, self._private_key = self.keys_generator(bits)

    def get_public(self):
        """Get public key"""
        print(self._public_key)

    def get_private(self):
        """Get private key"""
        print(self._private_key)

    def eq_encrypt_decrypt(self, message):
        """Check if message and decrypt message is equal"""
        encrypt = self.encrypt_message(message)
        decrypt = self.decrypt_message(encrypt)
        return message == decrypt


    def keys_generator(self, bits = 256):
        """Generate public and private key for rsa algorithm"""
        if bits not in [32, 64, 128, 256, 512, 1024, 2048]:
            raise ValueError('Value of bits must be power of 2 from 32 to 2048')
        ceil, floor = 2 ** (bits//2), 2 ** (bits//2 + 1)
        prime_1 = randprime(ceil, floor)
        prime_2 = randprime(ceil, floor)
        prime_product = prime_1 * prime_2
        phi = (prime_1 - 1) * (prime_2 - 1)
        public = random.randint(1, phi)
        while math.gcd(public, phi) != 1:
            public = random.randint(1, phi)
        private = pow(public, -1, phi)
        return ((public, prime_product), (private, prime_product))

    def encrypt_message(self, message,):
        """Encrypt message using private key"""
        encrypt = []
        for char in message:
            own_add = power(ord(char), self._public_key[0], self._public_key[1])
            encrypt.append(own_add)
        return encrypt

    def decrypt_message(self, encrypt_message):
        """Decrypt message using private key"""
        decrypted = []
        for elem in encrypt_message:
            decrypt_num = power(elem, self._private_key[0], self._private_key[1])
            decrypted.append(chr(decrypt_num))
        return ''.join(decrypted)


if __name__ == '__main__':
    rsa = RSA(64)
    message_encr = 'hello, my name Tolik 12412412312'
    print(rsa.eq_encrypt_decrypt(message_encr))
