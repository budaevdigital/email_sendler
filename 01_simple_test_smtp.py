# smtpd - smtpd клиент для отправки почты
import smtplib

server = smtplib.SMTP("localhost", 25)  # подключиться локально

server.sendmail(
    from_addr="from@mail.com",
    to_addrs="to@mail.com",  # кому - строка или список строк адресов
    msg="<h1>This is just the message</h1>"
)

server.close()

# для запуска:
# - запуск сервера
# python -m smtpd -n -c DebuggingServer localhost:25

# - запуск кода
# python 01_simple_test_smtp.py