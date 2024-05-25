import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess
import pygame
import webbrowser
import sendMail


weather_url = "https://havadurumupython.netlify.app/"

def havaDurumu():
    webbrowser.open(weather_url, new="chrome")  # Tarayıcıyı belirtin

def indirim():
    subprocess.Popen(['python', 'indirim.py'])

def eczane():
    root.destroy()
    subprocess.Popen(['python', 'eczane.py'])

def play_sound():
    pygame.mixer.init()
    collision_sound = pygame.mixer.Sound('ses.ogg')
    collision_sound.play()

#ARAYÜZ KODLARI-------------------
root = tk.Tk()
root.title("Menü")
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.resizable(False, False)

def disable_fullscreen(event=None):
    return "break"

root.bind("<F11>", disable_fullscreen)
root.bind("<Escape>", disable_fullscreen)

background_image_path = "bg.png"
bg_img = Image.open(background_image_path)
bg_img = bg_img.resize((500, 400))
background_image = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_image, anchor="nw")

image_hava = "hava.png"
image_indirim = "indirim.png"
image_eczane = "eczane.png"

img_hava = Image.open(image_hava)
img_hava = img_hava.resize((100, 100))
hava_img = ImageTk.PhotoImage(img_hava)

img_indirim = Image.open(image_indirim)
img_indirim = img_indirim.resize((100, 100))
indirim_img = ImageTk.PhotoImage(img_indirim)

indirim_eczane = Image.open(image_eczane)
indirim_eczane = indirim_eczane.resize((100, 100))
eczane_img = ImageTk.PhotoImage(indirim_eczane)


button1 = tk.Button(root, image=hava_img, command=lambda: [play_sound(), havaDurumu()], borderwidth=0, highlightthickness=0)
button1_window = canvas.create_window(100, 180, anchor="center", window=button1)

button2 = tk.Button(root, image=indirim_img, command=lambda: [play_sound(), indirim()], borderwidth=0, highlightthickness=0)
button2_window = canvas.create_window(250, 180, anchor="center", window=button2)

button3 = tk.Button(root, image=eczane_img, command=lambda: [play_sound(), eczane()], borderwidth=0, highlightthickness=0)
button3_window = canvas.create_window(400, 180, anchor="center", window=button3)

root.mainloop()