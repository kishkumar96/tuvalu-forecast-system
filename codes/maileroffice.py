import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

#username = "svcsmtp-cloud@spc.int"
#password = "R(VFv0yHFyMbY3e"
password = "R(VFv0yHFyMbY3e"
#mail_from = "svcsmtp-cloud@spc.int"
mail_to = "divesha@spc.int"

username = "svcSMTP-Cloud@spc.int"
#password = "R(VFv0yHFyMbY3e"
mail_from = "svcSMTP-Cloud@spc.int"

def send_email(documents, receipients, mail_subject, mail_body):
    exampleCombinedString = ','.join(receipients)
    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=exampleCombinedString
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'html'))
    """
    for x in documents:
        with open(x, "rb") as f:
            name_split = x.split('/')
            attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition','attachment',filename=str(name_split[3]))
            mimemsg.attach(attach)
    """
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()

#document_arr = ["/home/divesha/data/TUV/tailored-report-tv/Hall_Reports/2024080812/Nanumea_Channel_2024080812.pdf"]
#receipients =  ["divesha@spc.int"]
#mail_subject = "test"
#mail_body = "testinggg."
#send_email(document_arr, receipients,mail_subject,mail_body)
