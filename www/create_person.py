#!/usr/bin/env python

import sys

import ElGrupo

def main():
  # Set filenames
  conffilename = '/home/adam/ElGrupo/conf.txt'

  # Load it
  gs = ElGrupo.Session(conffilename)
  gs.db.connect()
  gs.accountCheck()

  gs.printHeader('Create a Person')
  print '<form action="thanks_person.py" method="get">'
  print '<table>'
  print '<tr>'
  print '<td><label for="nameid">Name</label></td>'
  print '<td><input type="text" name="name" id="nameid"></td>'
  print '</tr>'
  print '<tr><td><input type="submit" value="Submit" /></td><td></td>'
  print '</table>'
  print '</form>'
  gs.printFooter('Create a Person')
  gs.db.disconnect()

main()
