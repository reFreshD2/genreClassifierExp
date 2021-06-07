#!/usr/bin/env python
from sys import argv
from Application.Parser import Parser

scrypt, uri, params = argv
if uri == 'parse':
    parser = Parser()
    print(Parser.parse(parser, params))
