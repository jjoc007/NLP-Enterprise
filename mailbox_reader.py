import mailbox
import uuid
import hashlib
from src.utils.constants import *

def extractattachements(message):
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            if part.get_filename() is None: continue
            filename = part.get_filename()
            print(filename)
            m = hashlib.md5(filename.encode('utf-8')).hexdigest()

            if part.get_payload(decode=True) is not None:
                fb = open(LOCATION_FILES + "files/" + m, 'wb')
                fb.write(part.get_payload(decode=True))
                fb.close()

def extract_body(message):
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True)
                        idbody = str(uuid.uuid1())
                        fb = open(LOCATION_FILES + 'files/' + idbody, 'wb')
                        fb.write(body)
                        fb.close()

print("Reading emails:")

mbox_file = "/home/juan/Descargas/111/Takeout/Mail/Inbox.mbox"

print("Processing " + mbox_file)
mbox = mailbox.mbox(mbox_file)
count_emails = 0
for key in mbox.iterkeys():
    count_emails += 1
    message = mbox[key]
    print("From: " + str(message['from']))
    print("To: " + str(message['to']))
    print("Subject: " + str(message['Subject']))
    #print("-----------------------------")
    print("Body\n\n")
    extractattachements(message)
    extract_body(message)

    print("********************************************")

print("Total de emails:"+str(count_emails))
