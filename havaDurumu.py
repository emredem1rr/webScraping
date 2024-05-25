from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Hava durumu -------------------------------------------------------------------------

def get_weather(city): # Hava durumu bilgileri alma yeri
    api_key = '3cd3a9180e7a29cb8e33bafb5eff91a0'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=tr"
    
    try: # HTTP hatalarını kontrol etmek için
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        if response.status_code == 200:
            weather_info = {
                "city": data["name"] + ", " + data["sys"]["country"],
                "temperature": int(data["main"]["temp"]),
                "description": translate_description(data["weather"][0]["description"]).capitalize(),
                "minmax": str(int(data["main"]["temp_min"])) + "°C / " + str(int(data["main"]["temp_max"])) + "°C"
            }
            return weather_info
        else:
            return None
    except requests.RequestException as e:
        print(f"HTTP isteği sırasında hata oluştu: {e}")
        return None
    except Exception as e:
        print(f"Farklı bir hata oluştu: {e}")
        return None

def translate_description(description): # Tr çevirisi
    translations = {
        "clear sky": "Açık Hava",
        "few clouds": "Az Bulutlu",
        "scattered clouds": "Parçalı Bulutlu",
        "broken clouds": "Yer Yer Bulutlu",
        "shower rain": "Sağanak Yağmur",
        "rain": "Yağmurlu",
        "thunderstorm": "Gök Gürültülü Sağanak Yağmur",
        "snow": "Karlı",
        "mist": "Sisli"
    }
    return translations.get(description.lower(), description)

@app.route('/') # Başlatma yeri
def index():
    return render_template('havaDurumu.html')

@app.route('/get_weather')
def get_weather_route():
    city = request.args.get('city')  # Kullanıcının girdiği şehiri alma
    weather_data = get_weather(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Hava durumu bilgisi alınamadı."}), 500

if __name__ == '__main__':
    app.run(debug=True)
