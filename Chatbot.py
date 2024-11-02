import datetime
import logging
import requests

class ChatBot:
    def __init__(self):
        self.conversation_log = "chat_log.txt"
        self.api_key = "13673394ad7c3440e349cb7b4f5c2df0"  # Replace with your actual OpenWeatherMap API key
        logging.basicConfig(filename=self.conversation_log, level=logging.INFO)
        self.name = ""
        self.greet_user()

    def greet_user(self):
        print("Hello! I'm your assistant chatbot.")
        self.name = input("What's your name? ")
        logging.info(f"{datetime.datetime.now()} - User: {self.name} joined the conversation.")
        print(f"Nice to meet you, {self.name}!")

    def log_conversation(self, message):
        logging.info(f"{datetime.datetime.now()} - {message}")

    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                response_message = f"The weather in {city} is {weather} with a temperature of {temperature}°C."
            else:
                response_message = f"Could not retrieve weather data for '{city}'. Please check the city name."

        except requests.RequestException as e:
            response_message = "Error: Unable to connect to the weather service."
            logging.error(f"Weather API request failed: {e}")

        self.log_conversation(f"User asked about weather in {city}. Bot response: {response_message}")
        return response_message

    def perform_calculation(self, operation, num1, num2):
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
            
            response = f"The result of {operation} is {result}."
            self.log_conversation(f"User asked for {operation} of {num1} and {num2}. Bot response: {response}")
            return response
        except (ValueError, ZeroDivisionError) as e:
            error_message = f"Error: {str(e)}"
            self.log_conversation(f"Bot response: {error_message}")
            return error_message

    def chat(self):
        print("How can I assist you today? Type 'exit' to end the conversation.")
        while True:
            user_input = input("You: ").lower()
            self.log_conversation(f"User input: {user_input}")
            
            if "weather" in user_input:
                city = input("Enter city name: ")
                print(self.get_weather(city))
            elif any(op in user_input for op in ["add", "subtract", "multiply", "divide"]):
                operation = input("Enter operation (add, subtract, multiply, divide): ").lower()
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                    print(self.perform_calculation(operation, num1, num2))
                except ValueError:
                    print("Please enter valid numbers.")
                    self.log_conversation("Invalid numbers provided by user.")
            elif user_input == "exit":
                print("Goodbye!")
                self.log_conversation("User exited the chat.")
                break
            else:
                print("Sorry, I didn't understand that. Please ask about the weather or math operations.")
                self.log_conversation("Bot could not understand the user input.")

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.chat()
