import smtplib
from bs4 import BeautifulSoup
import requests
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def main():
    salesList = scarpSite()
    createCSV(salesList)
    sendEmail()
    print("Done")

def getInfo(website, list):
    result = requests.get(website)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')

    for el in soup.find_all('div', attrs={'class': 'productPriceInfoWrap'}):
        saleItem = el.find('span', class_='salePrice item-unit-price')
        if saleItem != None:
            price = el.find('span', class_='salePrice item-unit-price').get_text()
            name = el.find('span', class_='real-product-name').get_text()
            price = price.strip('\t\r\n')
            # Strip twice to remove whitespace as well as newlines
            price = price.strip()
            product = {
            'name': name,
            'price': price
            }
            list.append(product)

def scarpSite():
    beef = "https://www.hannaford.com/departments/meat/beef?displayAll=true"
    pork = "https://www.hannaford.com/departments/meat/pork?displayAll=true"
    chicken = "https://www.hannaford.com/departments/meat/chicken-turkey?displayAll=true"
    itemsOnSale = []
    
    getInfo(beef, itemsOnSale)
    getInfo(pork, itemsOnSale)
    getInfo(chicken, itemsOnSale)
    
    return itemsOnSale

def createCSV(list):
    field_names = ["name", "price"]

    with open('Names.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(list)
    
def sendEmail():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    from_email = ''
    to_email = ''
    subject = 'Hannaford Meat Sales'
    body = 'Here are the meat sales'

    msg = MIMEMultipart()
    body_part = MIMEText("Here are the sale items", 'plain')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
        # Add body to email
    msg.attach(body_part)

    with open(r"F:\Practice\Grocery-Discounts\Names.csv",'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name='Names.csv'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(from_email, smtp_password)
        smtp_server.sendmail(from_email, to_email, msg.as_string())

if __name__=="__main__":
    main()