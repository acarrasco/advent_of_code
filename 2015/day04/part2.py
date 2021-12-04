import hashlib

input = 'bgvyzdsv'

prefix = '0' * 6
n = 0
while not hashlib.md5(input + str(n)).hexdigest().startswith(prefix):
    n += 1

print(n)