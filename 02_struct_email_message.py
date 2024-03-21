import smtplib
from email.message import EmailMessage

server = smtplib.SMTP("localhost", 25)

message = EmailMessage()

message["From"] = "from@mail.com"
message["To"] = "to@mail.com"
message["Subject"] = "Title for email message"
message.set_content("В этой фразу 25 символов.")

server.sendmail(
    from_addr=message["From"],
    to_addrs=message["To"],
    msg=message.as_string()
)

server.close()

