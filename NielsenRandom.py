# Imports
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
#import email
import pandas as pd
import numpy as np
'''''
import yaml
import re
import datetime
import pytz
import time
import socket
import sys
import getopt
import os
'''

##CSV Read in
def Data_In():
    global dataf
    dataf=pd.read_csv("Covid-Nielsen-Play.csv" ) #CWD/filename, skip row for header skiprows = 1, na_values = ['no info', '.']

    #optional checkers
    #print(dataf.head(2)), #print(names[0]), #print(emails[0])


#CSV Read out
def Data_out():
    dataf.to_csv('NR_Output.csv')



##Avoid family members in the same house
def Avoider(namez, Lenz):
    global avoid, number
    avoid=np.zeros(Lenz,dtype=int)
    number=np.zeros(Lenz,dtype=int)
    for y in range (0,Lenz):
        print(namez[y], end= " ")
        number[y]=y
    print("\n")
    for x in range (0, Lenz):
        print("Enter Avoid group value for " + namez[x])
        avoid[x]=random.randint(0,Lenz) #Debugging
        #avoid[x] = int(input('Enter Number')) #manual entry



#Random assignment and check against the avoider
def RandoMK(namez, Lenz):
    global rando
    rando=np.copy(number)
    flag=1
    while (flag!=0):
        rando =np.random.choice(rando, Lenz, replace=False)
        print("Random ")
        print(rando)
        count=0
        for y in range(0, Lenz):
            if number[y] == rando[y] or avoid[y] == avoid[rando[y]]:
                #print(number[y]), #print(random[y]), #print(avoid[y]), #print(avoid[rando[y]])
                flag=1
                break
            else:
                count += 1
        if count==Lenz:
            flag=0
    print("good to go")



##Print the paired names to screen for debug
def Printer(namez, Lenz):
    global asmt
    asmt=np.copy(namez)
    for z in range (0,Lenz):
        print(namez[z], end= " ")
        print(" is with ", end= " ")
        print(namez[rando[z]])
        asmt[z]=namez[rando[z]]
        #Mailman1(z)
    dataf["Rand"] = rando
    dataf["Assign"] = asmt





# Sent the mail to the people
def Mailman1(idx):
    fromaddr = "nielsen.randomizer@gmail.com"
    toaddr = "tim.vandermeiden@gmail.com" #emails[idx]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Nielson Randomizer - Your assignment!"

    body1 = "Hello, " + names[idx] #0-Len_1
    body2 = "\n Body2"
    body3 = "\n Body3"
    body = body1 + body2 + body3
    msg.attach(MIMEText(body, 'plain'))

    '''
    filename = "The image file you put in the same directory with this file"
    attachment = open("The image file you put in the same directory with this file(ex: xxxx.jpg)", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Contnt-Disposition', "attachment; filename= %s" % filename)e
    msg.attach(part)
    '''

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "jebziwychgoxjxpj")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("mail sent to", names[idx])




Data_In()

#Pull from DF and name arrays
names = dataf["Your first Name"].to_numpy(dtype=str)
emails = dataf["Your email address"].to_numpy(dtype=str)
Len_1=names.size

#run avoider and Random int gen
Avoider(names, Len_1)
RandoMK(names, Len_1)
Printer(names, Len_1)
#Mailman1(1)

Data_out()


