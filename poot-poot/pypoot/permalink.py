#!/usr/bin/env python
"""permalink utilities"""

import string

PREFIXES    = ['the', 'my', 'a']
TRANSLATORS = [
    dict((ord(char), u'-') for char in string.punctuation),
    dict((ord(char), u'-') for char in string.whitespace),
]

def phrase_link_generator(phrase):
    """returns a generator which creates 'permalink' URL-safe words
       derived from the input phrase"""

    ## smash case
    link = phrase.lower()

    ## convert non-
    for translator in TRANSLATORS:
        link = link.translate(translator)

    ## remove prefixes
    for prefix in PREFIXES:
        while link.startswith(prefix + '-'):
            link = link[(len(prefix)+1):len(link)]

    ## remove double-dashes
    while link.find('--') >= 0:
        link = link.replace('--', '-')

    ## remove leading & trailing dashes
    link = link.strip('-')
    yield link

    ## generate a sequence of derived links in case of collisions
    i = 0
    while True:
        i += 1
        yield link + '-' + str(i)
