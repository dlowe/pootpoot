#!/usr/bin/env python

import sys
import unittest

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
        j = json.ify({'a':1L})
        self.assertEquals(j, '{"a":1}')
        j = json.ify({'a':None})
        self.assertEquals(j, '{"a":null}')
        j = json.ify({'a':True})
        self.assertEquals(j, '{"a":true}')
        j = json.ify({'a':False})
        self.assertEquals(j, '{"a":false}')
