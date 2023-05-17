""" Rabin Cryptography system """

from random import randint
import random

def n_bit_random(bitsize):
    """ Generates random integer with particular bitsize """
    return randint(2**bitsize, 2**(bitsize + 1))


def is_miller_rabin_passed(miller_rabin_candidate):
	'''Run 200 iterations of Rabin Miller Primality test'''

	maxDivisionsByTwo = 0
	evenComponent = miller_rabin_candidate-1

	while evenComponent % 2 == 0:
		evenComponent >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1)

	def trialComposite(round_tester):
		if pow(round_tester, evenComponent,
			miller_rabin_candidate) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * evenComponent,
				miller_rabin_candidate) == miller_rabin_candidate-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 200
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2,
					miller_rabin_candidate)
		if trialComposite(round_tester):
			return False
	return True

def generate_key(bitsize):
    """ Generate key which = 3mod4 and is prime with paricular bitsize """
    while True:
        number = (n_bit_random(bitsize) * 4) + 3
        if is_miller_rabin_passed(number):
            break
    return number

def coeffs_gcd_extended(number1 , number2):
    """ Coeff using Euclide Algorithm """
    number1_save = number1
    number2_save = number2

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

    if number1_save < number2_save and abs(s_next) > abs(t_next):
        return s_next, t_next
    if number1_save > number2_save and abs(s_next) < abs(t_next):
        return s_next, t_next
    if number1_save < number2_save and abs(s_next) < abs(t_next):
        return t_next, s_next
    return t_next, s_next


class RabinCryptography:
    """ Rabin Cryptography """
    def generate_keys(self):
        """ Generates two numbers which satisfies condition p, q = 3mod(4)"""
        self.__q_var = generate_key(50)
        self.__p_var = generate_key(50)
        print(self.__p_var, self.__q_var)
        while self.__p_var == self.__q_var:
            self.__q_var = generate_key(5)

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
                        (self.n_var)

            root_2 = (a_var * self.__p_var * m_q_var_1 +\
                      b_var * self.__q_var * m_p_var_1) %\
                        (self.n_var)

            root_3 = (a_var * self.__p_var * m_q_var_1 +\
                      b_var * self.__q_var * m_p_var) %\
                        (self.n_var)
            root_4 = (a_var * self.__p_var * m_q_var +\
                      b_var * self.__q_var * m_p_var_1) %\
                        (self.n_var)

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
a = cryptosystem.encode(key, "h ajsdhba sdjh ashbd ad hjasd ajsdk ")
# print(a)
print(cryptosystem.decode(a))
