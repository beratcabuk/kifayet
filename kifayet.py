import sys
from chatbot import Bot
from driver import GoogleShopping


def main():
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("usage: kifayet img_file apikey_file")
        sys.exit(0)
    elif len(sys.argv) != 3:
        print("Please supply an image file and a file with the API key.\nTo get help, try: kifayet -h")
    else:
        # Check if filename points to an image.
        if sys.argv[1][-4:] not in {'.png', '.jpg'}:
            print('The file must be of a png/jpg image!')
            sys.exit(1)

        img_file_name, api_key_file_name = sys.argv[1], sys.argv[2]
        # Read the api key from the indicated file
        with open(api_key_file_name, 'r') as f:
            api_key = f.read()
            f.close()

        bot = Bot(api_key)
        gs = GoogleShopping()

        # Encode the image to base64
        encoded_image = bot.encode_image(img_file_name)
        # Send the image to openai, get the keywords
        keywords = bot.respond(encoded_image)
        # Get the links that match to the keywords
        links = gs.keywords_to_links(keywords)
        # Export the links to a file.
        with open('links.txt', mode='w') as outfile:
            outfile.write('\n'.join(links))
            outfile.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
