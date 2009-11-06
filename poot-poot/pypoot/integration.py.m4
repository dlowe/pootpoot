#!/usr/bin/env python
"""integration points"""

INTEGRATIONS = {
m4_ifdef(`POOTPOOT_BITLY_KEY',   `"BITLY_KEY": "POOTPOOT_BITLY_KEY",')
m4_ifdef(`POOTPOOT_BITLY_LOGIN', `"BITLY_LOGIN": "POOTPOOT_BITLY_LOGIN",')
}
