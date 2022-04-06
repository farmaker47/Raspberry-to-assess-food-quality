import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 
body = '''Hello,
I am G.S.
'''
# put your email here
sender = 'george.soloupis.raspberry@gmail.com'
# put the password here
password = 'xxxxxxxxxxxx'
# put the email of the receiver here
receiver = 'farmaker47@gmail.com'
 
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender
message['To'] = receiver
message['Subject'] = 'This email has an attacment, a csv file'
 
message.attach(MIMEText(body, 'plain'))
 
csvname = '/home/george/Downloads/mq_sensors_log_2_days.csv'
 
# open the file in binary
binary_csv = open(csvname, 'rb')
 
payload = MIMEBase('application', 'octate-stream', Name=csvname)
# payload = MIMEBase('application', 'csv', Name=csvname)
payload.set_payload((binary_csv).read())
 
# enconding the binary into base64
encoders.encode_base64(payload)
 
# add header with csv name
payload.add_header('Content-Decomposition', 'attachment', filename=csvname)
message.attach(payload)
 
#use gmail with port
session = smtplib.SMTP('smtp.gmail.com', 587)
 
#enable security
session.starttls()
 
#login with mail_id and password
session.login(sender, password)
 
text = message.as_string()
session.sendmail(sender, receiver, text)
session.quit()
print('Mail Sent')
