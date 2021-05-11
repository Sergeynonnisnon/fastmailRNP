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

    message = f'''Добрый день, Заказчик принял решение расторгнуть с Вами контракт в одностороннем порядке.

Мы знаем, что и в какие сроки необходимо сделать, чтобы Заказчик отменил данное решение и сведения о Вас не были включены в РНП, а также, как вернуть обеспечение контракта. Вы можете задать любые вопросы!

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
    password = "OuPA3licT3u$"
    msg['From'] = "9127343243@mail.ru"
    msg['To'] = to_email
    msg['Subject'] = f'уведомление о внесении в РНП по контракту№{subscription}'

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.mail.ru: 465')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    con = sqlite3.connect('RNP.db')
    cur = con.cursor()
    cur.execute(f"UPDATE RNP SET status = 0 WHERE  decision_number = {mess} LIMIT 50")
    con.commit()
    con.close()
def format_string(a):
    for i in a:
        if i == '.':
            a = a.split('.')
            x = str()
            for i in a:
                if i != a[-1]:
                    x += i + '\.'
                else:
                    x += i
    return x

def mailing():
    con = sqlite3.connect('RNP.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM RNP WHERE status = 1 AND email_status = 1''')
    exists = cur.fetchall()
    for data in exists:
        #format_email = format_string(str(data[2]))
        cur.execute(f'''SELECT * FROM RNP WHERE email = ?''',(data[2],))
        checks = cur.fetchall()

        if len(checks) <= 1:
            send_email(data[0], data[2], data[1])
            rand_sleep = random.randint(1, 5)
            time.sleep(float(rand_sleep))
            print(f'отправлено на {data[2]}')
            print(f'Ожидаю {rand_sleep} секунд для отправки следующего письма')

        else:
            cur.execute(f"UPDATE RNP SET status = 0 WHERE  email = ?",(data[2],))
            con.commit()
            print(f'{checks} уже в таблице и ему не будет направленн емейл')


    # cur.execute(f"UPDATE RNP SET status = 0 WHERE  decision_number = {mess}")
    print(f'направлено {len(exists)} емейл')
    con.commit()
    con.close()

