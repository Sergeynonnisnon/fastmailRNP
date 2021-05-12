# -*- coding: UTF-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sqlite3
import time
import random


# create message object instance
def send_email(mess, to_email, subscription):
    msg = MIMEMultipart()

    message = f'''     С Вами расторгли контракт в одностороннем порядке! Заказчик сошел с ума? Или он решил Вам что-то доказать?

Отменим данное решение и сведения о Вас не будут включены в РНП, а также, вернем обеспечение контракта, если надо. Вы можете задать любые вопросы!

Для этого просто позвоните по телефону +7 978 721 5775 или напишите нам.
Если своими силами не получитьcя урегулировать данную проблему, пишите нам. Мы на протяжении 5 лет решаем подобные вопросы, я и мои коллеги, опытные юристы, исходя из документов по контракту, заранее можем сказать, что Вас ожидает.
Если дело провальное, то мы так и сообщаем клиенту, так как наша мотивация на прямую зависит от победы. Попадание в РНП приводит к большим проблемам, чем простой запрет на участие в закупке, в том числе проблемам с банками, с текущими обязательствами и прочее. И часто действует как отталкивающий фактор (наподобие решения о блокировке счета ФНС). Ваша информация сразу показывается во всех общедоступных источниках по проверке контрагентов, более того, если Вы один раз там побывали, то эта информация останется в отношении вашей компании навсегда.

Обращаем Ваше внимание, что согласно ч.6 ст.104 ФЗ-44, Заказчик в течение 3 рабочих дней направляет в УФАС, информацию с обоснованием причин одностороннего отказа. После этого, УФАС осуществляет проверку этих сведений в течение 5 рабочих дней согласно ч.7 ст.104 ФЗ-44. В случае подтверждения достоверности фактов, указанных Заказчиком, УФАС включает информацию (ИНН организации, учредителей и Директора) в реестр недобросовестных поставщиков (РНП) в течение 3 рабочих дней.По вопросам помощи в решении данной ситуации, а также по любым вопросам, связанным с 44 и 223 ФЗ обращайтесь по указанным ниже контактам:

Cсылка для ознакомления:
https://zakupki.gov.ru/epz/dizk/dizkCard/generalInformation.html?dizkId={mess}

г. Киров, ул. Калинина, 38,
офис 313.
тел. + 79787215775
'''

    # setup the parameters of the message
    password = "zPxcjWHUW6rWW22"
    msg['From'] = "rnp.auto.informator@gmail.com"
    msg['To'] = to_email
    msg['Subject'] = f'Не дадим внести в РНП по контракту №{subscription}'

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server

    server = smtplib.SMTP('smtp.gmail.com: 587')
    print('отправленно на ', to_email)
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    con = sqlite3.connect('RNP.db')
    cur = con.cursor()
    cur.execute(f"UPDATE RNP SET status = 0 WHERE  decision_number = {mess} ")
    con.commit()
    con.close()
    print('отправленно на ', to_email)


def format_string(a):
    for i in a:
        if i == '.':
            a = a.split('.')
            x = str()
            for y in a:
                if y != a[-1]:
                    x += y + '\.'
                else:
                    x += y
    return x


def mailing():
    con = sqlite3.connect('RNP.db')

    cur = con.cursor()
    cur.execute('''SELECT * FROM RNP WHERE status = 0 AND email_status = 1  LIMIT 50''')
    exists = cur.fetchall()
    print(exists)
    for data in exists:

        cur.execute(f'''SELECT * FROM RNP WHERE email = ?''', (data[2],))
        checks = cur.fetchall()

        if len(checks) <= 1:
            send_email(data[0], data[2], data[1])
            print(checks)
            rand_sleep = random.randint(1, 5)
            time.sleep(float(rand_sleep))
            print(f'отправлено на {data[2]}')
            print(f'Ожидаю {rand_sleep} секунд для отправки следующего письма')

        else:
            cur.execute(f"UPDATE RNP SET status = 0 WHERE  email = ?", (data[2],))
            print(f'{checks} уже в таблице и ему не будет направленн емейл')

    print(f'направлено {len(exists)} емейл')
    con.commit()
    con.close()
