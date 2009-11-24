#!/usr/bin/env python
#
#       elgrupo_pop.py
#       
#		Edward Radau

import smtplib
import sys
import ElGrupo

def calc_donation():
	Sess = ElGrupo.Session('/home/adam/ElGrupo/conf.txt')
	Database = Sess.db
	Database.connect()	
	#Begin calculation of donations
	#Formula for donation is:  P * [(h1 * h2 * ... * hP) ^ (1/P)]
	#((s1 + s2 + ... + sm) / m) will be the health for that person (hj)
	
	all_users = Database.sqlReturn('select u_id from users')		#Use for loop-range
	#people = Database.sqlReturn('select p_id from persons')     #Use for equation
		
	for i in range(len(all_users)):
		num_persons = Database.sqlReturn('select p_id from persons where u_id=' + str(all_users[i][0]))
		if len(num_persons) < 1: continue
		health_total = 1
		
		for n in range(len(num_persons)):
		   #num_stats = Database.sqlReturn('select * from stats where p_id = ' + str(i))			#number of stats each person possesses
		   total_s = Database.sqlReturn('SELECT SUM(value), COUNT(value) FROM stats WHERE p_id=' + str(num_persons[n][0]))		#calculate total sm
                   if total_s[0][1] == 0: continue
		   health = total_s[0][0]/float(total_s[0][1])					#health for ONE person
		   health_total *= health									#health for ALL persons
		
		donation = 5 * len(num_persons) * (health_total)**(1/float(len(num_persons)))                        #Donation size
		
		Database.sql('update users set this_donation = (this_donation + ' + str(donation) + ') where u_id=' + str(all_users[i][0]))
		#Database.sql('update users set total_donation = (total_donation + ' + str(donation) + ') where u_id=' + str(i))
		
	
	Database.sql('update stats set value=value-(10*rand());')
	Database.sql('update stats set value=0 where value<0;')
		
	#End calculation of donations	
	Database.disconnect()

def empty_donations():
	#Database = ElGrupo.DB()	
	#Database.connect()		
	Sess = ElGrupo.Session('/home/adam/ElGrupo/conf.txt')
	Database = Sess.db
	Database.connect()	
	people = Database.sqlReturn('select u_id from users;')		#Use for loop-range
	for i in range(len(people)):
		donation = Database.sqlReturn('select this_donation, wants_email from users where u_id=%d' % people[i][0])
                if donation[0][0] == 0: continue

		#Begin emailing the results
                if donation[0][1]:
			name = Database.sqlReturn('select name from users where u_id=' + str(people[i][0]))
			email = Database.sqlReturn('select email from users where u_id=' + str(people[i][0]))	
			
			smtpuser = 'elgruporice@gmail.com'
			smtppass = 'QsLgrup-o'
			
			FROM = "elgruporice@gmail.com"
			TO = ''.join(email[0]) # must be a list
			SUBJECT = "ElGrupo: Donations have been processed"
			TEXT='Hello, ' + ''.join(name[0]) + '!\n\nYou have donated ' + str(donation[0][0]) + ' grain(s) of rice today!'
			message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % \
			(FROM, TO, SUBJECT, TEXT)
			server = smtplib.SMTP("smtp.gmail.com",587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(smtpuser, smtppass)
			server.sendmail(FROM, TO, message)
			server.close()		
		
		#End email
		Database.sql('update users set total_donation=total_donation+this_donation, last_donation=this_donation;')
		Database.sql('update users set this_donation=0;')
	
	Database.disconnect()

if __name__ == '__main__':
  if 'calc' in sys.argv: calc_donation()
  if 'empty' in sys.argv: empty_donations()
