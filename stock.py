
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import logging
import os
import random

class ColoredFormatter(logging.Formatter):
    BLUE = '\033[94m'
    END = '\033[0m'

    def format(self, record):
        log_message = super().format(record)
        if "Checking stock for:" in log_message:
            return f"{self.BLUE}{log_message}{self.END}"
        return log_message

# Replace your existing logging setup with:
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
log = logging.getLogger('')
for hdlr in log.handlers[:]:  # remove all old handlers
    log.removeHandler(hdlr)
ch = logging.StreamHandler()
ch.setFormatter(ColoredFormatter(log_format))
log.addHandler(ch)

def fetch_configurations():
    return {
        'webhook_url': os.getenv('WEBHOOK_URL'),
        'user_agent': os.getenv('USER_AGENT'),
        'model_numbers': os.getenv('MODEL_NUMBERS').split(','),
        'specified_stores': os.getenv('SPECIFIED_STORES').split(','),
        'zip_code': os.getenv('ZIP_CODE')
    }

def retry_request(url, session, max_retries=3, backoff_factor=0.5):
    for i in range(max_retries):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if i == max_retries - 1:
                raise
            else:
                sleep_time = backoff_factor * (2 ** i)
                time.sleep(sleep_time)

def health_check(last_found_time, threshold=3600):
    current_time = time.time()
    if current_time - last_found_time > threshold:
        logging.warning("Haven't found stock for over an hour. Check if script is functioning correctly.")

class StockChecker:
    def __init__(self, webhook_url, user_agent, model_numbers, specified_stores, zip_code):
        self.webhook_url = webhook_url
        self.user_agent = user_agent
        self.model_numbers = model_numbers
        self.specified_stores = specified_stores
        self.zip_code = zip_code
        self.url_template = f"https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0={{}}&location={zip_code}"
        self.in_stock_tracker = {}
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})


    def send_discord_notification(self, title, description, image_url=None):
        """Sends an embedded message to the Discord webhook."""
        webhook = DiscordWebhook(url=self.webhook_url)
        embed = DiscordEmbed(title=title, description=description, color='43b581')
        if image_url:
            embed.set_thumbnail(url=image_url)
        webhook.add_embed(embed)
        try:
            webhook.execute()
            logging.info(f"Sent Discord notification: {title} - {description}")
        except Exception as e:
            logging.error(f"Failed to send Discord notification: {e}")

    def check_stock(self, model_number):
        """Checks the stock for a given model number and sends a notification if available."""
        url = self.url_template.format(model_number)
        try:
            response = retry_request(url, self.session)
            data = response.json()

            # More detailed logging:
            if 'body' not in data:
                logging.error("'body' key not found in JSON data.")
            elif 'content' not in data['body']:
                logging.error("'content' key not found in 'body' of JSON data.")
            elif 'pickupMessage' not in data['body']['content']:
                logging.error("'pickupMessage' key not found in 'content' of JSON data.")
            elif 'stores' not in data['body']['content']['pickupMessage']:
                logging.error("'stores' key not found in 'pickupMessage' of JSON data.")

            try:
                product_title = data['body']['content']['pickupMessage']['stores'][0]['partsAvailability'][model_number].get('messageTypes', {}).get('compact', {}).get('storePickupProductTitle', 'Unknown Product')
            except KeyError:
                logging.error("KeyError: Problem extracting 'storePickupProductTitle'.")
                return

            logging.info(f"Checking stock for: {product_title}")

            for store in data['body']['content']['pickupMessage']['stores']:
                if 'storeName' not in store:
                    logging.error("'storeName' key not found in 'store' of JSON data.")
                if 'partsAvailability' not in store:
                    logging.error("'partsAvailability' key not found in 'store' of JSON data.")
                if model_number not in store['partsAvailability']:
                    logging.error(f"'{model_number}' key not found in 'partsAvailability' of JSON data.")
                if 'pickupSearchQuote' not in store['partsAvailability'][model_number]:
                    logging.error("'pickupSearchQuote' key not found in model number details of JSON data.")

                try:
                    store_name = store['storeName']
                except KeyError:
                    logging.error("KeyError: 'storeName' not found.")
                    continue  # Skip to the next store

                try:
                    stock_status = store['partsAvailability'][model_number]['pickupSearchQuote']
                except KeyError:
                    logging.error(f"KeyError: 'pickupSearchQuote' not found for model: {model_number}")
                    continue  # Skip to the next store

                logging.info(f"{store_name}: {'In Stock' if stock_status.lower() != 'currently unavailable' else 'Out of Stock'}")

                if stock_status.lower() != "currently unavailable" and store_name in self.specified_stores:
                    # Ensure that the model number is in the tracker and that it's a dictionary.
                    if model_number not in self.in_stock_tracker:
                        self.in_stock_tracker[model_number] = {}

                    # If the specific store isn't in the tracker for the model or it's set to False
                    if store_name not in self.in_stock_tracker[model_number] or not self.in_stock_tracker[model_number].get(store_name):
                        title = f"Stock Alert: {product_title}"
                        content = f"Store: {store_name} \nAvailability: In Stock \n@everyone"
                        store_img = store.get('storeImageUrl')
                        self.send_discord_notification(title, content, store_img)
                        self.in_stock_tracker[model_number][store_name] = True
                    else:
                        self.in_stock_tracker[model_number][store_name] = False  # Set to False if the product is out of stock

        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            self.send_discord_notification("Stock Checker Error", f"Failed to retrieve data: {e}")

        except KeyError:
            logging.error("Unexpected response structure. Printing the response for debugging:")
            logging.error(json.dumps(data, indent=4))

    def monitor_stock(self, sleep_duration=240):
        """Monitors the stock continuously for the specified model numbers."""
        last_found_time = time.time()
        try:
            while True:
                for model_number in self.model_numbers:
                    self.check_stock(model_number)
                    time.sleep(random.randint(5, 15))
                health_check(last_found_time)
                time.sleep(sleep_duration)
        except KeyboardInterrupt:
            logging.info("Stopping stock monitoring...")

def main():
    config = fetch_configurations()
    checker = StockChecker(
        config['webhook_url'],
        config['user_agent'],
        config['model_numbers'],
        config['specified_stores'],
        config['zip_code']
    )
    checker.monitor_stock()

if __name__ == "__main__":
    main()
