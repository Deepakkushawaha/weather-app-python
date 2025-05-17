import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os

def get_weather():
    city = city_entry.get().strip().title()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    api_key = "b8bbbca3165483cb8108e05d5a8e1b79"  # Replace with your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 404:
            messagebox.showerror("Error", "City not found.")
            return
        elif response.status_code == 401:
            messagebox.showerror("Error", "Invalid API Key.")
            return

        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['main'].lower()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        result_label.config(
            text=f"{city}\n\n🌡️ Temp: {temp} °C\n☁️ Weather: {weather.title()}\n💧 Humidity: {humidity}%\n🌬️ Wind: {wind_speed} m/s"
        )

        icon_path = f"assets/{weather}.png"
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).resize((80, 80))
            icon_img_tk = ImageTk.PhotoImage(icon_img)
            icon_label.config(image=icon_img_tk)
            icon_label.image = icon_img_tk
        else:
            icon_label.config(image='')

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather: {e}")

# GUI setup
root = tk.Tk()
root.title("🌤️ Weather Dashboard")
root.geometry("420x560")
root.resizable(False, False)

# Background
bg_img = Image.open("assets/background.png").resize((420, 560))
bg_img_tk = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)

# Card with soft white background (compatible color)
card = tk.Frame(root, bg="#f8f8f8", bd=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=300, height=400)

# Title
title = tk.Label(card, text="Weather App", font=("Helvetica", 20, "bold"), bg="#f8f8f8", fg="#333")
title.pack(pady=10)

# Input field
city_entry = tk.Entry(card, font=("Helvetica", 14), justify="center", bd=1)
city_entry.pack(pady=10)
city_entry.insert(0, "Vadodara")

# Button
tk.Button(card, text="Check Weather", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=get_weather).pack(pady=5)

# Icon placeholder
icon_label = tk.Label(card, bg="#f8f8f8")
icon_label.pack(pady=10)

# Result text
result_label = tk.Label(card, text="", font=("Helvetica", 12), justify="center", bg="#f8f8f8", fg="#333")
result_label.pack(pady=10)

root.mainloop()
