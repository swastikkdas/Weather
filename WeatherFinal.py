import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import geocoder
import io

API_KEY = "API-KEY"

def get_location():
    g = geocoder.ip('me')
    return g.city or "Bhubaneswar"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return response

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return response.get("list", [])

def show_weather():
    city = entry.get() or get_location()
    weather = get_weather(city)

    if weather.get("main"):
        temp = weather["main"]["temp"]
        desc = weather["weather"][0]["description"].capitalize()
        icon_code = weather["weather"][0]["icon"]

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        img_data = requests.get(icon_url).content
        img = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)))
        icon_label.config(image=img)
        icon_label.image = img

        weather_label.config(text=f"{city}\nTemperature: {temp}°C\n{desc}")
        show_forecast(city)
    else:
        messagebox.showerror("Error", "City not found or API error.")

def show_forecast(city):
    forecast_list = get_forecast(city)
    forecast_text.delete("1.0", tk.END)
    forecast_text.insert(tk.END, f"📅 5-Day Forecast:\n\n")

    days_added = set()
    for item in forecast_list:
        time = item["dt_txt"]
        if "12:00:00" in time:  # Only show midday
            date = time.split(" ")[0]
            if date not in days_added:
                desc = item["weather"][0]["description"].capitalize()
                temp = item["main"]["temp"]
                forecast_text.insert(tk.END, f"{date}: {temp}°C - {desc}\n")
                days_added.add(date)

# GUI Setup
app = tk.Tk()
app.title("🌦️ Weather Forecast App")
app.geometry("400x550")
app.resizable(False, False)

tk.Label(app, text="Enter City or Leave Blank for Auto-Detect:", font=("Arial", 10)).pack(pady=10)
entry = tk.Entry(app, font=("Arial", 12))
entry.pack()

tk.Button(app, text="Get Weather", command=show_weather, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

icon_label = tk.Label(app)
icon_label.pack()

weather_label = tk.Label(app, text="", font=("Arial", 14), justify="center")
weather_label.pack(pady=10)

forecast_text = tk.Text(app, height=10, width=45, font=("Arial", 10))
forecast_text.pack(pady=10)

app.mainloop()
