#xstrings.py
Similar to the famous [GNU binutils](http://www.gnu.org/software/binutils/)' strings command line utility, xstrings is used for emitting printable strings in files. Unlike strings, xstrings is capable of detecting obfuscated strings hidden in files using simple encodings like bitwise XOR, bitwise rotate-right, bitwise shift-left, etc. which are fairly common among malwares.

By default, xstrings looks for sequences of all printable characters (i.e. alphanumeric, punctuation and whitespaces) using all available encoding methods. To reduce noise, the user may disable certain encoding methods or narrow down the printable characters set to a smaller subset.

xstrings may be empowered by [GNU grep](http://www.gnu.org/software/grep/) to locate certain obfuscated strings or patterns in files.

xstrings is inspired by [xorsearch](http://blog.didierstevens.com/programs/xorsearch) by Didier Stevens
