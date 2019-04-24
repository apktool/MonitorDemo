from notify import exmail
from database import mysql_utils
from yaml import safe_load, dump
from datetime import datetime


def get_user_access_msg(user_list):
    mysql = mysql_utils.mysql(documents['mysql'])

    msg = str()

    for user in user_list:
        key = next(iter(user))
        value = user[key]
        result = mysql.query_data(key)
        tmp = '{} visited {} times in past 17 hours.\n'.format(value, result['access_count'])
        msg = msg + tmp

    return msg


def send_user_msg(email, msg):
    title = 'IDM AUDIT REPORT | ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mail = exmail.exmail(email)
    mail.send(title, msg)


if __name__ == '__main__':
    documents = safe_load(open('config.yaml', 'r'))
    
    user_list = documents['user_list']

    msg = dict()

    for company, users in user_list.items():
        msg[company] = get_user_access_msg(users)


    email = documents['email']

    for company, mail in email.items():
        send_user_msg(mail, msg[company])
