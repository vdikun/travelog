''' email functions 
    in future this will handle password reset messages
    right now it's just to tell viewers about their accounts
'''

from flask_mail import Mail, Message

mail = Mail()

'''
emails new viewers with account information
'''
def email_new_viewers(owner, emails, password):

	subject = "New Travelog Account"

	msg_body = "Hello from Travelog.\n\n User {0} has approved you for the following account:\n\n \
				Username: {1}\nPassword: {2}\n\nLog in at travelog.herokuapp.com to access {0}'s photos. \
				\n\nYour credentials should be kept confidential." 

	with mail.connect() as conn:
	    for email in emails:
	        msg = Message(sender="noreply@travelog.herokuapp.com",
	        			  recipients=[email],
	                      body=msg_body.format(owner.name, email, password),
	                      subject=subject)
	        print "sending email to {0}".format(email)
	        conn.send(msg)

