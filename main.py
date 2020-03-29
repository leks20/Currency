import os
import smtplib
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv()

password = os.getenv('password')
email = os.getenv('email')


class Currency:
    dollar_url = 'https://www.google.com/search?client=ubuntu&hs=q2r&sxsrf=ALeKk01-uwN87q4OeSihO3wxpBmlnli_VA%3A1585393879586&ei=1zB_XpW3I8-T8gLSlp_oBA&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeMgYIABAHEB4yAggAMgIIADIGCAAQBxAeMgIIADIGCAAQBxAeMgIIADICCAA6BAgAEEc6BwgjELECECc6DAgjELACECcQRhCCAjoECAAQDToJCAAQQxBGEIICUIWiBli2zQZgwtUGaABwAngAgAH-AYgBzQeSAQUwLjUuMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjV_pW4hL3oAhXPiVwKHVLLB00Q4dUDCAs&uact=5'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'}

    current_converted_price = 0
    difference = 3

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(',', '.'))

    def get_currency_price(self):
        full_page = requests.get(self.dollar_url, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.find_all('span', {
            'class': 'DFlfde SwHCTb', 'data-precision': '2'
            }
            )
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(',', '.'))
        if currency >= self.current_converted_price + self.difference:
            print("Курс доллара сильно вырос!")
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print("Курс доллара сильно упал!")
            self.send_mail()
        print('Курс доллара на текущий момент = ' + str(currency))

        time.sleep(60)
        self.check_currency()

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()  # шифрование с помощью протокола TLS
        server.ehlo()

        server.login(email, password)
        subject = 'Warning!'
        body = 'The dollar exchange rate has changed!'
        message = 'Subject: {}\n\n{}'.format(subject, body)

        server.sendmail(
            'example@gmail.com',
            email,
            message
        )
        server.quit()


currency = Currency()

currency.check_currency()
