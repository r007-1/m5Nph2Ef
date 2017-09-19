import smtplib
import time



server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login("lovetteregner@gmail.com", "")

msg = "\r\n".join([
  "From: lovetteregner@gmail.com",
  "To: jayhan@ymail.com",
  "Subject: Hoyyy",
  "",
  "DON'T DIE FROM THE STUPID EARTHQUAKE. GET ON THE NEXT FLIGHT AND CALL ME. OR ELSE."
  ])

for i in range(0, 110):
    server.sendmail("lovetteregner@gmail.com", "jayhan@ymail.com", msg) ##will send to recipient as bcc
    time.sleep(15)


#server.sendmail("lovetteregner@gmail.com", "lovetteregner@gmail.com", msg)