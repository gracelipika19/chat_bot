import unittest
from unittest.mock import patch
from chatbot_api import ChatBot

class TestChatBot(unittest.TestCase):
    def setUp(self):
        """Set up a ChatBot instance for testing."""
        self.chatbot = ChatBot()
        
    @patch("chatbot_api.requests.get")
    def test_get_weather(self, mock_get):
        """Test the get_weather function with a mocked API response."""
        # Mock response data
        mock_response = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 25}
        }
        
        # Configure the mock to return a response with JSON data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the function with a sample city name
        result = self.chatbot.get_weather("London")
        
        # Check if the response message is formatted correctly
        self.assertEqual(result, "The weather in London is clear sky with a temperature of 25°C.")

    def test_perform_calculation_addition(self):
        """Test perform_calculation for addition operation."""
        result = self.chatbot.perform_calculation("add", 10, 5)
        self.assertEqual(result, "The result of add is 15.0.")

    def test_perform_calculation_division_by_zero(self):
        """Test perform_calculation for division by zero error handling."""
        result = self.chatbot.perform_calculation("divide", 10, 0)
        self.assertEqual(result, "Error: Cannot divide by zero")

if __name__ == "__main__":
    unittest.main()
