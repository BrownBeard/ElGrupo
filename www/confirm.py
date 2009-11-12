#!/usr/bin/env python

import random, hashlib
import cgi
import MySQLdb
import Cookie
import sys, os
import cgitb; cgitb.enable()

import ElGrupo

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()

  form = cgi.FieldStorage()
  name = form.getfirst('name', '')
  gs.name = name
  passwd = form.getfirst('passwd', '')

  rows = gs.db.sqlReturn( \
      'select u_id from users where name = %s and passwd_hash = "%s";' % \
      (MySQLdb.string_literal(name), hashlib.sha256(passwd).hexdigest()))
  if len(rows) != 1:
    gs.printHeader('Login failed.')
    print '<h1 class="login">Login failed.</h1>'
    gs.printFooter('Login failed.')
    sys.exit(0)

  u_id = rows[0][0]
  gs.u_id = u_id
  secret = hashlib.sha256(str(random.random())).hexdigest()
  gs.db.sql('insert into sessions (secret, u_id) values ("%s", %d);' % \
      (secret, u_id))
  c = Cookie.SimpleCookie()
  c['secret'] = secret

  gs.printHeader('Thanks', cookie=c)
  print '<h1 class="login">Login succeeded.</h1>'
  gs.printFooter('Thanks')

  gs.db.disconnect()

main()
