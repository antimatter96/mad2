import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_HOST = 'localhost'
SMTP_PORT = '1025'
SMTP_USERNAME = 'arpit@arpit.com'
SMTP_PASSWORD = ''
SMTP_FROM = 'arpit@arpit.com'

def send_email(to, subject, plain_text, html_text, attachment):
  print("Sending email")
  try:
    msg = MIMEMultipart()

    msg['From'] = SMTP_FROM
    msg['To'] = to
    msg['Subject'] = subject

    if plain_text != None:
      msg.attach(MIMEText(plain_text, "plain"))

    if html_text != None:
      msg.attach(MIMEText(html_text, "html"))

    s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    s.login(SMTP_USERNAME, SMTP_PASSWORD)

    if attachment != None:
      filename = attachment['filename']
      upload_path = attachment['upload_path']
      subtype = attachment['subtype']

      with open(upload_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype=subtype)
      attach.add_header('Content-Disposition', 'attachment', filename=filename)
      msg.attach(attach)

    s.send_message(msg)
    s.quit()
    print("Email sent")
  except Exception as e:
    print('Error', e)
    return False

  return True
