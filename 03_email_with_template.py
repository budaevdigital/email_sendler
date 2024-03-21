# Отправка будет осуществлять через любой почтовый сервер
# Адрес сервера	| smtp.yandex.ru:465 | smtp.mail.ru:465 | smtp.rambler.ru:465
# Логин         |      %login%       | %login%@mail.ru  | %login%@rambler.ru

# Создание пароля для приложения https://id.yandex.ru/security/app-passwords
# после генерации скопировать и -> export PASS_ACCOUNT_SEND_EMAIL=<вставить сюда>

# jinja template - https://jinja.palletsprojects.com/en/2.10.x/templates/


import os
import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage
from getpass import getpass
import logging

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=int(os.environ.get("LOG_EMAIL")) if os.environ.get("LOG_EMAIL") else logging.INFO
)

LOGIN = input("Введите логин почты yandex: ")
LOGIN = LOGIN.split("@")[0] if "@" in LOGIN else LOGIN

logger.debug(f"введен логин: {LOGIN}")

EMAIL_ADDRESS = f"{LOGIN}@yandex.ru"
PASSWORD = os.environ.get("PASS_ACCOUNT_SEND_EMAIL")

if not PASSWORD:
    # скрывает символы при воде пароля
    PASSWORD = getpass("Введите пароль приложения для отправки почты")

# для подключения к почтовому серверу используем ssl
SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 465
server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
server.login(EMAIL_ADDRESS, PASSWORD)
logger.debug("Подключение к серверу SMTP - выполнено")

message = EmailMessage()

message["From"] = EMAIL_ADDRESS
message["To"] = ",".join([EMAIL_ADDRESS])
message["Subject"] = "Тестовое сообщение"

logger.debug(f"Почта сформированна: \n{message}")

# указываем свои шаблоны
base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "mail_files/email.jpg")
loader = FileSystemLoader(os.path.join(base_dir, "mail_files"))
env = Environment(loader=loader)

# загружаем шаблон в память
template = env.get_template("mail.html")

with open(image_path, "rb") as img_file:
    image_data = img_file.read()

# cоздание объекта MIMEImage и добавление его к сообщению
image = MIMEImage(image_data)
image.add_header("Content-ID", "<email_image>")  # Уникальный ID для ссылки в HTML
image.add_header("Content-Disposition", "inline", filename="email.jpg")  # Отображение в теле письма

# подставляем свои данные в шаблон (тег "image" будем вставлять чезер Content-ID)
data = {
    "title": "Новое письмо!",
    "text": "Тут могла быть ваша реклама",
    "image": "https://bogatyr.club/uploads/posts/2023-01/thumbs/1674954707_bogatyr-club-p-fon-dlya-khedera-fon-krasivo-8.jpg"
}
output = template.render(**data)

# отправляем как html страницу
message.add_alternative(output, subtype="html")
# message.attach(image)  # прикрепляем картинку к шаблону письма - cid:email_image - в src картинки в html

try:
    logger.debug("Старт приложения")
    server.sendmail(
        from_addr=EMAIL_ADDRESS,
        to_addrs=[EMAIL_ADDRESS],
        msg=message.as_string()
    )
except smtplib.SMTPException as smtp_exc:
    reason_fail = f"{type(smtp_exc).__name__}: {smtp_exc!r}"
    logger.error(f"При отправке письма произошла ошибка: {reason_fail}")
else:
    logger.info("Письмо отправлено")
finally:
    logger.debug("Завершение работы")
    server.close()
