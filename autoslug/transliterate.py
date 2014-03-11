# -*- coding: utf8 -*-
"""
Extends
http://effbot.org/zone/unicode-convert.htm
"""

import sys
import re
import unicodedata

from urllib import unquote_plus


CHAR_REPLACEMENT = {
    u'\N{Latin capital letter AE}': u'AE',
    u'\N{Latin small letter ae}': u'ae',
    u'\N{Latin capital letter Eth}': u'Dh',
    u'\N{Latin small letter eth}': u'dh',
    u'\N{Latin capital letter O with stroke}': u'Oe',
    u'\N{Latin small letter o with stroke}': u'oe',
    u'\N{Latin capital letter Thorn}': u'Th',
    u'\N{Latin small letter thorn}': u'th',
    u'\N{Latin small letter sharp s}': u'ss',
    u'\N{Latin capital letter D with stroke}': u'Dj',
    u'\N{Latin small letter d with stroke}': u'dj',
    u'\N{Latin capital letter H with stroke}': u'H',
    u'\N{Latin small letter h with stroke}': u'h',
    u'\N{Latin small letter dotless i}': u'i',
    u'\N{Latin small letter kra}': u'q',
    u'\N{Latin capital letter L with stroke}': u'L',
    u'\N{Latin small letter l with stroke}': u'l',
    u'\N{Latin capital letter Eng}': u'Ng',
    u'\N{Latin small letter eng}': u'ng',
    u'\N{Latin capital ligature OE}': u'Oe',
    u'\N{Latin small ligature oe}': u'oe',
    u'\N{Latin capital letter T with stroke}': u'Th',
    u'\N{Latin small letter t with stroke}': u'th',
    u'\u2019': u"'",
    u'\u201c': u'"',
    u'\u201d': u'"'
}


SPACE_RE = re.compile('\s+')


class unaccented_map(dict):

    ##
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    
    def mapchar(self, key):
        if key in self:
            return self[key]
        de = unicodedata.decomposition(unichr(key))
        if de:
            try:
                ch = int(de.split(None, 1)[0], 16)
            except (IndexError, ValueError):
                ch = key
        else:
            ch = CHAR_REPLACEMENT.get(unichr(key), key)
        if ch  == 32: # space
            pass
        elif 47 < ch < 58: # digits
            pass
        elif 64 < ch < 91: # uppercase
            pass
        elif 96 < ch < 123: # lowercase
            pass
        elif 127 < ch < 165: # upper ascii latin1
            pass
        elif ch == 9: # map tab to space
            ch = 32
        elif ch < 128: # reject invalid lower ascii
            ch = None
        elif ch in (152, 158) or ch < 256:
            ch = None
        self[key] = ch
        return ch

    if sys.version >= "2.5":
        # use __missing__ where available
        __missing__ = mapchar
    else:
        # otherwise, use standard __getitem__ hook (this is slower,
        # since it's called for each character)
        __getitem__ = mapchar


def transliterate(s, charset='utf8', unquote=True, lower=True, squash_spaces='-', map=unaccented_map()):
    if not isinstance(s, basestring):
        return s
    if not isinstance(s, unicode):
        for c in set([charset] + ['utf8', 'iso-8859-15']):
            try:
                s = s.decode(c)
            except UnicodeDecodeError:
                continue
            else:
                break
    if not isinstance(s, unicode):
        return s
    if unquote:
        s = unquote_plus(s)
    if lower:
        s = s.lower()
    s = s.strip().translate(map).encode('ascii', 'ignore')
    if squash_spaces:
        return SPACE_RE.sub(squash_spaces, s)
    return s

        
if __name__ == "__main__":
    TESTS = (
        {'s':'terza Et\xe0'},
        {'s':'terza%20Et\xe0'},
        {'s':'terza\tEt\xe0?!$#'},
        {'s':'terza%20Et\xe0', 'unquote':False},
        {'s':'terza Et\xe0', 'lower':False},
        {'s':'terza%20Et\xe0', 'squash_spaces':False},
    )
    padding = max(len(repr(t)) for t in TESTS)
    for t in TESTS:
        print repr(t).ljust(padding+1), transliterate(**t)
