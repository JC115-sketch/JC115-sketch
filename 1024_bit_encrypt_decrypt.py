import sys
import math

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


def main():
    file_name = 'encrypted_file.txt'
    mode = input("Please enter 'encrypt' or 'decrypt' to select mode: ")

    if mode == 'encrypt':
        message = 'Please send to this BTC address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'

        pub_key_file_name = 'key_gen_pubkey.txt'
        print('Encrypting and writing to %s...' % (file_name))
        encrypted_text = encrypt_and_write_file(file_name, pub_key_file_name, message)

        print('Encrypted text:')
        print(encrypted_text)

    elif mode == 'decrypt':

        priv_key_file_name = 'key_gen_privkey.txt'
        print("Reading from %s and decrypting..." % (file_name))
        decrypted_text = read_from_file_decrypt(file_name, priv_key_file_name)

        print('Decrypted text:')
        print(decrypted_text)


def get_blocks_from_text(message, block_size):
    for character in message:
        if character not in SYMBOLS:
            print('Error - invalid character')
            sys.exit()
    block_ints = []
    for block_start in range(0, len(message), block_size):
        block_integer = 0
        for i in range(block_start, min(block_start + block_size, len(message))):
            block_integer += (SYMBOLS.index(message[i])) * (len(SYMBOLS)) ** (i % block_size)
        block_ints.append(block_integer)
    return block_ints


def get_text_from_blocks(block_ints, message_length, block_size):
    message = []
    for block_integer in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                char_index = block_integer // (len(SYMBOLS) ** i)
                block_integer = block_integer % (len(SYMBOLS) ** i)
                block_message.insert(0, SYMBOLS[char_index])
        message.extend(block_message)
    return ''.join(message)


def encrypt_message(message, key, block_size):
    encrypted_blocks = []
    n, e = key
    for block in get_blocks_from_text(message, block_size):
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, block_size):
    decrypted_blocks = []
    n, d = key
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_file_name):
    fo = open(key_file_name)
    content = fo.read()
    fo.close()
    key_size, n, EorD = content.split(',')
    return (int(key_size), int(n), int(EorD))


def encrypt_and_write_file(message_file, key_file_name, message, block_size=None):
    key_size, n, e = read_key_file(key_file_name)
    if block_size == None:
        # set to largest possible block size
        block_size = int(math.log(2 ** key_size, len(SYMBOLS)))
    # verify key size is large enough for block size
    if not (math.log(2 ** key_size, len(SYMBOLS)) >= block_size):
        sys.exit('Error - Block size is too large for key and symbol set size')
    encrypted_blocks = encrypt_message(message, (n, e), block_size)

    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ','.join(encrypted_blocks)

    encrypted_content = '%s;%s;%s' % (len(message), block_size, encrypted_content)
    fo = open(message_file, 'w')
    fo.write(encrypted_content)
    return encrypted_content


def read_from_file_decrypt(message_file, key_file_name):
    key_size, n, d = read_key_file(key_file_name)

    fo = open(message_file)
    content = fo.read()
    print("Split content:", content.strip().split(';'))
    message_length, block_size, encrypted_message = content.strip().split(';')
    message_length = int(message_length)
    block_size = int(block_size)

    if not (math.log(2 ** key_size, len(SYMBOLS)) >= block_size):
        sys.exit('Error - Block size is too large for key and symbol set size')

    encrypted_blocks = []
    for block in encrypted_message.split(','):
        encrypted_blocks.append(int(block))

    return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)


if __name__ == '__main__':
    main()
