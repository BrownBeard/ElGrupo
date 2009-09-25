#!/usr/bin/python

import sys

import ElGrupo

def main():
  # Set filename
  filename = 'conf.txt'
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  # Load it
  gs = ElGrupo.Session(filename)

  # Print info
  print 'host: %s' % (gs.dbinfo.host)
  print 'db: %s' % (gs.dbinfo.db)
  print 'user: %s' % (gs.dbinfo.user)
  print 'passwd: %s' % (gs.dbinfo.passwd)

if __name__ == '__main__':
  main()
