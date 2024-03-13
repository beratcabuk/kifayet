import sys
from chatbot import Bot
from driver import GoogleShopping

def main():
    if len(sys.argv) == 1:
        print("Please supply an image file.\nTo get help, try: kifayet -h")
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("usage: kifayet filename")
        sys.exit(0)
    else:
        # Check if filename points to an image.
        if sys.argv[1][-4:] not in {'.png', '.jpg'}:
            print('The file must be of a png/jpg image!')
            sys.exit(1)

        file_name = sys.argv[1]
        bot = Bot()
        gs = GoogleShopping()

        # Encode the image to base64
        encoded_image = bot.encode_image(file_name)
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