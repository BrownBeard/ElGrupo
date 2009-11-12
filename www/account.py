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
