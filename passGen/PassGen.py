from random import randint, choice


def gen(mode):
    spacers = ["-", '_']
    specials = ['!', '#', '$', '%', '&', '(', ')', '*', '+',
                '.', '/', ':', ';', '=', '>', '?', '@', '[',
                ']', '^', '`', '{', '|', '}', '~', "'", '\\']
    if mode == 'numbers':
        return randint(0, 9)
    elif mode == 'upper':
        return chr(randint(65, 90))
    elif mode == 'lower':
        return chr(randint(97, 122))
    elif mode == 'spacers':
        return choice(spacers)
    elif mode == 'specials':
        return choice(specials)


def generate_passwords(length, mods, n=1):
    if n != 1:
        passwords = []
        for x in range(n):
            password = ''
            for i in range(length):
                md = choice(mods)
                password += str(gen(md))
            passwords.append(password)
        return passwords
    else:
        password = ''
        for i in range(length):
            md = choice(mods)
            password += str(gen(md))
        return password

print(generate_passwords(10, ["numbers", 'lower', 'upper'], 10))
