# xstrings
print the strings of encoded printable characters in files

Similar to the infamous GNU strings command line utility, xstrings is used to emit printable strings in files. Unlike strings, xstrings is capable of detecting obfuscated printable strings hidden in filges using simple encodings like xor, ror, shl, etc.

Since this utility produces a lot of noise, it is best used in conjunction with grep.

This project is inspired by 'xorsearch' by didier stevens, http://blog.didierstevens.com/programs/xorsearch
