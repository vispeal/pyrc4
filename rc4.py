#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Copyright (C) 2016
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""


def ksa(key):
    key_length = len(key)
    s_box = range(256)

    j = 0
    for i in range(256):
        j = (j + s_box[i] + key[i % key_length]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]  # swap

    return s_box


def prga(s_box):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]  # swap
        t = s_box[(s_box[i] + s_box[j]) % 256]
        yield t


def rc4(plain_bytes, key):
    key = [ord(c) for c in key]
    s_box = ksa(key)
    key_stream = prga(s_box)

    cipher_bytes = []
    for c in plain_bytes:
        cipher_bytes.append(ord(c) ^ key_stream.next())

    return "".join([chr(x) for x in cipher_bytes])


def main():
    import json
    # wiki: http://en.wikipedia.org/wiki/RC4

    key = 'Key'
    data = {
        "name": u"大战神",
        "level": 1
    }

    plaintext = json.dumps(data)
    print plaintext

    # encrypt
    cipher_bytes = rc4(plaintext, key)

    print cipher_bytes

    # decrypt
    text = rc4(cipher_bytes, key)

    data = json.loads(text)
    print data["name"]

if __name__ == '__main__':
    main()
