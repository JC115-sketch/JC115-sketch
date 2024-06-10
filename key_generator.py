import random
import sys
import os
import prime_numbers
import cryptomath


def main():
    # 1024-bit key pairs
    print("Generating key files...")
    make_key_files('key_gen', 1024)
    print("Key files ready")


def generate_key(key_size):
    p = 0
    q = 0
    # creating two prime numbers, p and q. n = p * q
    while p == q:
        p = prime_numbers.generate_large_prime_num(key_size)
        q = prime_numbers.generate_large_prime_num(key_size)
    n = p * q

    # creating number (e) that is relatively prime () to (p - 1) * (q - 1)
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # calculate (d) the mod inverse of e
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)

    print('Public key:', public_key)
    print('Private key:', private_key)

    return public_key, private_key


def make_key_files(name, key_size):
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        sys.exit(
            'WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name.' % (name, name))

    public_key, private_key = generate_key(key_size)

    print()
    print('The public key is a %s and a %s digit number.' % (len(str(public_key[0])), len(str(public_key[1]))))
    print('Writing public key to file %s_pubkey.txt...' % (name))
    fo = open('%s_pubkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (key_size, public_key[0], public_key[1]))
    fo.close()

    print()
    print('The private key is a %s and a %s digit number.' % (len(str(private_key[0])), len(str(private_key[1]))))
    print('Writing private key to file %s_privkey.txt...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (key_size, private_key[0], private_key[1]))
    fo.close()


# If makePublicPrivateKeys.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
    main()

