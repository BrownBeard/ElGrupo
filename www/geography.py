#!/usr/bin/env python

import sys

sys.path.append('include')
import ElGrupo
import game

print 'Content-Type: text/html'
print

print '<html><body>'
game.printqs('Geography')
print '</body></html>'
