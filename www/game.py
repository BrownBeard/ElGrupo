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

  # Print info
  gs.printHeader()
  print '<h1>Questions:</h1>\n<hr />\n<ul>'
  for q in qs:
    print '<li>', q.string, '</li>'
    print '<ul>'
    for a in q.answers:
      print '<li>',
      print a.string,
      if a.correct: print '(correct)', '</li>'
      else:         print '(incorrect)', '</li>'
    print '</ul>'
  print '</ul>'
  gs.printFooter()
  gs.db.disconnect()

def printq(game):
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  q = gs.getRandQuestion(game)

  # Print info
  gs.printHeader()
  print '<h1>%s</h1>\n<hr />' % (q.string)
  print '<ul>'
  for a in q.answers:
    if a.correct: print '<li>%s *</li>' % (a.string)
    else: print '<li>%s</li>' % (a.string)
  print '</ul>'
  gs.printFooter()
  gs.db.disconnect()
