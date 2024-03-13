import base64
import requests


class Bot:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_image(self, image_path: str) -> str:
        """
        Reads the images and converts them into base64 encoded bytes -> strings.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def respond(self, base64_image: str) -> list[str]:
        """
        Takes base64 converted images and extracts search keywords for
        the outfits. Returns a list of keywords, one item for each piece of
        clothing.
        """
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
    api_key = input('Please enter your API key...\n')
    bot = Bot(api_key)
    encoded_img = bot.encode_image(img_path)
    search_keywords = bot.respond(encoded_img)
    assert type(search_keywords) is list
    assert type(search_keywords[0]) is str
    print('Here are the search keywords...\n', search_keywords)
