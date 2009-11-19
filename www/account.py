#!/usr/bin/python

import sys
import cgi
import cgitb; cgitb.enable()
import MySQLdb

import ElGrupo

def main():
  title='Account Management'
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  gs.printHeader(title)
  rows = gs.db.sqlReturn('select total_donation, last_donation, this_donation, points from users where u_id=%d;' % gs.u_id)
  total, last, this, points = rows[0]
  print '<h1 class="login">Statistics</h1>'
  print '<table>'
  print '<tr>'
  print '<td>Total donations:</td><td align="right">%d grains</td>' % total
  print '</tr>'
  print '<tr>'
  print '<td>Donated yesterday:</td><td align="right">%d grains</td>' % last
  print '</tr>'
  print '<tr>'
  print '<td>To be donated tonight:</td><td align="right">%d grains</td>' % this
  print '</tr>'
  print '<tr><td>&nbsp;</td><td>&nbsp;</td></tr>'
  print '<tr>'
  print '<td>Points:</td><td align="right">%d points</td>' % points
  print '</tr>'
  print '</table>'

  print '<h1 class="login">Account Management</h1>'
  print '<p>Enter values you want to change.'
  print 'Fields left blank will be unaltered.</p>'
  print '<p><span style="color:red">*</span> = always required</p>'
  print '<form action="managed.py" method="post">'
  print '<table width="520px">'
  print '<tr>'
  print '<td align="right"><span style="color:red">*</span> Current password:</td>'
  print '<td align="left"><input type="password" name="cur_passwd"></td>'
  print '</tr>'
  print '<tr>'
  print '<td align="right">Email:</td>'
  print '<td align="left"><input type="text" name="email"></td>'
  print '</tr>'
  print '<tr><td></td><td>'
  rows = gs.db.sqlReturn('select wants_email from users where u_id=%d;' % gs.u_id)
  if rows[0][0]:
    checked = ' checked'
  else:
    checked = ''
  print '<input type="checkbox" name="wantmail"%s>' % checked
  print 'Receive emails about donations'
  print '</input></td></tr>'
  print '<tr>'
  print '<td align="right">New password:</td>'
  print '<td align="left"><input type="password" name="new_passwd"></td>'
  print '</tr>'
  print '<tr>'
  print '<td align="right">Confirm new password:</td>'
  print '<td align="left"><input type="password" name="new_confirm"></td>'
  print '</tr>'
  print '<tr></td><td><td><input type="submit" value="Submit" /></td></tr>'
  print '</table>'
  gs.printFooter(title)
  gs.db.disconnect()

if __name__ == '__main__': main()
