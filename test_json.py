#!/usr/bin/env python

import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

## import from the app
from pypoot import json

class TestJsonify(unittest.TestCase):
    def test(self):
        j = json.ify([])
        self.assertEquals(j, '[]')
        j = json.ify({})
        self.assertEquals(j, '{}')
        j = json.ify([{'a':'b'}])
        self.assertEquals(j, '[{"a":"b"}]')
        j = json.ify([{'a':'b'}, {'c':'d'}])
        self.assertEquals(j, '[{"a":"b"},{"c":"d"}]')
        j = json.ify({'a':'b'})
        self.assertEquals(j, '{"a":"b"}')
        j = json.ify({'a':'b"'})
        self.assertEquals(j, '{"a":"b\\""}')
        j = json.ify({'a':1})
        self.assertEquals(j, '{"a":1}')

if __name__ == '__main__':
    unittest.main()
