#!/usr/bin/env python

import sys

import ElGrupo

def main():
  gs = ElGrupo.Session('/home/adam/ElGrupo/conf.txt')
  gs.db.connect()
  gs.printHeader()
  print 'Text!'
  gs.printFooter()
  gs.db.disconnect()

if __name__ == '__main__':
  main()
