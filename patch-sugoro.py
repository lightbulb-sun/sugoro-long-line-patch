#!/usr/bin/python3

INPUT_FILENAME = 'english.nes'
OUTPUT_FILENAME = 'fixed.nes'
CHANGES_FILENAME = 'changes.txt'


DIGRAPHS = {
        "Fighter":  (0xe8,),
        "Ketbash":  (0xe9,),
        "t's":      (0x6e, 0x6f),
        "'s":       (0x5f,),
        "'l":       (0x58,),
        "'r":       (0x79,),
        "I'":       (0x5c,),
        "n'":       (0x70,),
        "'t":       (0x71,),
        }


CHARACTERS = {
        "-":        0x0a,
        "„":        0x0b,
        "*":        0x0f,
        "/":        0x10,
        ",":        0x2b,
        "?":        0x2c,
        "!":        0x2d,
        ".":        0x2e,
        "…":        0x2f,
        "“":        0x30,
        "c":        0x36,
        "j":        0x38,
        "h":        0x3a,
        "n":        0x3b,
        "g":        0x3d,
        "q":        0x3f,
        "w":        0x43,
        "k":        0x47,
        "+":        0x4a,
        "l":        0x4b,
        "d":        0x4d,
        "v":        0x53,
        "e":        0x54,
        "u":        0x56,
        "[":        0x59,
        "x":        0x5a,
        "f":        0x5b,
        "m":        0x5d,
        "p":        0x5e,
        "t":        0x62,
        "]":        0x69,
        "°":        0x6a,
        "i":        0x72,
        "z":        0x73,
        "o":        0x74,
        "y":        0x75,
        "r":        0x76,
        "m":        0x77,
        "a":        0x78,
        "F":        0x7a,
        "b":        0x7b,
        "h":        0x7d,
        "”":        0x7e,
        "t":        0x7f,
        "©":        0x80,
        "s":        0x83,
        "·":        0x84,
        " ":        0xfd,
        "\n":       0xfe,
        }


def convert_character(c):
    if ord('A') <= ord(c) <= ord('Z'):
        return 0x11 + ord(c) - ord('A')
    if ord('0') <= ord(c) <= ord('9'):
        return ord(c) - ord('0')
    return CHARACTERS[c]


def contains(lst, x):
    length = len(x)
    for n in range(len(lst)-length):
        if lst[n:n+length] == x:
            return n
    return None


def replace(lst, offset, length, x):
    return lst[:offset] + [x] + lst[offset+length:]


def replace_bytes(lst, offset, x):
    return lst[:offset] + x + lst[offset+len(x):]


def replace_digraphs(lst):
    for x in DIGRAPHS:
        cur = contains(lst, list(x))
        if cur is not None:
            lst = replace(lst, cur, len(x), DIGRAPHS[x])
    return lst


def flatten(lst):
    return [x for elem in lst for x in elem]


def convert_string(s):
    lst = replace_digraphs(list(s))
    for n, elem in enumerate(lst):
        try:
            c = convert_character(elem)
            lst = replace(lst, n, 1, (c,))
        except TypeError:
            pass
    return bytearray(flatten(lst))


def load_changes(filename):
    with open(filename, 'rb') as inf:
        data = inf.read().strip()

    result = []
    for elem in data.split(b'\n\n'):
        lines = elem.split(b'\n')
        offset = int(lines[0], 16)
        s = b'\n'.join(lines[1:]).decode('utf-8')
        result.append((offset, s))

    return result


def main():
    with open(INPUT_FILENAME, 'rb') as inf:
        rom = bytearray(inf.read())

    for offset, s in load_changes(CHANGES_FILENAME):
        rom = replace_bytes(rom, offset, convert_string(s))

    with open(OUTPUT_FILENAME, 'wb') as outf:
        outf.write(rom)


if __name__ == '__main__':
    main()
