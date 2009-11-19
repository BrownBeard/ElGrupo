#!/usr/bin/env python

import sys
import cgi
import MySQLdb

import ElGrupo

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  form = cgi.FieldStorage()
  name = form.getvalue('p')

  rows = gs.db.sqlReturn('select p_id from persons where u_id=%d and name=%s;'\
      % (gs.u_id, MySQLdb.string_literal(name)))
  if len(rows) == 0:
    gs.printHeader('Failure')
    print '<h1 class="login">You have noone of that name.</h1>'
    gs.printFooter('Failure')
    gs.db.disconnect()
    return
  for row in rows:
    gs.db.sql('delete from stats where p_id=%d;' % row[0])
  gs.db.sql('delete from persons where u_id=%d and name=%s;'\
      % (gs.u_id, MySQLdb.string_literal(name)))

  gs.printHeader('Deleted')
  print '<h1 class="login">%s Deleted.</h1>' % cgi.escape(name)
  gs.printFooter('Deleted')
  gs.db.disconnect()

main()
