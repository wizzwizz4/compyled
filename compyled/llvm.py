# This file is part of compyled.

import struct

class LLVM:
    """An incomplete LLVM bytecode generator.

    Implements the subset I need, and no more.
    """

    def __init__(self):
        pass

    @staticmethod
    def represent_int_vbr(i, signed):
        """Returns the LLVM representation of an integer.
        
        The caller is responsible for ensuring that the integer is in range.
        """
        if signed:
            if i < 0:
                i = (~i << 1) | 1
            else:
                i <<= 1

        l = []
        while i:
            l.append((i & 127) | 128)
            i >>= 7
        if not l:
            l.append(0)
        l[-1] &= 127
        return bytes(l)

    @staticmethod
    def represent_float(f):
        return struct.pack("<f", f)

    @staticmethod
    def represent_double(d):
        return struct.pack("<d", d)

    @classmethod
    def represent_llist(cls, type_representer, l):
        if len(l) > 0xffff:
            raise ValueError("l is too long")

        b = []
        b.append(cls.represent_int_vbr(len(l), False))
        for item in l:
            b.append(type_representer(item))
        return b"".join(b)

    @classmethod
    def represent_zlist(cls, type_representer, l):
        if any(item == 0 for item in l):
            raise ValueError("an item is 0")

        b = []
        for item in l:
            b.append(type_representer(item))
        b.append(cls.represent_int_vbr(0, False))
        return b"".join(b)

    @staticmethod
    def represent_block(typecode, data):
        if len(data) >= (1 << 27):
            raise ValueError("data is too big")
        return represent_int_vbr(len(data) << 5 & typecode, False) + data
