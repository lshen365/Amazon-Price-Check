import smtplib

class MailSMTP:
    def __init__(self,oldPrice,newPrice,link):
        self.oldPrice = oldPrice
        self.newPrice = newPrice
        self.link = link
    def sendMail(self):
        gmail_user = ''
        gmail_password = ''
        sent_from = gmail_user
        to = []
        with open('Emails.txt') as my_file:
            for line in my_file:
                to.append(line)
        subject = "Price Change detected"
        body = 'Price has been changed from '+self.oldPrice+ ' to '+self.newPrice+ '. \n\n\n More information can be found at: \n '+self.link

        email_text = """\
                From: %s
                To: %s
                Subject: %s

                %s
                """ % (sent_from, ", ".join(to), subject, body)
        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user,gmail_password)
            # ...send emails
            server.sendmail(sent_from, to, email_text)
            server.close()

            print ('Email sent!')
        except:
            print ('Something went wrong...')
