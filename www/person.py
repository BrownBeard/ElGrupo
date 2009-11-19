#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb

import ElGrupo

# main {{{
def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  p = ElGrupo.Person()
  form = cgi.FieldStorage()
  p.name = form.getvalue('p')

  # Find person info
  rows = gs.db.sqlReturn('select p_id, birthday from persons where ' +
      'name = %s and u_id = %d' % (MySQLdb.string_literal(p.name), gs.u_id))
  if len(rows) == 0:
    gs.printHeader()
    print '<h1 class="login">You have no person named %s.</h1>' % (cgi.escape(p.name))
    gs.printFooter()
    gs.db.disconnect()
    return
  p.p_id, p.birthday = rows[0]

  # Find stat info
  spend = form.getvalue('spend')
  spend_spot = None
  rows = gs.db.sqlReturn('select stat, value from stats where p_id=%d' % p.p_id)
  i = 0
  sum = 0
  for row in rows:
    s = ElGrupo.Stat()
    s.string, s.value = row
    sum += float(s.value)
    if spend == s.string:
      spend_spot = i
    p.stats.append(s)
    i += 1

  # Do we need to up a stat?
  if spend:
    rows = gs.db.sqlReturn(
    'select stat_id from stats where p_id=%d and stat=%s and value<100;'\
    % (p.p_id, MySQLdb.string_literal(spend)))
    if len(rows) > 0 and spend_spot is not None and p.stats[spend_spot].value < 100:
      stat_id = rows[0][0]
      rows = gs.db.sqlReturn('select points from users where u_id=%d'\
          % gs.u_id)
      if rows[0][0] >= 100:
        gs.db.sql('update users set points=points-100 where u_id=%d'\
            % gs.u_id)
        p.stats[spend_spot].value = min(p.stats[spend_spot].value+20, 100)
        gs.db.sql('update stats set value=%f where stat_id=%d'\
            % (p.stats[spend_spot].value, stat_id))

  gs.printHeader(p.name)
  print '<h1 class="login">%s, born on %s.</h1>' % (p.name, str(p.birthday))
  print '<table width="300px">'
  for stat in p.stats:
    print '<tr>'
    print '<td>%s:</td><td align="right">%2.1f</td>' % (stat.string, stat.value)
    print '<td align="right">'
    print '<a href="person.py?p=%s&spend=%s">Spend' % (p.name, cgi.escape(stat.string))
    print '</a></td>'
    print '</tr>'
  print '<tr>'
  print '<td><strong>Total:</td>'
  print '<td align="right"><strong>%2.1f</strong></td><td />' % (sum/len(p.stats))
  print '</table>'
  print '<p><a href="delete.py?p=%s">Delete</a></p>' % p.name
  gs.printFooter(p.name)

  gs.db.disconnect()
# }}}

main()
