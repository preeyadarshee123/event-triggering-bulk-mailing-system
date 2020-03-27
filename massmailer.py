import sqlite3,csv,smtplib
import schedule
import time
from datetime import date

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def work():
    def read_template(filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
            return Template(template_file_content)

    MY_ADDRESS = 'myemail@gmail.com'
    PASSWORD = 'password'
    
    message_template = read_template('message.txt')
    
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    co=sqlite3.connect('people.db')
    con=co.cursor()
    con.execute("create table if not exists mass_mailer(id text PRIMARY KEY,name text)")
    with open('data.csv',mode='r')as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            lis=[]
            print(row)
            for e in row:
                lis.append(e)
            con.execute(
                    'insert or ignore into mass_mailer (id,name) values(?,?)',
                    (lis[0],lis[1])
                )
    con.execute("SELECT * from mass_mailer")
    rows=con.fetchall()
    for row in rows:
        msg = MIMEMultipart() 
        lis1=[]
        for e in row:
            lis1.append(e)
        message = message_template.substitute(PERSON_NAME=lis1[1])
        print(message)
        msg['From']=MY_ADDRESS
        msg['To']=lis1[0]
        msg['Subject']="This is TEST"    
        msg.attach(MIMEText(message, 'plain'))   
        s.send_message(msg)
        del msg
    s.quit()
    s.close()
    co.commit()
    co.close()

schedule.every().day.at("00:00").do(work)
while True:  
    schedule.run_pending() 
    time.sleep(1) 
 
