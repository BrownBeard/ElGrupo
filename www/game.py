#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import math

import ElGrupo

# normal {{{
def normal(gs, form, filename):
  q = gs.getRandQuestion(gs.game_name)

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
  gs.printHeader(gs.game_name + '-Normal')
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

  gs.printFooter(gs.game_name + '-Normal')
  gs.db.disconnect()
# }}}

# sprint {{{
def sprint(gs, form, filename):
  q = gs.getRandQuestion(gs.game_name)

  # Is a game running?
  ss_rows = gs.db.sqlReturn(
  'select ss_id, n_correct, n_total, time_to_sec(timediff(started + interval 3 minute, now())) from sprint_scores where ' +
  'u_id = %d and g_id = %d and started + interval 3 minute > now() and lost=0;' %
  (gs.u_id, gs.g_id))
  if len(ss_rows) == 0:
    # Is it time to do the action now?
    startone = form.getvalue('startone')
    if startone == 'yes':
      # Get a game going
      gs.db.sql('insert into sprint_scores (u_id, g_id) values (%d, %d);' %
          (gs.u_id, gs.g_id))
      sprint(gs, form, filename) # Now, there's a row, so no deep recursion
    else:
      # Need to review a finished game?
      rows = gs.db.sqlReturn(
      'select n_correct, n_total, ss_id from sprint_scores where ' +
      'reviewed = 0 and u_id = %d and g_id = %d;' % (gs.u_id, gs.g_id))
      if len(rows) == 0:
        # Give dialog
        gs.printHeader(gs.game_name + '-Sprint  (New Game)')
        print '<form action="%s" method="post">' % (filename)
        print '<input type="hidden" name="startone" value="yes" />'
        print '<input type="hidden" name="m" value="s" />'
        print '<input type="submit" value="New game" />'
        print '</form>'
        gs.printFooter(gs.game_name + '-Sprint  (New Game)')
      else:
        # Print summary
        gs.printHeader(gs.game_name + '-Sprint  (Review)')
        print '<h1 class="login">Good job.  Your score is %d/%d.</h1>' % \
            (rows[0][0], rows[0][1])
        gs.printFooter(gs.game_name + '-Sprint  (Review)')

        # Now it is reviewed
        gs.db.sql('update sprint_scores set reviewed=1 where ss_id=%d;' %
            rows[0][2])
  else:
    # Present a question
    ss_id = ss_rows[0][0]
    n_correct = ss_rows[0][1]
    n_total = ss_rows[0][2]
    t_left = ss_rows[0][3]

    # Time to quit?
    quit = form.getvalue('quit')
    if quit == 'yes':
      gs.db.sql('update sprint_scores set lost=1 where ss_id=%d' % ss_id)
      sprint(gs, form, filename)
      return
    # Figure out correctness
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
        n_total += 1
        if rows[0][0] == 1:
          correct = True
          n_correct += 1
          gs.db.sql('''\
  update sprint_scores set n_correct=n_correct+1, n_total=n_total+1 where ss_id=%d;'''
          % ss_id)
        else:
          correct = False
          gs.db.sql('''\
  update sprint_scores set n_total=n_total+1 where ss_id=%d;'''
          % ss_id)

    # Print info
    gs.printHeader(gs.game_name + '-Sprint')
    print '<h1 class="question">%s</h1><br />' % (q.string)
    print '<div class="question_bar">&nbsp;</div><br />'
    print '<div class="question_form">'
    print '<table width="520px">'
    print '<form action="%s" method="post">' % filename
    spot = int((len(q.answers) + 1) / 2)
    i = 0
    for a in q.answers:
      print '<tr>'
      print '<td>'
      print '<input type="radio" name="answer" value="%d-%s">%s</input><br />' \
          % (q.q_id, a.string, a.string)
      print '</td>'
      print '<td align="right">'
      if i == 0:
        print '<span style="color:red">' + str(t_left) + 's remaining</span>'
      if i == spot-1:
        print n_correct, '/', n_total
      elif i == spot and not correct is None:
        if correct: print 'Correct!'
        else: print 'Incorrect!'
      print '</td>'
      print '</tr>'
      i += 1
    print '<tr><td><input type="submit" value="Choose" />'
    print '</td><td align="right"><a href="%s?m=s&quit=yes">Quit</a></td></tr>'\
        % filename
    print '<input type="hidden" name="m" value="s">'
    print '</form></table></div><br />'
    print '<div class="question_bar">&nbsp;</div><br />'

    gs.printFooter(gs.game_name+'-Sprint')
    gs.db.disconnect()
# }}}

# marathon {{{
def marathon(gs, form, filename):
  q = gs.getRandQuestion(gs.game_name)

  # Is a game running?
  ms_rows = gs.db.sqlReturn(
  'select ms_id, n_correct, t_left from marathon_scores where u_id = %d and g_id = %d and t_prev + interval t_left second > now() and lost=0;' %
  (gs.u_id, gs.g_id))
  if len(ms_rows) == 0:
    # Is it time to do the action now?
    startone = form.getvalue('startone')
    if startone == 'yes':
      # Get a game going
      gs.db.sql('insert into marathon_scores (u_id, g_id, t_left) ' +
                'values (%d, %d, %d);' % (gs.u_id, gs.g_id, 100))
      marathon(gs, form, filename) # Now, there's a row, so no deep recursion
    else:
      # Need to review a finished game?
      rows = gs.db.sqlReturn(
      'select n_correct, ms_id from marathon_scores where ' +
      'reviewed = 0 and u_id = %d and g_id = %d;' % (gs.u_id, gs.g_id))
      if len(rows) == 0:
        # Give dialog
        gs.printHeader(gs.game_name + '-Marathon  (New Game)')
        print '<form action="%s" method="post">' % (filename)
        print '<input type="hidden" name="startone" value="yes" />'
        print '<input type="hidden" name="m" value="m" />'
        print '<input type="submit" value="New game" />'
        print '</form>'
        gs.printFooter(gs.game_name + '-Marathon  (New Game)')
      else:
        # Print summary
        gs.printHeader(gs.game_name + '-Marathon  (Review)')
        print '<h1 class="login">Good job.  Your score is %d.</h1>' % \
            (rows[0][0])
        gs.printFooter(gs.game_name + '-Marathon  (Review)')

        # Now it is reviewed
        gs.db.sql('update marathon_scores set reviewed=1 where ms_id=%d;' %
            rows[0][1])
  else:
    # Present a question
    ms_id = ms_rows[0][0]
    n_correct = ms_rows[0][1]
    t_left = ms_rows[0][2]

    # Time to quit?
    quit = form.getvalue('quit')
    if quit == 'yes':
      gs.db.sql('update marathon_scores set lost=1 where ms_id=%d' % ms_id)
      marathon(gs, form, filename)
      return
    # Figure out correctness
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
          n_correct += 1
          t_left = math.ceil(0.85 * t_left)
          gs.db.sql(
          'update marathon_scores set n_correct=n_correct+1, t_prev=now(), '
          't_left=%d where ms_id=%d;' % (t_left, ms_id)
          )
        else:
          # Lose the game
          correct = False
          gs.db.sql('update marathon_scores set lost=1 where ms_id=%d;' % ms_id)
          marathon(gs, form, filename)
          return

    # Print info
    gs.printHeader(gs.game_name+'-Marathon')
    print '<h1 class="question">%s</h1><br />' % (q.string)
    print '<div class="question_bar">&nbsp;</div><br />'
    print '<div class="question_form">'
    print '<table width="520px">'
    print '<form action="%s" method="post">' % filename
    spot = int((len(q.answers) + 1) / 2)
    i = 0
    for a in q.answers:
      print '<tr>'
      print '<td>'
      print '<input type="radio" name="answer" value="%d-%s">%s</input><br />' \
          % (q.q_id, a.string, a.string)
      print '</td>'
      print '<td align="right">'
      if i == 0:
        print '<span style="color:red">' + str(t_left) + 's round</span>'
      if i == spot-1:
        print n_correct
      elif i == spot and not correct is None:
        if correct: print 'Correct!'
        else: print 'Incorrect!'
      print '</td>'
      print '</tr>'
      i += 1
    print '<tr><td><input type="submit" value="Choose" />'
    print '</td><td align="right"><a href="%s?m=m&quit=yes">Quit</a></td></tr>'\
        % filename
    print '<input type="hidden" name="m" value="m">'
    print '</form></table></div><br />'
    print '<div class="question_bar">&nbsp;</div><br />'

    gs.printFooter(gs.game_name + '-Marathon')
    gs.db.disconnect()
# }}}

# printq {{{
def printq(game, filename):
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()
  gs.game_name = game

  # Dispatch correct function
  form = cgi.FieldStorage()
  mode = form.getvalue('m')
  if mode == 's':
    sprint(gs, form, filename)
  elif mode == 'm':
    marathon(gs, form, filename)
  else:
    normal(gs, form, filename)
# }}}
