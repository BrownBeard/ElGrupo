#!/usr/bin/python

import sys

import ElGrupo

def printqs(game):
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  qs = gs.getQuestions(game)
  gs.db.disconnect()

  # Print info
  print 'Questions:\n<ul>'
  for q in qs:
    print '<li>', q.string
    print '<ul>'
    for a in q.answers:
      print '<li>',
      print a.string,
      if a.correct: print '(correct)'
      else:         print '(incorrect)'
    print '</ul>'
  print '</ul>'
