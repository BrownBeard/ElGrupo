#!/usr/bin/python

import sys

import ElGrupo

def main():
  # Set filenames
  conffilename = 'conf.txt'
  if len(sys.argv) > 1:
    conffilename = sys.argv[1]
  qsfilename = 'qs.txt'
  if len(sys.argv) > 2:
    qsfilename = sys.argv[2]

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.readQuestions(qsfilename)
  gs.db.disconnect()

  # Print info
  pass

if __name__ == '__main__':
  main()
