
import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                   # Функции для работы с операционной системой, не зависящие от используемой операционной системы
import sqlite3
# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


class newclients_mailing():
    def __init__(self, record):

        self.record = record
        self.files = [r"C:\Users\pc\PycharmProjects\fullbasezakupki.gov\newclients\files"]
        self.msg_text = self.org_or_ip(self.record)[0]
        self.msg_subj = self.org_or_ip(self.record)[1]
        self.addr_to = self.record[4]

        self.send_email(self.addr_to, self.msg_subj, self.msg_text, self.files)
        print(record)

    def org_or_ip(self, record):

        if record[0] == '0':

            msg_subj = f'Сопровождение торгов Для ИП {record[2]} '
            msg_text = f"""
                    ИП {record[2]} Поздравляем с успешной регистрации в Единой информационной системе !\n
                    Наша компания занимается комплексным сопровождением торгов с 2014 года , мы предлагаем лучший сервис по скромным ценам. Наше преимущество автоматизация почти всех закупочных процедур, которые созданы под пылким руководством настоящих профессионалов своего дела. 
                    Мы предлагаем:
                    -Полное сопровождения участника на всех этапах закупочных процедур.
                    - Сметное сопровождение в закупках по строительству , поиск  поставщиков
                    - Поиск торгов с автоматическим добавлением в вашу гугл-таблицу.
                    - Помощь в трудных закупках, сложных заказчиках, УФАСе.
                    - Удобные условия сотрудничества в зависимости от ваших потребностей\n
                    Тендерное сопровождение - это комплекс услуг, которые оказываются участнику государственных или коммерческих закупок. Конечная цель сопровождения - увеличение количества побед участника в тендерах за счет более профессиональной работы специализированной компании.
                    \nЕСЛИ:\n 
                    1. В вашей компании нет отдельного специалиста по закупкам
                    2. У вас нет времени самостоятельно заниматься заполнением заявок
                    3. Вас не устраивает медленный темп работы. Вы хотите получать больше контрактов
                    4. Вы хотите платить за результат, а не за "просиживание штанов" собственного сотрудника
                    \n
                    Позвоните нам и мы обязательно Ваc проконсультируем. \b 89787215775\b\n

                    В приложении  прайс-лист на наши услуги.\n

                    С уважением , Ваш менеджер:
                    Ларский Иван 89787215775  
                    email    9782179840@mail.ru
                    """

        else:
            msg_subj = f'Сопровождение торгов Для  {record[0]} '
            msg_text = f"""
                    Уважаемый участник закупок ,{record[0]}\n
                    Наша компания занимается комплексным сопровождением торгов с 2014 года , мы предлагаем лучший сервис по скромным ценам. Наше преимущество автоматизация почти всех закупочных процедур, которые созданы под пылким руководством настоящих профессионалов своего дела. 
                    \nМы предлагаем:
                    -Полное сопровождения участника на всех этапах закупочных процедур.
                    - Сметное сопровождение в закупках по строительству , поиск  поставщиков
                    - Поиск торгов с автоматическим добавлением в вашу гугл-таблицу.
                    - Помощь в трудных закупках, сложных заказчиках, УФАСе.
                    - Удобные условия сотрудничества в зависимости от ваших потребностей\n
                    Тендерное сопровождение - это комплекс услуг, которые оказываются участнику государственных или коммерческих закупок. Конечная цель сопровождения - увеличение количества побед участника в тендерах за счет более профессиональной работы специализированной компании.
                    \nЕСЛИ:\n 
                    1. В вашей компании нет отдельного специалиста по закупкам
                    2. У вас нет времени самостоятельно заниматься заполнением заявок
                    3. Вас не устраивает медленный темп работы. Вы хотите получать больше контрактов
                    4. Вы хотите платить за результат, а не за "просиживание штанов" собственного сотрудника
                    \n
                    Позвоните нам и мы обязательно Ваc проконсультируем. \b 89787215775\b\n

                    В приложении  прайс-лист на наши услуги.\n

                    С уважением , Ваш менеджер:
                    Ларский Иван 89787215775  
                    email    9782179840@mail.ru
                    """
        return msg_text, msg_subj

    def send_email(self, addr_to, msg_subj, msg_text, files):
        con = sqlite3.connect('newclients.db')
        cur = con.cursor()
        cur.execute(f"UPDATE newclients SET status = 1 WHERE  INN = ?", (self.record[3],))
        con.commit()
        con.close()

        addr_from = "rnp.auto.informator@gmail.com"  # Отправитель
        password = "zPxcjWHUW6rWW22"  # Пароль

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = msg_subj  # Тема сообщения

        body = msg_text  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        self.process_attachement(msg, files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим

        # ==========================================================================================================================

    def process_attachement(self, msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
        for f in files:
            if os.path.isfile(f):  # Если файл существует
                self.attach_file(msg, f)  # Добавляем файл к сообщению
            elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
                dir = os.listdir(f)  # Получаем список файлов в папке
                for file in dir:  # Перебираем все файлы и...
                    self.attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению

    def attach_file(self, msg, filepath):  # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)  # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:  # Если тип файла не определяется
            ctype = 'application/octet-stream'  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
        if maintype == 'text':  # Если текстовый файл
            with open(filepath) as fp:  # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                fp.close()  # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':  # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:  # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению





