# claude_client.py
import requests
import json

class ClaudeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://api.anthropic.com/v1/messages'
        self.headers = {
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def send_message(self, message):
        data = {
            'model': 'claude-3-5-sonnet-20240620',
            'max_tokens': 1024,
            'messages': [{'role': 'user', 'content': message}]
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            print(result['content'])
            print(result['content'][0]['text'])
            return result['content'][0]['text'] #response.json()['text']
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"