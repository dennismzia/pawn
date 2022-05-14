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

get_mails()

