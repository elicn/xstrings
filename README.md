Similar to the infamous GNU strings command line utility, xstrings is used fot emitting printable strings in files. Unlike strings, xstrings is capable of detecting obfuscated strings hidden in files using simple encodings like bitwise XOR, bitwise rotate-right, bitwise shift-left, etc. which is fairly common among malwares.

By default, xstrings looks for sequences of all printable characters (i.e. alphanumeric, punctuation and whitespaces) using all available encoding methods. To reduce noise, the user may disable certain encoding methods or set the printable characters set to be a certain subset of the printable characters set.

To locate certain obfuscated strings or patterns in files, xstrings is best used in conjunction with GNU grep.

xstrings is inspired by 'xorsearch' by didier stevens, http://blog.didierstevens.com/programs/xorsearch
