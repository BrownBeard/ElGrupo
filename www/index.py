#!/usr/bin/env python

import sys
import cgi
import cgitb; cgitb.enable()

import ElGrupo

def main():
  gs = ElGrupo.Session('/home/adam/ElGrupo/conf.txt')
  gs.db.connect()
  gs.accountCheck()
  gs.printHeader()
  print 'Welcome to El Grupo!'
  gs.printFooter()
  gs.db.disconnect()

if __name__ == '__main__':
  main()
