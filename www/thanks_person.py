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
  name = form.getvalue('name')

  rows = gs.db.sqlReturn('select p_id from persons where u_id=%d and name=%s'\
      % (gs.u_id, MySQLdb.string_literal(name)))
  if len(rows) != 0:
    gs.printHeader('Failure')
    print '<h1 class="login">You already have a person of that name.</h1>'
    gs.printFooter('Failure')
    gs.db.disconnect()
    return

  gs.db.sql('insert into persons (u_id, name, birthday) values (%d,%s,date(now()));' \
      % (gs.u_id, MySQLdb.string_literal(name)))
  rows = gs.db.sqlReturn('select p_id from persons where u_id=%d and name=%s;'\
      % (gs.u_id, MySQLdb.string_literal(name)))
  p_id = rows[0][0]
  for stat in ['Food', 'Drink', 'Happiness', 'Exercise']:
    gs.db.sql('insert into stats (p_id, stat, value) values (%d, %s, 0)' \
        % (p_id, MySQLdb.string_literal(stat)))

  gs.printHeader('Thanks')
  print '<h1 class="login">Thank you!</h1>'
  print '<p>A person has been created.  You can manipulate it on the left.</p>'
  gs.printFooter('Thanks')
  gs.db.disconnect()

main()
