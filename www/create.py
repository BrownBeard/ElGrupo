#!/usr/bin/env python

import sys

import ElGrupo

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.name = None
  gs.db.connect()

  gs.printHeader('Create an Account')
  print '<h1 class="login">Enter your information.  All fields are requried.</h1>'
  print '<p>Your password will be emailed to you, so ensure that you will get it.</p>'
  print '<form action="thanks.py" method="get">'
  print '<table>'
  print '<tr>'
  print '<td align="right"><label for="nameid">Name</label></td>'
  print '<td><input type="text" name="name" id="nameid"></td>'
  print '</tr>'
  print '<tr>'
  print '<td align="right"><label for="emailid">Email address</label></td>'
  print '<td><input type="text" name="email" id="emailid"></td>'
  print '</tr>'
  print '</table>'
  print '<input type="submit" value="Submit" />'
  print '</form>'
  gs.printFooter('Create an Account')
  gs.db.disconnect()

main()
