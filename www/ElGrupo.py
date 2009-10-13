#!/usr/bin/python

import sys
import MySQLdb
import re
import random

# DB {{{
# Holds database related stuff
class DB:
  # __init__ {{{
  def __init__(self, user='root', passwd='', db='grupo', host='localhost'):
    self.host = host
    self.user = user
    self.passwd = passwd
    self.db = db

    self.connected = False
  # }}}

  # connect {{{
  # Establish connection to the database
  def connect(self):
    try:
      self.conn = MySQLdb.connect(host = self.host,
                                  user = self.user,
                                  passwd = self.passwd,
                                  db = self.db)
      self.cursor = self.conn.cursor()
      self.connected = True
    except:
      print 'Error connecting to database.  Exiting.'
      sys.exit(1)
  # }}}

  # disconnect {{{
  def disconnect(self):
    if self.connected:
      self.cursor.close()
      self.conn.close()
      self.connected = False
  # }}}

  # sqlReturn {{{
  # Execute the statement, return the values
  def sqlReturn(self, stmt):
    self.cursor.execute(stmt)
    return self.cursor.fetchall()
  # }}}

  # sql {{{
  def sql(self, stmt):
    self.cursor.execute(stmt)
  # }}}
# }}}

# Answer {{{
class Answer:
  def __init__(self):
    self.string = ''
    self.correct = False
# }}}

# Question {{{
class Question:
  def __init__(self):
    self.string = ''
    self.answers = []
# }}}

# Game {{{
class Game:
  def __init__(self):
    self.string = ''
    self.questions = []
# }}}

# Session {{{
class Session:
  # __init__ {{{
  def __init__(self, conf_fn=None):
    self.db = DB()
    self.title_prefix = {'label': 'El Grupo', 'separator': ': '}

    # Load config file if provided
    if not conf_fn is None:
      self.load(conf_fn)
  # }}}

  # load {{{
  # Load the configuration file
  def load(self, conf_fn):
    # Open the file
    try:
      fp = open(conf_fn, 'r')
    except:
      print 'Error opening %s.  Exiting.' % (conf_fn)
      sys.exit(1)

    # Parse it
    for line in fp:
      # Remove comments
      comment_start = line.find('#')
      if comment_start >= 0:
        line = line[:comment_start]

      # Do the command
      toks = line.split()
      if len(toks) < 2: continue
      if toks[0] == 'user':
        self.db.user = toks[1]
      elif toks[0] == 'passwd':
        self.db.passwd = toks[1]
      elif toks[0] == 'db':
        self.db.db = toks[1]
      elif toks[0] == 'host':
        self.db.host = toks[1]
  # }}}

  # readQuestions {{{
  # Reinitialize the questions database.  This function is dangerous!!!
  def readQuestions(self, filename):
    # Can't do this if not connected
    if not self.db.connected:
      print "Error: can't reinitialize the questions without connecting first."
      sys.exit(1)

    # Open the file
    try:
      fp = open(filename, 'r')
    except:
      print 'Error opening %s.  Exiting.' % (filename)
      sys.exit(1)

    # Clear the tables
    self.db.sql('delete from answers;')
    self.db.sql('delete from questions;')
    self.db.sql('delete from games;')

    # Read the info in
    games = []

    for line in fp:
      # Remove comments, newlines
      comment_start = line.find('#')
      if comment_start >= 0:
        line = line[:comment_start]
      while line[-1] == '\r' or line[-1] == '\n': line = line[:-1]

      # Do the command
      toks = line.split()
      if len(toks) == 0: continue
      if toks[0] == 'game':
        if len(toks) != 3:
          print 'Error: game takes exactly 2 arguments.'
          sys.exit(1)
        g = Game()
        g.string = toks[1]
        g.filename = toks[2]
        games.append(g)
      elif toks[0] == 'question':
        if len(games) == 0:
          print 'Error: question before a game was initialized.'
          sys.exit(1)
        q = Question()
        q.string = line[line.find('n')+2:] # Remove the "question ".
        games[-1].questions.append(q)
      elif toks[0] == 'answer':
        if len(games) == 0:
          print 'Error: answer before a game was initialized.'
          sys.exit(1)
        if len(games[-1].questions) == 0:
          print 'Error: answer before a question was initialized.'
          sys.exit(1)
        a = Answer()
        if toks[1] == 'correct':
          a.correct = True
        elif toks[1] == 'incorrect':
          a.correct = False
        else:
          print 'Error: answer needs either "correct" or "incorrect".'
          sys.exit(1)
        a.string = line[line.find('t')+2:] # Remove the "...rrect ".
        games[-1].questions[-1].answers.append(a)

    # Make sql command to insert values
    g_id = 0
    q_id = 0
    g_stmt = 'insert into games (name, filename) values '
    q_stmt = 'insert into questions (g_id, question) values '
    a_stmt = 'insert into answers (q_id, answer, correct) values '
    for g in games:
      g_id += 1
      g_stmt += '("%s", "%s"), ' % (g.string, g.filename)
      for q in g.questions:
        q_id += 1
        q_stmt += '(%d, "%s"), ' % (g_id, q.string)
        for a in q.answers:
          a_stmt += '(%d, "%s", ' % (q_id, a.string)
          if a.correct: a_stmt += 'true), '
          else:         a_stmt += 'false), '
    g_stmt = g_stmt[:-2] + ';'
    q_stmt = q_stmt[:-2] + ';'
    a_stmt = a_stmt[:-2] + ';'

    # Run them
    self.db.sql(g_stmt)
    self.db.sql(a_stmt)
    self.db.sql(q_stmt)
  # }}}

  # getRandFact {{{
  def getRandFact(self):
    facts = ['The rain in Spain falls mainly on the plain.',
        'A bird in the hand is worth two in the bush.',
        'A penny saved is a penny earned.']
    return facts[random.randrange(len(facts))]
  # }}}

  # getRandQuestion {{{
  def getRandQuestion(self, game):
    # Can't do this if not connected
    if not self.db.connected:
      print "Error: can't reinitialize the questions without connecting first."
      sys.exit(1)
    rows = self.db.sqlReturn('select g_id from games where name = "%s";' %
        (game))
    g_id = rows[0][0]

    rows = self.db.sqlReturn('select min(q_id), max(q_id) from questions where g_id = %d;' % (g_id))
    min_q_id = rows[0][0]
    max_q_id = rows[0][1]
    q_id = random.randint(min_q_id, max_q_id)

    rows = self.db.sqlReturn('select question from questions where q_id = %d;' % (q_id))
    q = Question()
    q.string = rows[0][0]

    rows = self.db.sqlReturn('select answer, correct from answers where q_id = %s;' % (q_id))
    for row in rows:
      a = Answer()
      a.string = row[0]
      a.correct = (row[1] == 1)
      q.answers.append(a)

    random.shuffle(q.answers)
    return q
  # }}}

  # getQuestions {{{
  def getQuestions(self, game):
    # Can't do this if not connected
    if not self.db.connected:
      print "Error: can't reinitialize the questions without connecting first."
      sys.exit(1)
    rows = self.db.sqlReturn('select g_id from games where name = "%s";' %
        (game))
    g_id = rows[0][0]

    rows = self.db.sqlReturn(
        'select q_id, question from questions where g_id = %d;' % (g_id))
    questions = []
    q_id_map = {}
    index = 0
    q_id_list = '('
    for row in rows:
      q = Question()
      q.string = row[1]
      questions.append(q)
      q_id_map[row[0]] = index
      q_id_list += '%d, ' % (row[0])
      index += 1
    q_id_list = q_id_list[:-2] + ')'

    rows = self.db.sqlReturn(
        'select q_id, answer, correct from answers where q_id in %s;' %
        (q_id_list))
    for row in rows:
      a = Answer()
      a.string = row[1]
      a.correct = (row[2] == 1)
      questions[q_id_map[row[0]]].answers.append(a)

    return questions
  # }}}

  # getGames {{{
  def getGames(self):
    if not self.db.connected:
      print "Error: can't get list of games while not connected."
      sys.exit(1)

    rows = self.db.sqlReturn('select name, filename from games')
    games = []
    for row in rows:
      g = Game()
      g.string = row[0]
      g.filename = row[1]
      games.append(g)

    return games
  # }}}

  # doSubs {{{
  def doSubs(self, line, title):
    retval = line

    retval = re.sub(r'\n|\r', '', retval)
    while True:
      if re.search(r'\{TITLE\}', retval):
        titstr = self.title_prefix['label']
        if title != '':
          titstr = titstr + self.title_prefix['separator'] + title
        retval = re.sub(r'\{TITLE\}', titstr, retval)
      elif re.search(r'\{TOPLINKS\}', retval):
        str = '<span class="top_item">one</span><span class="top_item">two</span>'
        retval = re.sub(r'\{TOPLINKS\}', str, retval)
      elif re.search(r'\{SIDELINKS\}', retval):
        # str = '<span class="left_fact">"%s"</span><br />\n' % (self.getRandFact())
        str = ''

        games = self.getGames()
        for g in games:
          str += '<div class="left_item"><a class="item" href="%s">%s</a></div>\n' % (g.filename, g.string)
        retval = re.sub(r'\{SIDELINKS\}', str, retval)
      else:
        break

    return retval
  # }}}

  # printHeader {{{
  def printHeader(self, title='', filename='template'):
    try:
      template = open(filename, 'r')
    except:
      print 'Unable to open template file %s, exiting.' % (filename)
      sys.exit(1)

    print 'Content-Type: text/html'
    print

    for line in template:
      if re.search(r'\{TEXT\}', line): break
      else: print self.doSubs(line, title)
  # }}}

  # printFooter {{{
  def printFooter(self, title='', filename='template'):
    template = open(filename, 'r')
    ready = False

    for line in template:
      if re.search(r'\{TEXT\}', line):
        ready = True
      else:
        if ready:
          print self.doSubs(line, title)
  # }}}
# }}}
