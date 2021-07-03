#!/usr/bin/env python
from sys import argv
from Application.Parser import Parser
from Application.Experimenter import Experimenter


scrypt, uri, params = argv
if uri == 'parse':
    parser = Parser()
    print(parser.parse(params))
elif uri == 'experiment':
    experimenter = Experimenter()
    file = open(params)
    json = file.read()
    print(experimenter.handle(json))
