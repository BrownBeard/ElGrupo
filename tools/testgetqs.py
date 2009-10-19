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
  qsv = gs.getQuestions('Vocabulary')
  qsg = gs.getQuestions('Geography')
  gs.db.disconnect()

  # Print info
  print 'vocab:'
  for q in qsv:
    print q.string
    for a in q.answers:
      print ' ',
      print a.string,
      if a.correct: print '(correct)'
      else:         print '(incorrect)'
  print 'geog:'
  for q in qsg:
    print q.string
    for a in q.answers:
      print ' ',
      print a.string,
      if a.correct: print '(correct)'
      else:         print '(incorrect)'

if __name__ == '__main__':
  main()
