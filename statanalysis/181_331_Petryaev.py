import math
from sympy.ntheory import totient

def doubl_p(P_arg, a, p):
    lyambda_arg = ['', '']
    lyambda_arg[0] = (3 * P_arg[0] ** 2 + a) % p
    lyambda_arg[1] = 2 * P_arg[1] % p

    if not (lyambda_arg[0]/lyambda_arg[1]).is_integer():
        lyambda_arg[0] = lyambda_arg[0] % p
        lyambda_arg[1] = (lyambda_arg[1] ** (totient(p) - 1)) % p
        lyambda_arg = int(lyambda_arg[0] * lyambda_arg[1] % p)
    else:
        lyambda_arg = int(lyambda_arg[0]/lyambda_arg[1])

    x = (lyambda_arg ** 2 - 2 * P_arg[0]) % p
    y = (lyambda_arg * (P_arg[0] - x) - P_arg[1]) % p
    return x, y

def eiler_func(a):
    p = 0
    for i in range(a):
        if math.gcd(a, i) == 1:
            p += 1
    return p

def key_gen(P, k, a, p):
    k = bin(k)[3:]
    P_ = P
    for i in k:
        P_ = doubl_p(P_, a, p)
        if i == '1':
            P_ = add_p(P, P_, p)
    return P_

def add_p(P1, P2, p):
    lyambda_arg = ['', '']
    lyambda_arg[0] = (P2[1] - P1[1]) % p
    lyambda_arg[1] = (P2[0] - P1[0]) % p

    if not (lyambda_arg[0]/lyambda_arg[1]).is_integer():
        lyambda_arg[0] = lyambda_arg[0] % p
        lyambda_arg[1] = (lyambda_arg[1] ** (totient(p) - 1)) % p
        lyambda_arg = int(lyambda_arg[0] * lyambda_arg[1] % p)
    else:
        lyambda_arg = int(lyambda_arg[0]/lyambda_arg[1])

    x = (lyambda_arg ** 2 - P1[0] - P2[0]) % p
    y = (lyambda_arg * (P1[0] - x) - P1[1]) % p
    return x, y

def encrypt(msg, Cb):
    global P
    msg = msg_to_unicode(msg)
    new_msg = []

    for i in range(len(msg)):
        public_key = key_gen(P, Cb, a, p)
        private_key = key_gen(P, k, a, p)
        P = key_gen(public_key, k, a, p)

        new_msg.append(private_key)
        new_msg.append(str(int(msg[i]) * P[0] % p))
    return new_msg

def decrypt(message, Cb):
    new_message = []
    for i in range(0, len(message), 2):
        P = key_gen(message[i], Cb, a, p)

        new_message.append(int(message[i+1]) * (P[0] ** (p - 2)) % p)

    new_message = unicode_to_msg(new_message)
    return new_message

def check_prime(a):
    return all(a % i for i in range(2, a))

def msg_to_unicode(message):
    new_message = []
    new_message.append(('0' * (4 - len(str(message))) + str(message)))
    return new_message

def unicode_to_msg(message):
    new_message = ''
    for i in message:
        new_message += chr(i)
    return message[0]

q = int(input('Введите q: '))
a = int(input('Введите a: '))
b = int(input('Введите b: '))
p = int(input('Введите p: '))
while not check_prime(p):
    p = int(input('Ошибка! p должно быть простым: '))
k = int(input('Введите k: '))
while k <= 0 or k >= q:
    k = int(input(f'Ошибка! k должно быть условию 0 < k < {q}: '))
P = tuple(map(int, input('Введите G (через пробел): ').split()))

message = input('Введите сообщение: ')
key = int(input('Введите закрытый ключ: '))
while key <= 0 or key >= q:
    key = int(input(f'Ошибка! Закрытый ключ должнен быть 0 < Cb < {q}: '))

enc = encrypt(message, key)
print('Зашифрованное сообщение:', enc)
dec = decrypt(enc, key)
print('Расшифрованное сообщение:', dec)

# одинчасутромстоитдвухчасоввечеромтчк