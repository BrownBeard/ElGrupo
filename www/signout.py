#!/usr/bin/env python

import random, hashlib
import cgi
import cgitb; cgitb.enable()
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

  cookie_string = os.environ.get('HTTP_COOKIE')

  if not cookie_string: return None

  cookie = Cookie.SimpleCookie()
  cookie.load(cookie_string)
  try:
    secret = cookie['secret'].value
  except:
    return None

  gs.db.sql('delete from sessions where secret = %s;' % \
      MySQLdb.string_literal(secret))

  # Delete the cookie from user's browsing
  cookie['secret']['expires'] = 'Sun, 18-Oct-2009 10:00:00 GMT'
  gs.accountCheck(force_cookie=cookie)

main()
