import os
from dotenv import load_dotenv
import base64
import requests


load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

class Bot:
    def __init__(self) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

    def encode_image(self, image_path: str) -> bytes:
        '''Reads the images and converts them into base64 encoded bytes.'''
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def respond(self, base64_image: bytes) -> list[str]:
        '''
        Takes base64 converted images and extracts search keywords for
        the outfits. Returns a list of keywords, one item for each piece of
        clothing.
        '''
        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": """Provide me with keywords I can use to search for and 
                        buy this person's clothes to replicate their look.
                        Give only one set of keywords for each article of 
                        clothing, seperated by commas."""
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", 
                                 headers=self.headers, json=payload)
        msg = response.json()['choices'][0]['message']['content']
        search_keywords = msg.split(', ')
        return search_keywords

if __name__ == '__main__':
    img_path = input('Please enter the path to the image...\n')
    bot = Bot()
    encoded_img = bot.encode_image(img_path)
    search_keywords = bot.respond(encoded_img)
    assert type(search_keywords) == list
    assert type(search_keywords[0]) == str
    print('Here are the search keywords...\n', search_keywords)
