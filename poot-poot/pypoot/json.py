#!/usr/bin/env python
"""json utilities"""

def ify(thing):
    """attempt to turn an arbitrary python thing into valid JSON"""

    json = ""

    if (thing == None):
        json = 'null'
    elif (isinstance(thing, bool)):
        if thing:
            json = 'true'
        else:
            json = 'false'
    elif (isinstance(thing, basestring)):
        thing = thing.replace('"', '\\"')
        thing = thing.replace("\n", '\\n')
        thing = thing.replace("\r", '\\r')
        json = '"' + thing + '"'
    elif (isinstance(thing, int)) or (isinstance(thing, long)):
        json = str(thing)
    elif (isinstance(thing, dict)):
        ## string dictionary to json...
        first = 1
        json += "{"
        for key, value in thing.iteritems():
            if not first:
                json += ","
            json += "\"%s\":%s" % (key, ify(value))
            first = 0
        json += "}"
    elif (isinstance(thing, list)):
        first = 1
        json += "["
        for element in thing:
            if not first:
                json += ","
            json += ify(element)
            first = 0
        json += "]"
    else:
        raise Exception("I have no idea what to do with %s..." % str(thing))
    return json
