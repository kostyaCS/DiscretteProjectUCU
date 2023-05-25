import random
import hashlib

def gcdExtended(a, b):
    """ Extended GCD Anlgorith """
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

class DSA():
    """ Digital Signature Algorithm """
    def __init__(self) -> None:
        self.dict = {}
        self.public, self.__private = self.keys()

    def add_signature(self, message):
        """ Adds digital signature to message
           and returns the same message with signature"""
        val_p,val_q, val_g, val_x = self.__private
        hash_of_object = int(hashlib.sha1(message.encode()).hexdigest(), 16)

        coeff = random.randint(0, val_q - 1)

        val_r = (((val_g**coeff) % val_p)) % val_q

        val_s = ((gcdExtended(coeff, val_q)[1]) *\
                 (hash_of_object + val_x * val_r)) % val_q
        return message, val_r, val_s

    def verify_signature(self, message_sign, public_key):
        """ Vetify signature and return True if valid and False if not """
        message, val_r, val_s = message_sign
        val_p,val_q, val_g, val_y = public_key
        hased_image = int(hashlib.sha1(message.encode()).hexdigest(), 16)

        a_1 = (hased_image * gcdExtended(val_s, val_q)[1]) % val_q
        a_2 = (gcdExtended(val_s, val_q)[1] * val_r) % val_q
        value = (((val_g**a_1) * (val_y**a_2)) % val_p) % val_q
        if value == val_r:
            return True
        return False

    def keys(self):
        """ Generates public and pivate keys """
        val_p = 1531447
        val_q = 5209
        val_h = 2
        val_g = int((val_h ** ((val_p - 1) / val_q)) % val_p)
        val_x = random.randint(0, val_q - 1)
        val_y = (val_g ** val_x) % val_p

        return [[val_p, val_q, val_g, val_y],
                 [val_p,val_q, val_g, val_x]]


dsa = DSA()
key = dsa.public
print(key)

signature = dsa.add_signature("message")
print(signature)
signature = (signature[0] + "1", signature[1], signature[2])

result = dsa.verify_signature(signature, key)
print(result)
