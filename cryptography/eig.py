"""Module with modulo powering and class of ElGamal Encryption Algorithm"""
import random
import math

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

class EIG:
    """
    Class for ElGamal Encryption Algorithm"""
    def __init__(self, bits):
        self._public_key, self._private_key = self.generate_keys(bits)
        self._large_number = self._public_key[1]

    def get_public(self):
        """Return public key"""
        return self._public_key

    def get_private(self):
        """Return private key"""
        return self._private_key

    def get_largenumber(self):
        """Return large number, that was generated"""
        return self._large_number

    def equal_encrypt_orig(self, message):
        """Check equalence of message and its decryption"""
        encrypt, p = self.encrypt_message(message, *self._public_key)

        decrypt = self.decrypt_message(encrypt, p, self.get_private(), self._large_number)
        return message == decrypt

    def generate_keys(self, bits):
        """Generate key for encryption
        Generate q = large number in size of bits variable
        Also generate g = range(1, q), which is basis for all power raising,
        a = range(1, q), gcd(a, q) = 1, a is a private key
        h = g^a(mod q)
        return public key = (h, q, g) and private key = a
        """

        large_number = random.randint(2**bits, 2**(bits + 1)) #generate random large number in size of bits variable
        g = random.randint(1, large_number) #generate random number from 1 to large number (g)

        key = random.randint(1, large_number) #also generate random number, its gcd with large number must be equal to 1, it is our private key (a)
        while math.gcd(key, large_number) != 1:
            key = random.randint(1, large_number)

        h = power(g, key, large_number) #raise g to the power of key modulo large_number (h = g^a variable)
        return (h, large_number, g), key #public key is tuple of h, large number and g, private key its number key (gcd(key, q) = 1)

    def encrypt_message(self: object, msg: str, h: int, large_number: int, g: int):
        """Encrypt message
        Require message, h = g^a(mod q), q = large number, g = random number
        Generate k = random number in range(1, q)
        Calculate p = g^k(mod q) will be needed for decryption
        Calculate s = h^k(mod q) = g^ak(mod q)
        Encrypt ord of message elements by multiplying its by s
        Return Encrypted message(list) and p = g^k(mod q)"""

        encrypt = []
        k = random.randint(1, large_number) # generate number k, gcd(k, large number) = 1
        while math.gcd(k, large_number) != 1:
            k = random.randint(1, large_number)

        p = power(g, k, large_number) #raise g to the power of k modulo large number (g^k, number to return after encryption)
        s = power(h, k, large_number) #raise h to the power of k modulo large number (g^ak, number for encryption)

        for elem in msg:
            encrypt.append(ord(elem) * s) #multiply ord of each letter element by g^ak

        return encrypt, p #return encrypt message(list) and p = g^k

    def decrypt_message(self, en_message, p, key, q):
        """Decrypt message
        Require encrypt message, p = g^k(mod q), a(private key), q = large number
        Find s = g^ak(mod q) from encryption  and divide all ecrypt elements by it
        Return Original message"""
        de_message = []

        s = power(p, key, q) #Find s = g^ak from encryption by raising p = g^k to the power of a modulo large number

        for elem in en_message:
            de_message.append(chr(int(elem / s))) #divide each encrypt element by s = g^ak and find its chr()

        return ''.join(de_message)


if __name__ == '__main__':
    eig = EIG(128)
    print(eig.equal_encrypt_orig('Hello'))
