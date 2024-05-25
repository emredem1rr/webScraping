import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(toMail, subject, content):
    fromMail = "yilmaznazar92@gmail.com"
    try: # e-posta gönderimi başarılı mı?
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(fromMail, "cfxs myal wgvv kkzv")

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = fromMail
        message['To'] = toMail

        htmlContent = MIMEText(content, 'html')
        message.attach(htmlContent)

        server.sendmail(
            fromMail,
            toMail,
            message.as_string()
        )
        print("E-posta gönderildi!")
    except smtplib.SMTPException as e: 
        print(f"E-posta gönderimi sırasında hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmedik farklı bir hata oluştu: {e}")
    finally:
        server.quit()


