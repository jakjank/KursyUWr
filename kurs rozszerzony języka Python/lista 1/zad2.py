def is_palindrom(text):
    z_lewej = ""
    z_prawej = ""
    for symbol in text:
        if symbol.isalpha():
            z_lewej += symbol
            z_prawej = symbol + z_prawej
    return z_lewej.upper() == z_prawej.upper()

print(is_palindrom("Eine güldne, gute Tugend: Lüge nie!"))