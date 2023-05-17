""" Rabin Cryptography system """

from random import randint
import os

def generate_keypair(bits=2048):
    random_generator = Random.new().read
    rsa_key = RSA.generate(bits, random_generator)
    return rsa_key.exportKey(), rsa_key.publickey().exportKey()

def coeffs_gcd_extended(number1 , number2):
    """ Coeff using Euclide Algorithm """
    number1 = number1
    number2 = number2

    full_part = []

    while True:
        n_1 = max(number1, number2)
        n_2 = min(number1, number2)

        result = n_1 % n_2
        full_part.append(n_1 // n_2)

        if n_1 % n_2 == 0:
            break

        if number1 == n_1:
            number1 = result
            continue
        number2 = result

    s_0 = 1
    s_1 = 0
    t_0 = 0
    t_1 = 1

    index = 0
    while index != len(full_part) - 1:

        s_next = s_0 - full_part[index] * s_1
        s_0 = s_1
        s_1 = s_next

        t_next = t_0 - full_part[index] * t_1
        t_0 = t_1
        t_1 = t_next

        index += 1
    if number1 > number2:
        return s_next, t_next
    return t_next, s_next


class RabinCryptography:
    """ Rabin Cryptography """
    def generate_keys(self):
        """ Generates two numbers which satisfies condition p, q = 3mod(4)"""
        self.__q_var = 191
        self.__p_var = 139

        while self.__p_var == self.__q_var:
            self.__q_var = (randint(11230, 95737) * 4) + 3

        return self.__q_var * self.__p_var

    def __init__(self) -> None:
        self.n_var = self.generate_keys()

    @staticmethod
    def encode(key, message):
        """ Encode message with passed key """
        send_coded = []
        for symbol in message:
            ord_symbol = ord(symbol)
            bin_symbol = bin(ord_symbol)[2:] * 2
            new_ord = int(bin_symbol, 2)
            new_bin = (new_ord ** 2) % key
            send_coded.append(new_bin)

        return send_coded

    def recursive_power_modul(self, power, modul, number):
        """ Recursively find modul of numbers with big power """
        if power == 1:
            return number % modul

        result = self.recursive_power_modul(power // 2, modul, number)

        result = (result ** 2) % modul
        if power % 2 == 1:
            result = (result * number) % modul


        return result

    def decode(self, message):
        """ Decode message using key and codded message """
        line = ""

        for symbol in message:
            m_p_var = self.recursive_power_modul(0.25 * (1 + self.__p_var), self.__p_var, symbol)
            m_q_var = self.recursive_power_modul(0.25 * (1 + self.__q_var), self.__q_var, symbol)


            m_p_var_1 = self.__p_var - m_p_var
            m_q_var_1 = self.__q_var - m_q_var

            a_var, b_var = coeffs_gcd_extended(self.__p_var, self.__q_var)

            roots = []

            root_1 = (a_var * self.__p_var * m_q_var +\
                      b_var * self.__q_var * m_p_var) %\
                        (self.__p_var * self.__q_var)

            root_2 = (a_var * self.__p_var * m_q_var_1 +\
                      b_var * self.__q_var * m_p_var_1) %\
                        (self.__p_var * self.__q_var)

            root_3 = (a_var * self.__p_var * m_q_var_1 +\
                      b_var * self.__q_var * m_p_var) %\
                        (self.__p_var * self.__q_var)
            root_4 = (a_var * self.__p_var * m_q_var +\
                      b_var * self.__q_var * m_p_var_1) %\
                        (self.__p_var * self.__q_var)

            roots.append(bin(root_1)[2:])
            roots.append(bin(root_2)[2:])
            roots.append(bin(root_3)[2:])
            roots.append(bin(root_4)[2:])

            for root in roots:
                if len(root) % 2:
                    continue
                half = len(root) // 2
                if root[:half] == root[half:]:
                    line += chr(int(root[:half], 2))
                    break
        return line

cryptosystem = RabinCryptography()
key = cryptosystem.n_var
a = cryptosystem.encode(key, "hEANJSDANJSDB AHSDB AHSBD AHSDbasjhbd hasbdj BJsgvd ")
# print(a)
print(cryptosystem.decode(a))
