import requests
from bs4 import BeautifulSoup
from sendMail import sendMail
import time

url1 = "https://www.trendyol.com/pull-bear/dokulu-islemeli-kisa-kollu-sweatshirt-p-816187960?boutiqueId=61&merchantId=112044"
mail_sent = False 

def checkPrice(url, paramPrice):
    global mail_sent  

    if not mail_sent:  
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        try: # HTTP isteği başarılı bir şekilde gitti mi?
            page = requests.get(url, headers=headers)
            page.raise_for_status()  # HTTP hatalarını kontrol etmek için
        except requests.RequestException as e:
            print(f"HTTP isteği sırasında hata oluştu: {e}")
            return

        htmlPage = BeautifulSoup(page.content, 'html.parser')

       
        productTitle = htmlPage.find("h1", class_="pr-new-br").getText() 
        price = htmlPage.find("span", class_="prc-dsc").getText()  

        image = htmlPage.find("img", {"src": "https://cdn.dsmcdn.com/ty1326/product/media/images/prod/QC/20240521/17/e067c066-ca99-3d0a-a448-4a53e21bb2bd/1_org_zoom.jpg"})  # ürün fotosu
        if image:
            image['width'] = '300'
            image['height'] = '400'
            image_html = str(image)
        else:
            image_html = "<p>Ürün resmi bulunamadı.</p>"

        convertedPrice = float(price.replace(",", ".").replace(" TL", ""))

        if convertedPrice <= paramPrice:
            print("Ürün fiyatı düştü!")
            htmlEmailContent = f"""
                <html>
                <head></head>
                <body>
                <h3>{productTitle}</h3>
                <br/>
                {image_html}
                <br/>
                <p>Ürün linki: {url}</p>
                </body>
                </html>
                """
            try: # mail başarılı bir şekilde gönderildi mi?
                sendMail("demire773@gmail.com", "Ürünün fiyatı düştü!!🥳🎉", htmlEmailContent)
                mail_sent = True
            except Exception as e:
                print(f"E-posta gönderimi sırasında hata oluştu: {e}")
        else:
            print("Ürün fiyatı düşmedi :(")
        

while not mail_sent:
    checkPrice(url1, 800) 
    time.sleep(3)
