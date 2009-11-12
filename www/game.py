#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb

import ElGrupo

def printq(game, filename):
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()
  gs.game_name = game
  q = gs.getRandQuestion(game)

  # Make sure table has a row for me
  rows = gs.db.sqlReturn( \
  'select n_correct, n_total from normal_scores where u_id = %d and g_id = %d;' \
  % (gs.u_id, gs.g_id))
  if len(rows) == 0:
    gs.db.sql('insert into normal_scores (u_id, g_id, n_correct, n_total) values (%d,%d,%d,%d);' % (gs.u_id, gs.g_id, 0, 0))
    n_correct = 0
    n_total = 0
  else:
    n_correct = rows[0][0]
    n_total = rows[0][1]

  # Figure out correctness
  form = cgi.FieldStorage()
  last_answer = form.getvalue('answer')
  correct = None
  if last_answer:
    sep = last_answer.find('-')
    last_q_id = int(last_answer[:sep])
    last_string = last_answer[sep+1:]
    rows = gs.db.sqlReturn(
        'select correct from answers where q_id=%d and answer=%s;' % \
            (last_q_id, MySQLdb.string_literal(last_string)))
    if len(rows) == 1:
      if rows[0][0] == 1:
        correct = True
        gs.db.sql('''\
update normal_scores set n_correct=n_correct+1, n_total=n_total+1 where u_id=%d and g_id=%d;'''
        % (gs.u_id, gs.g_id))
      else:
        correct = False
        gs.db.sql('''\
update normal_scores set n_total=n_total+1 where u_id=%d and g_id=%d;'''
        % (gs.u_id, gs.g_id))

  rows = gs.db.sqlReturn( \
  'select n_correct, n_total from normal_scores where u_id = %d and g_id = %d;' \
  % (gs.u_id, gs.g_id))
  n_correct = rows[0][0]
  n_total = rows[0][1]

  # Print info
  gs.printHeader(game)
  print '<h1 class="question">%s</h1><br />' % (q.string)
  print '<div class="question_bar">&nbsp;</div><br />'
  print '<div class="question_form">'
  print '<table width="520px">'
  print '<form action="%s" method="get">' % filename
  spot = int((len(q.answers) + 1) / 2)
  i = 0
  for a in q.answers:
    print '<tr>'
    print '<td>'
    print '<input type="radio" name="answer" value="%d-%s">%s</input><br />' \
        % (q.q_id, a.string, a.string)
    print '</td>'
    print '<td align="right">'
    if i == spot-1:
      print n_correct, '/', n_total
    elif i == spot and not correct is None:
      if correct: print 'Correct!'
      else: print 'Incorrect!'
    print '</td>'
    print '</tr>'
    i += 1
  print '<tr><td><input type="submit" value="Choose" /></td><td></td></tr>'
  print '</form></table></div><br />'
  print '<div class="question_bar">&nbsp;</div><br />'

  gs.printFooter(game)
  gs.db.disconnect()
