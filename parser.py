#!/usr/bin/python
# -*- coding: latin-1 -*-

# from __future__ import unicode_literals
import imapclient, pyzmail, html2text , email,csv
import gspread ,json, time, pytz, re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

user = 'qzonescraper@gmail.com'
password = 'MoSalah11!'
imap_url = 'imap.gmail.com'
subject = 'Quad Bike'
senders_mail = 'adam.bensaud@lancasterinsurance.co.uk' #Required fields...
tag = 'INBOX'
google_sheet_name = 'qzonetests'
brokers_fee = 40

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)

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
            print('parsing magic has began')
            start_parser()
            # break
    else:
        text_data = None
        print('no mails to parse')
        time.sleep(30)

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
    global insurance_start_date
    global quote_reference

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
        try:
            emil = text_data[text_data.find('EMAIL ADDRESS'):text_data.find('ADDRESS LINE 1')].split('EMAIL ADDRESS')[1]
            _email = re.findall(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9-_]+\.[A-Za-z0-9-._]+',emil)[0]
            print _email
        except:
            pass

        try:
            start_date = text_data[text_data.find('INSURANCE START DATE'):text_data.find('QUOTE REFERENCE')].split('INSURANCE START DATE')[1]
            insurance_start_date = re.findall(r'[0-9]+/[0-9]+/*[0-9]+',start_date)[0]
            print insurance_start_date
        except: pass

        try:
            reference = text_data[text_data.find('QUOTE REFERENCE'):text_data.find('This user')].split('QUOTE REFERENCE')[1]
            quote_reference = re.findall(r'[A-Za-z0-9-_]+',reference)[0]
            print quote_reference
        except: pass 

    else:
        print('text_data is empty meaning no new mails.')


def calculate():
    global val
    global added_premium
    global deposit
    global monthly_installments

    wks = gc.open('kgm_quad_calculator_201912 (1)').sheet1
    print('calculator found and opened successfully')
    print('started calculator')
    if stg4 == 'Garage':
        cover = wks.update_acell('E4','TPFT')
        print('storage is garage soooo TPFT')
    else:
        cover = wks.update_acell('E4','TPO')
        print('not garage so storge sorted')

    cover = wks.update_acell('E4','TPFT') if stg4 == 'Garage' else wks.update_acell('E4','TPO')
    postcode = wks.update_acell('E6', globals()['pcode'])
    engine_size = wks.update_acell('E8', globals()['esize'])
    vehicle_value = wks.update_acell('E14', globals()['_value'])
    age_of_rider = wks.update_acell('E16', globals()['age'])
    year_of_manufacture = wks.update_acell('E18',globals()['y_of_make'])
    vehicle_use = wks.update_acell('E20', globals()['use'])
    claim_bonus = wks.update_acell('E22', globals()['bonus_claim'])
    protected_NCB = wks.update_acell('E24', globals()['ncb'])
    mileage = wks.update_acell('E26', globals()['mage'])
    typ_of_quad = wks.update_acell('E28', globals()['tp3'])
    conviction_load = wks.update_acell('E30',globals()['con_load'])
    claim_load = wks.update_acell('E32',globals()['cload'])
    ownership = wks.update_acell('E34', globals()['own_yr'])
    pillion_passenger = wks.update_acell('E36',globals()['p_psg'])
    storage = wks.update_acell('E38',globals()['stg4'])
    ground_anchor = wks.update_acell('E40',globals()['ganchor'])
    security = wks.update_acell('E42', globals()['scrty'])
    additional_riders = wks.update_acell('E44',globals()['riders'])

    va = wks.acell('H51').value #
    val = str(va.encode('utf-8'))
    print val
    val2 = re.findall(r'[*\d]+.',val)
    val3 = float(str(val2[0]) + str(val2[1])) if len(val2) >= 2 else float(str(val2[0]))
    print val3
    added_premium = val3 + brokers_fee
    deposit = 0.2 * added_premium
    monthly_installments= ((0.8 * added_premium)*0.16 + (0.8*added_premium))/10
    print added_premium, deposit , monthly_installments
    time.sleep(2)
    print('calculator done')



def parse_to_sheets():
    global lists
    print('started google sheets parsing')
    def create_sheet():
        sh = gc.create(google_sheet_name)
        sh.share(user,perm_type='user',role='writer')
        wks = sh.sheet1
        return wks

    try:
        wks = gc.open(google_sheet_name).sheet1
    except Exception as e:
        print('no new sheet under that name sooo Creating right away...:)')
        create_sheet()
        wks = create_sheet()

    print('writing data to sheets....')
    if len(wks.get_all_values()) < 1:
        print('creating headers')
        wks.update_acell('A1','first_name')
        wks.update_acell('B1','last_name')
        wks.update_acell('C1','email')
        wks.update_acell('D1','phone')
        wks.update_acell('E1','make')
        wks.update_acell('F1','model')
        wks.update_acell('G1','pcode')
        wks.update_acell('H1','premium')
        wks.update_acell('I1','PREMIUM + FEE')
        wks.update_acell('J1','DEPOSIT')
        wks.update_acell('K1','MONTHLY INSTALLMENTS')
        print('doooooone adding headers')
    else:
        lists = len(wks.get_all_values())
        print(lists)
    def parser():
        print('adding new line')
        n = lists + 1
        wks.update_acell('A' + str(n), first_name)
        print('first name done')
        wks.update_acell('B' + str(n), last_name)
        print('last name done')
        wks.update_acell('C' + str(n), _email)
        print('email done')
        wks.update_acell('D' + str(n), phone)
        print('phone done')
        wks.update_acell('E' + str(n), make)
        print('make done')
        wks.update_acell('F' + str(n), _model)
        print('model done')
        wks.update_acell('G' + str(n), pcode)
        print('postal code done')
        wks.update_acell('H' + str(n), val)
        print('value or price done')
        wks.update_acell('I' + str(n), added_premium)
        wks.update_acell('j' + str(n), deposit)
        wks.update_acell('k' + str(n), monthly_installments)
        wks.update_acell('L' + str(n), insurance_start_date)
        wks.update_acell('M' + str(n), quote_reference)
        print('all done successfully')
    parser()
    print('adding backup csv file to project dir')
    with open('scraped_data.csv','a') as csv_file:
        fieldnames = ['first_name','last_name','email','phone','make','model','post_code','price','added_premium','deposit','monthly_installments','insurance_start_date','quote_reference']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow({
            'first_name':globals()['first_name'],
            'last_name':globals()'last_name',
            'email':globals()['_email'],
            'phone':globals()['phone'],
            'make':globals()['make'],
            'model':globals()['_model'],
            'post_code':globals()['pcode'],
            'price':globals()['val'],
            'added_premium':globals()['added_premium'],
            'deposit':globals()['deposit'],
            'monthly_installments':globals()['monthly_installments'],
            'insurance_start_date':globals()['insurance_start_date'],
            'quote_reference':globals()['quote_reference']
            })
    print('finished backing up data')


def start_parser():
    try:
        extract()
    except Exception as exc:
        print(exc,'exception in extracting data from mail')
    try:
        calculate()
    except Exception as exx:
        print(exx,'exception occurs if data in calculator is changed')
    try:
        parse_to_sheets()
    except Exception as exxx:
        print(exxx,'occurs in parsing to sheets probably done with daily quota')


def main():
    while True:
        try:
            get_mails()
        except Exception as e:
            print(e, 'sleeping for 10secs before second retry')
            time.sleep(10)
            get_mails()


if __name__ == '__main__':
    main()


# from flask import Flask
# from multiprocessing import Process

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Parser running'
# if __name__ == '__main__':
#     p = Process(target=main)
#     p.start()
#     app.run(debug=True,use_reloader=False)
#     p.join()
