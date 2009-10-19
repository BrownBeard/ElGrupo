#!/usr/bin/env python

import sys
import cgi
import random, hashlib
import smtplib

import ElGrupo

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()

  form = cgi.FieldStorage()
  name = cgi.escape(form.getfirst('name', ''))
  gs.name = None
  gs.printHeader('Thanks')
  email = cgi.escape(form.getfirst('email', ''))

  tmp_passwd = hashlib.md5(str(random.random())).hexdigest()[:8]
  passwd_hash = hashlib.sha256(tmp_passwd).hexdigest()

  smtpuser = 'elgruporice@gmail.com'
  smtppass = 'QsLgrup-o'
  SERVER = "smtp.gmail.com"
  FROM = "elgruporice@gmail.com"
  TO = [email] # must be a list
  SUBJECT = "El Grupo Account Confirmation"
  TEXT='Hello, %s!\n\nThanks for creating an account!  Your password is "%s".' \
      % (name, tmp_passwd)
  message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % \
      (FROM, ", ".join(TO), SUBJECT, TEXT)
  server = smtplib.SMTP(SERVER)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login(smtpuser, smtppass)
  server.sendmail(FROM, TO, message)

  gs.db.sql('insert into users (name, passwd_hash, email) values ("%s","%s","%s");' \
      % (name, passwd_hash, email))

  print '<h1 class="login">Thank you!</h1>'
  print '<p>An account has been created.  Your password will be emailed to you.</p>'
  gs.printFooter('Thanks')
  gs.db.disconnect()
  try: server.quit()
  except: pass

main()
