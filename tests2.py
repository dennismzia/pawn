# -*- coding: latin-1 -*-

import imapclient, pyzmail, html2text , email,csv
import json, time, pytz, re
from datetime import datetime

user = 'qzonescraper@gmail.com'
password = 'MoSalah11!'
imap_url = 'imap.gmail.com'
subject = 'Quad Bike'
senders_mail = 'adam.bensaud@lancasterinsurance.co.uk' #Required fields...
tag = 'INBOX'
google_sheet_name = 'qzonetests'


def get_mails():
    global text_data
    iobj = imapclient.IMAPClient(imap_url)
    iobj.login(user,password)
    iobj.select_folder(tag)
    criteria = [b'UNSEEN',b'SUBJECT', b'Quad Bike']
    unread = iobj.search(criteria=criteria)
    print(unread)

    if unread:
        for i in unread:
            print('There are: ' + str(len(unread)), 'unread emails')
            mail = iobj.fetch(i,['BODY[]'])
            # print(mail)
            mcontent = pyzmail.PyzMessage.factory(mail[i][b'BODY[]'])
            # print(mcontent)
            subject = mcontent.get_subject()
            receiver_name , receiver_email = mcontent.get_address('from')
            text_data = html2text.html2text(mcontent.html_part.get_payload().decode(mcontent.html_part.charset))
            print(text_data)
            file = open('wks2.txt', 'w')
            file.write(text_data)
            file.close()
            time.sleep(2)
            iobj.set_flags(i,['\\Seen'])
            print('mail marked as read')
            # print('parsing magic has began')
            # start_parser()
            # break
    else:
        text_data = None
        print('no mails to parse')
        time.sleep(30)

import re
with open('wks2.txt','r') as file:
    text_data = file.read()
    # print text_data

def extract():

    global pcode
    global esize
    global _value
    global age
    global y_of_make
    global use
    global bonus_claim
    global ncb
    global mage
    global tp3
    global con_load
    global cload
    global own_yr
    global p_psg
    global stg4
    global ganchor
    global scrty
    global riders
    global val
    global _email
    global first_name
    global last_name
    global phone
    global make
    global _model

    if text_data != None:
        'postcode'
        p1 = text_data[text_data.find('POSTCODE'):text_data.find('DATE OF BIRTH')].split('POSTCODE')[1]
        p2 = re.findall(r'(\w*[A-Za-z0-9])\s(\w*[A-Za-z0-9])',p1)
        pcode = p2[0][0] + ' ' + p2[0][1]
        print(pcode)

        'Engine size'
        esz = text_data[text_data.find('ENGINE SIZE'):text_data.find('REGISTRATION')].split('ENGINE SIZE')[1]
        esize = re.findall(r'\d+',esz)[0]
        print(esize)

        'Vehicle value'
        v1 = text_data[text_data.find('VEHICLE VALUE'):text_data.find('YEAR OF MANUFACTURE')].split('VEHICLE VALUE')[1]
        _value = re.findall(r'\d+', v1)[0]
        print(_value)

        'age'
        try:
            ag = text_data[text_data.find('DATE OF BIRTH'):text_data.find('INSURANCE START DATE')].split('DATE OF BIRTH')[1].split('/')[-1]
            ag2 = re.findall(r'\d+', ag)[0]
            tz_London = pytz.timezone('Europe/London')
            datetime_London = datetime.now(tz_London).strftime("%Y")
            age = int(datetime_London) - int(ag2)
            print(age)
        except:
            age = '0'

        'year of make'
        try:
            y1 = text_data[text_data.find('YEAR OF MANUFACTURE'):text_data.find('QUOTE REFERENCE')]
            y2 = y1[y1.find('YEAR OF MANUFACTURE'):y1.find('IS THE VEHICLE MODIFIED?')]
            y_of_make = ''.join(re.findall(r'\d', y2))#[0]
            # print y_of_make
        except:
            y_of_make = '0'
            pass

        'use'
        use = 'SD&P Only'

        bonus_claim = '0%'

        ncb = 'No'

        'mileage'
        mage = '5000'

        'vehicle use'
        tp3 = 'Sports'

        'convictions load'
        con_load = '0%'

        cload = '0%'

        'own yr'
        own = text_data[text_data.find('HOW LONG HAVE YOU OWNED THE VEHICLE?'):text_data.find('WHERE IS THE VEHICLE STORED OVERNIGHT?')].split('HOW LONG HAVE YOU OWNED THE VEHICLE?')[1]
        own2 = re.findall(r'(\w*\w)', own)
        # print len(own2)
        if len(own2) > 1:
            own_yr = '0'
            print own_yr
        else:
            own_yr = re.findall(r'\d+',own)[0]
            print own_yr

            # own_yr = '0' if len(own2) > 1 else re.findall(r'\d+',own)[0]

        'pillon passenger'
        p_psg = 'No'
        'patrickdeclan@btinternet.com'

        'vehicle storage'
        try:
            stg1 = text_data[text_data.find('WHERE IS THE VEHICLE STORED OVERNIGHT?'):text_data.find('PERSONAL DETAILS')].split('WHERE IS THE VEHICLE STORED OVERNIGHT?')[1]
            stg4 = ''.join(re.findall(r'[A-Za-z0-9]',stg1))
            print stg4
        except:
            pass

        ganchor = 'No'
        print ganchor

        scrty = 'Thatcham 1'
        print scrty

        riders = 'insured only'
        print riders

        'phone'

        ph = text_data[text_data.find('PREFERRED TELEPHONE NUMBER'):text_data.find('ADDITIONAL TELEPHONE')].split('PREFERRED TELEPHONE NUMBER')[1]
        phone = ''.join(re.findall(r'\d',ph))
        print phone

        'vehicle make'
        try:
            m1 = text_data[text_data.find('VEHICLE MAKE'):text_data.find('VEHICLE MODEL (if known)')].split('VEHICLE MAKE')[1]
            make = ''.join(re.findall(r'\w',m1))
            print make
        except:
            pass

        'vehicle model'
        try:
            v1 = text_data[text_data.find('VEHICLE MODEL (if known)'):text_data.find('ENGINE SIZE')].split('VEHICLE MODEL (if known)')[1]
            _model = ''.join(re.findall(r'\w',v1))
            print _model
        except:
            pass
        'first-name and last-name'
        try:
            fn = text_data[text_data.find('NAME'):text_data.find('PREFERRED TELEPHONE NUMBER')].split('NAME')[1]
            fn2 = re.findall(r'(Mr|Ms|Mrs)\s(\w*[A-Za-z0-9])\s(\w*[A-Za-z0-9])',fn)
            first_name = fn2[0][1]
            print first_name
        except:
            # print('firstname error')
            first_name = re.findall(r'(Mr|Ms|Mrs)(\s*)(\w*[A-Za-z0-9])\s(\w*[A-Za-z0-9])',fn)[0][2]
            print first_name
            pass
        try:
            last_name = fn2[0][2]
            print(last_name)
        except:
            # print 'lastname error'
            last_name = re.findall(r'(Mr|Ms|Mrs)(\s*)(\w*[A-Za-z0-9])\s(\w*[A-Za-z0-9])',fn)[0][3]
            print last_name
            pass

        'email'
        emil = text_data[text_data.find('EMAIL ADDRESS'):text_data.find('ADDRESS LINE 1')].split('EMAIL ADDRESS')[1]
        _email = re.findall(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9-_]+\.[A-Za-z0-9-._]+',emil)[0]
        print _email
    
        insurance_start_date = text_data[text_data.find('INSURANCE START DATE'):text_data.find('QUOTE REFERENCE')].split('INSURANCE START DATE')[1]
        insurance_start_date = re.findall(r'[0-9]+/[0-9]+/*[0-9]+',insurance_start_date)[0]
        print insurance_start_date

        quote_reference = text_data[text_data.find('QUOTE REFERENCE'):text_data.find('This user')].split('QUOTE REFERENCE')[1]
        quote_reference = re.findall(r'[A-Za-z0-9-_]+',quote_reference)[0]
        print quote_reference
    else:
        print('text_data is empty meaning no new mails.')

# if _model == 'raptor' or 'RAPTOR':
#     pass
# if esize < 250 and age <20:
#     pass
# elif esize <350 and age == 21 or 22:
#     pass

val = '£312.44'
val2 = re.findall(r'[*\d]+.',val)
val3 = float(str(val2[0]) + str(val2[1])) if len(val2) >= 2 else float(str(val2[0]))
print val3

# val3 = float(str(re.findall(r'[*\d]+.',val)[0]) + str(re.findall(r'[*\d]+.',val)[1])) if len(re.findall(r'[*\d]+.',val)) >= 2 else float(str(re.findall(r'[*\d]+.',val)[0]))
brokers_fee = 40
added_premium = val3 + brokers_fee
deposit = 0.2 * added_premium
montly_installments = ((0.8 * added_premium)*0.16 + (0.8*added_premium))/10
print added_premium, deposit , montly_installments