import telebot
import requests
import json
from decouple import config

# Initialize the Telegram bot with the provided token
BOT = telebot.TeleBot(config("bot_token"))
API_KEY = config("api_key")

@BOT.message_handler(commands=["start"])
def start(message):
    BOT.send_message(message.chat.id, "Hi, tell me the city please.")

# Handle messages of content type "text"
@BOT.message_handler(content_types=["text"])
def send_weather(message):
    city = message.text.strip().lower()

    if city.isalpha():
        # Make an API request to OpenWeatherMap to get weather data for the city
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")

        if response.status_code == 200:
            data = json.loads(response.text)

            BOT.reply_to(message, f"Current weather in {city.capitalize()} is: {data['main']['temp']}°C.")

            # Determine the weather state and send an appropriate icon
            weather_state = data["weather"][0]["main"].lower() + ".png"
            photo = open("./" + weather_state, "rb")
            BOT.send_photo(message.chat.id, photo)
        else:
            BOT.send_message(message.chat.id, "City name was invalid, please try again.")
    else:
        BOT.send_message(message.chat.id, "City name can contain only English alphabet letters.")

# Handle messages of content types other than "text"
@BOT.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "voice"])
def no_text_handler(message):
    BOT.send_message(message.chat.id, "Please enter the city name as text.")

BOT.polling(none_stop=True)
