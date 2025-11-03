#This class is responsible for sending notifications with the deal flight details.
import os
import smtplib

class NotificationManager:
    def __init__(self):
        self.MY_EMAIL =  os.getenv("MY_EMAIL")
        self.MY_EMAIL_PASSWORD = os.getenv("MY_EMAIL_PASSWORD")

    def send_smtp_message(self, phone_number, message):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=self.MY_EMAIL, password=self.MY_EMAIL_PASSWORD)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=f"{phone_number}@vtext.com",
                                msg=f"Subject: Low Price Alert!\n\n{message}")
            connection.close()