#!/usr/bin/python

import sys

import ElGrupo

def main():
  # Set filenames
  conffilename = 'conf.txt'
  if len(sys.argv) > 1:
    conffilename = sys.argv[1]

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.db.sql('delete from sessions where activity + interval 30 minute < now();')
  gs.db.disconnect()

if __name__ == '__main__':
  main()
