import datetime
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(filename="chat_log.txt", level=logging.INFO)

API_KEY = "13673394ad7c3440e349cb7b4f5c2df0"  # Replace with your actual OpenWeatherMap API key

def log_conversation(message):
    logging.info(f"{datetime.datetime.now()} - {message}")

@app.route("/greet", methods=["POST"])
def greet_user():
    user_name = request.json.get("name", "Guest")
    greeting = f"Hello, {user_name}! Nice to meet you."
    log_conversation(f"User greeted with name: {user_name}")
    return jsonify({"response": greeting})

@app.route("/weather", methods=["POST"])
def get_weather():
    city = request.json.get("city", "")
    if not city:
        return jsonify({"error": "Please provide a city name."}), 400

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            weather_info = f"The weather in {city} is {weather} with a temperature of {temperature}°C."
        else:
            weather_info = f"Could not retrieve weather data for '{city}'. Please check the city name."
            
        log_conversation(f"User asked about weather in {city}. Bot response: {weather_info}")
        return jsonify({"response": weather_info})
    except requests.RequestException as e:
        error_message = "Error: Unable to connect to the weather service."
        log_conversation(f"Weather API request failed: {e}")
        return jsonify({"error": error_message}), 500

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    operation = data.get("operation")
    num1 = data.get("num1")
    num2 = data.get("num2")

    try:
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = num1 / num2
        else:
            raise ValueError("Invalid operation")

        response_message = f"The result of {operation} is {result}."
        log_conversation(f"User asked for {operation} of {num1} and {num2}. Bot response: {response_message}")
        return jsonify({"response": response_message})
    except (ValueError, ZeroDivisionError) as e:
        error_message = f"Error: {str(e)}"
        log_conversation(f"Bot response: {error_message}")
        return jsonify({"error": error_message}), 400

@app.route("/exit", methods=["POST"])
def exit_chat():
    log_conversation("User exited the chat.")
    return jsonify({"response": "Goodbye!"})

if __name__ == "__main__":
    app.run(debug=True)
