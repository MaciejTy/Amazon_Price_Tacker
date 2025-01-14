from email.mime.text import MIMEText
import lxml

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")

header = {"Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
response = requests.get(url, headers=header)

amazon_wbs = response.content
soup = BeautifulSoup(amazon_wbs, "html.parser")

# print(soup.prettify())

price_whole = soup.find(name="span", class_="a-price-whole").text
price_fraction = soup.find(name="span", class_="a-price-fraction").text
price = float(price_whole + price_fraction)

BUY_PRICE = float(100)
title = soup.find(id="productTitle").get_text().strip()


if price < BUY_PRICE:
    try:
        subject = f"Amazon Price Alert!"
        body = (f"{title} costs only {price}.!"
                f"{url}")
        message = MIMEText(body, "plain", "utf-8")
        message["From"] = EMAIL_ADDRESS
        message["To"] = EMAIL_ADDRESS
        message["Subject"] = subject

        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            result = connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS, msg=message.as_string())
    except Exception as e:
        print(f"Wystąpił błąd: {e}")