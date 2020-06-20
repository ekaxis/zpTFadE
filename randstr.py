'''
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

by mopx
'''

"""
função para gerar strings aleatórias
"""

import string
import random

# Ex. output: o_uYGxl$@HBEsCx&q$_NL!HdVTFqOnfQ
def k():
    u = ''
    for i in range(32):
        l = string.ascii_lowercase+'_@#$&*!'+string.ascii_uppercase
        u+=l[random.randint(0, len(l)-1)]
    return u

# Ex. output: dndirm
def k():
    u = ''
    for i in range(6):
        l = string.ascii_lowercase
        u+=l[random.randint(0, len(l)-1)]
    return u