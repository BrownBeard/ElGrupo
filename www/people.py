#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb

import ElGrupo

def main():
  title='People'
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  gs.printHeader(title)
  people = gs.getPeople()
  print '<h1 class="login">People:</h1>'
  print '<ul>'
  for p in people:
    print '<li>'
    print '<strong><a href="person.py?p=%s">%s</a></strong>' % (p.string, p.string)
    rows = gs.db.sqlReturn('select stat, value from stats where p_id=%d;'%p.p_id)
    print '<table>'
    sum = 0
    for row in rows:
      print '<tr>'
      print '<td>%s:</td><td align="right">%2.1f</td>' % (row[0], row[1])
      print '</tr>'
      sum += row[1]
    avg = sum / len(rows)
    print '<tr>'
    print '<td><strong>Total:</strong></td><td align="right"><strong>%2.1f</strong></td>' % avg
    print '</tr>'
    print '</li>'
  print '</ul>'
  gs.printFooter(title)
  gs.db.disconnect()

if __name__ == '__main__': main()
