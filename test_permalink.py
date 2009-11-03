#!/usr/bin/env python

import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

## import from the app
from pypoot import permalink

PHRASE_TO_LINK = {
    u'The Original Poot':                             'original-poot',
    u'Obfuscated C Poot':                             'obfuscated-c-poot',
    u'Model Poot II':                                 'model-poot-ii',
    u'P*O*O*T':                                       'p-o-o-t',
    u'McPoot\'s':                                     'mcpoot-s',
    u'Happy Poot':                                    'happy-poot',
    u'Poot 911':                                      'poot-911',
    u'Warhol Poot':                                   'warhol-poot',
    u'Ultra Poot':                                    'ultra-poot',
    u'Poot Translation Table':                        'poot-translation-table',
    u'Black Beast Poots':                             'black-beast-poots',
    u'Chalk Poot':                                    'chalk-poot',
    u'The Wrath of Poot!':                            'wrath-of-poot',
    u'Picasso Poot':                                  'picasso-poot',
    u'Poot Flowers':                                  'poot-flowers',
    u'Adopt a Poot':                                  'adopt-a-poot',
    u'Our First Poot':                                'our-first-poot',
    u'What is poot?':                                 'what-is-poot',
    u'Pootpoot.com is on crack':                      'pootpoot-com-is-on-crack',
    u'KittyPoot 2':                                   'kittypoot-2',
    u'The evil truth behind poot...':                 'evil-truth-behind-poot',
    u'RMS Poot':                                      'rms-poot',
    u'The BEST Game!':                                'best-game',
    u'"Why", "Will to Live" and "I Think"':           'why-will-to-live-and-i-think',
    u'Nasdaq:POOT':                                   'nasdaq-poot',
    u'Duh POOT- POOT.':                               'duh-poot-poot',
    u'Obfuscated C Poot 2':                           'obfuscated-c-poot-2',
    u'My favorite subatomic particle':                'favorite-subatomic-particle',
    u'Untitled':                                      'untitled',
    u'Epicurius\' Argument Against the Evil of Poot': 'epicurius-argument-against-the-evil-of-poot',
    u'What ever happened to Chicken Little?':         'what-ever-happened-to-chicken-little',
    u'Shadow poots too!':                             'shadow-poots-too',
    u'Pootle':                                        'pootle',
    u'Splash Mountain Poot':                          'splash-mountain-poot',
    u'Pooto':                                         'pooto',
    u'Poot Soliloquy':                                'poot-soliloquy',
    u'Sunday Fun':                                    'sunday-fun',
    u'Everquest Poot':                                'everquest-poot',
    u'Think Poot sticker design':                     'think-poot-sticker-design',
    u'Poot Xing sticker design':                      'poot-xing-sticker-design',
    u'Swirld shirt design':                           'swirld-shirt-design',
}

class TestPerma(unittest.TestCase):
    def test(self):
        for phrase, link in PHRASE_TO_LINK.iteritems():
            g = permalink.phrase_link_generator(phrase)
            self.assertEquals(g.next(), link)
            self.assertEquals(g.next(), link + '-1')
            self.assertEquals(g.next(), link + '-2')
