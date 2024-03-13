import sys
from chatbot import Bot
from driver import GoogleShopping

def main():
    file_name = sys.argv[1]
    bot = Bot()
    gs = GoogleShopping()

    # Encode the image to base64
    encoded_image = bot.encode_image(file_name)
    # Send the image to openai, get the keywords
    keywords = bot.respond(encoded_image)
    # Get the links that match to the keywords
    links = gs.keywords_to_links(keywords)
    for link in links:
        print(link)
    sys.exit(0)


if __name__ == '__main__':
    main()