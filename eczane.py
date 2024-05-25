import tkinter as tk
from tkinter import messagebox
import http.client
import json
from urllib.parse import quote

def get_duty_pharmacies(city, district):
    try: #HTTP isteği control 
        conn = http.client.HTTPSConnection("api.collectapi.com")

        headers = {
            'content-type': "application/json",
            'authorization': "apikey 2RcvucbHNkTiihlVJjjyZq:0wkLpKwAaaeg5Kzz8GUuwU"
        }

        encoded_district = quote(district, safe='')
        encoded_city = quote(city, safe='')
        query = f"/health/dutyPharmacy?ilce={encoded_district}&il={encoded_city}"

        conn.request("GET", query, headers=headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")

        conn.close()

        return json.loads(data)
    except http.client.HTTPException as e:
        print(f"HTTP isteği sırasında hata oluştu: {e}")
        return {"success": False}
    except Exception as e:
        print(f"Farklı bir hata oluştu: {e}")
        return {"success": False}

def show_duty_pharmacies():
    city = city_entry.get()
    district = district_entry.get()
    
    if city.strip() == "" or district.strip() == "":
        messagebox.showerror("Hata", "Lütfen şehir ve ilçe bilgisini girin.")
        return
    
    duty_pharmacies = get_duty_pharmacies(city, district)
    
    if 'success' in duty_pharmacies and duty_pharmacies['success']:
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Nöbetçi Eczaneler ({city}, {district}):\n\n")
        for pharmacy in duty_pharmacies['result']:
            result_text.insert(tk.END, f"{pharmacy['name']} - {pharmacy['address']}\n")
        result_text.config(state="disabled")
    else:
        messagebox.showerror("Hata", "Nöbetçi eczaneler alınamadı. Lütfen girdiğiniz şehir ve ilçeyi kontrol edin.")

root = tk.Tk()
root.title("Nöbetçi Eczane Sorgulama")
root.resizable(False, False)

city_label = tk.Label(root, text="Şehir:", font=("Helvetica", 12))
city_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

district_label = tk.Label(root, text="İlçe:", font=("Helvetica", 12))
district_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

city_entry = tk.Entry(root, width=35)
city_entry.grid(row=0, column=1, padx=5, pady=5)

district_entry = tk.Entry(root, width=35)
district_entry.grid(row=1, column=1, padx=5, pady=5)

search_button = tk.Button(root, text="Sorgula", command=show_duty_pharmacies, font=("Helvetica", 10))
search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

result_text = tk.Text(root, width=50, height=15, state="disabled")
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
