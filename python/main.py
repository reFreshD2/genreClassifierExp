#!/usr/bin/env python
from sys import argv
from Application.Parser import Parser
from Application.Experimenter import Experimenter


scrypt, uri, params = argv
if uri == 'parse':
    parser = Parser()
    print(Parser.parse(parser, params))
elif uri == 'experiment':
    experimenter = Experimenter()
    print(Experimenter.handle(experimenter, params))
