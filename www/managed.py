#!/usr/bin/env python

import random, hashlib
import cgi
import MySQLdb
import Cookie
import sys, os
import cgitb; cgitb.enable()

import ElGrupo

def fail(gs, msg):
  gs.printHeader('Update Failed')
  print '<h1 class="login">Update Failed</h1>'
  print '<p>%s<br><a href="account.py">Retry</a></p>' % msg
  gs.printFooter('Update Failed')
  gs.db.disconnect()
  sys.exit(0)

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  # Get values
  form = cgi.FieldStorage()
  cur_passwd = form.getvalue('cur_passwd')
  email = form.getvalue('email')
  new_passwd = form.getvalue('new_passwd')
  new_confirm = form.getvalue('new_confirm')
  u_id = gs.loggedInAs()

  # Check current passwd
  if not cur_passwd: fail(gs, 'Must enter current password.')

  rows = gs.db.sqlReturn( \
      'select name from users where u_id = %d and passwd_hash = "%s";' % \
      (u_id, hashlib.sha256(cur_passwd).hexdigest()))
  if len(rows) != 1: fail(gs, 'Current password does not match.')

  # Make the changes
  if email: gs.db.sql('update users set email=%s where u_id=%d;' % \
                      (MySQLdb.string_literal(email), u_id))

  if new_passwd:
    if new_passwd == new_confirm:
      gs.db.sql('update users set passwd_hash=%s where u_id=%d;' % \
                (MySQLdb.string_literal(hashlib.sha256(new_passwd).hexdigest()),
                  u_id))
    else: fail(gs, 'Passwords do not match.')

  gs.printHeader('Thanks')
  print '<h1 class="login">Update succeeded.</h1>'
  gs.printFooter('Thanks')

  gs.db.disconnect()

main()
