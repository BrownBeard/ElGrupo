#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb

import ElGrupo

def main():
  title='Arcade'
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  gs.printHeader(title)
  games = gs.getGames()
  print '<h1 class="login">Games:</h1>'
  print '<ul>'
  for g in games:
    print '<li>'
    print '<strong>%s</strong>' % g.string
    print '<ul>'
    # Normal
    print '<li><a href="%s?m=n">Normal</a><br />' % (g.filename)
    rows = gs.db.sqlReturn('select n_correct from normal_scores where u_id=%d and g_id=%d;' % (gs.u_id, g.g_id))
    if len(rows) > 0:
      print '<table>'
      print '<tr>'
      print '<td>Your score:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr><tr>'
      rows = gs.db.sqlReturn('select max(n_correct) from normal_scores where g_id=%d;' % g.g_id)
      print '<td>Top score:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr></table>'
    print '</li>'
    # Sprint
    print '<li><a href="%s?m=s">Sprint</a><br />' % (g.filename)
    rows = gs.db.sqlReturn('select max(n_correct) from sprint_scores where u_id=%d and g_id=%d;' % (gs.u_id, g.g_id))
    if len(rows) > 0 and rows[0][0]:
      print '<table>'
      print '<tr>'
      print '<td>Your best:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr><tr>'
      rows = gs.db.sqlReturn('select max(n_correct) from sprint_scores where g_id=%d;' % g.g_id)
      print '<td>Top score:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr></table>'
    print '</li>'
    # Marathon
    print '<li><a href="%s?m=m">Marathon</a><br />' % (g.filename)
    rows = gs.db.sqlReturn('select max(n_correct) from marathon_scores where u_id=%d and g_id=%d;' % (gs.u_id, g.g_id))
    if len(rows) > 0 and rows[0][0]:
      print '<table>'
      print '<tr>'
      print '<td>Your best:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr><tr>'
      rows = gs.db.sqlReturn('select max(n_correct) from marathon_scores where g_id=%d;' % g.g_id)
      print '<td>Top score:</td><td align="right">%d</td>' % rows[0][0]
      print '</tr></table>'
    print '</li>'
    print '</ul>'
  print '</ul>'
  gs.printFooter(title)
  gs.db.disconnect()

if __name__ == '__main__': main()
