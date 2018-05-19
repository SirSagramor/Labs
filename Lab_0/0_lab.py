alphabet = list("abcdefghijklmnopqrstuvwxyz")
matrix = []
for i in range(len(alphabet)):
    matrix.append(alphabet[i:] + alphabet[:i])

def encode(message, key):
    message = [i for i in message.lower() if i in alphabet]
    key = (key * (len(message) // len(key) + 1))[:len(message)]
    result = ""
    # for i in range(len(message)):
        # result += alphabet[(alphabet.index(message[i]) + alphabet.index(key[i]))%26]
    for i in range(len(message)):
        result += matrix[alphabet.index(message[i])][alphabet.index(key[i])]
    return result
print(encode("The quick brown fox jumped over the lazy dog", "key"))
