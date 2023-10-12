# Apple Stock Checker 🍏
Automated stock checker that monitors the availability of Apple products in specified stores, and notifies users through Discord when items are in stock.

![Apple Stock](https://cdn.discordapp.com/attachments/706954905432227896/1162048465724002324/image.png?ex=653a84f8&is=65280ff8&hm=c5296f68c494ef69523695a91bf1214071e684e7a48a6230d40c9475c92b92f0&)

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Getting Your Discord Webhook](#getting-your-discord-webhook)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Contribution](#contribution)
7. [License](#license)

## Features

- Monitors Apple's stock for specified product model numbers.
- Notifies users through Discord when items are in stock at specified stores.
- Uses an enhanced logging mechanism with color-coded logs for better visibility.
- Resilient against network issues with built-in retry mechanisms.
- Uses environment variables for configuration, ensuring security and scalability.

## Requirements

- Python 3.x
- Required libraries: `requests`, `discord_webhook`, `json`, `logging`, `os`, and `random`.
- [pipenv](https://pipenv.pypa.io/en/latest/): Python dependency manager if you want to use a virtual

## Getting Your Discord Webhook

1. Open Discord and go to the desired channel where you want to receive notifications.
2. Click on the gear icon next to the channel name (`Edit Channel`).
3. In the left sidebar, click on `Integrations`.
4. Click on the `Webhooks` option and then `New Webhook`.
5. Customize the name, channel, and avatar as desired.
6. Copy the `Webhook URL` and use it as the `WEBHOOK_URL` environment variable in the setup.

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your_username/apple-stock-checker.git
   cd apple-stock-checker
   ```

2. **Install required Python libraries with pip**:

   ```bash
   pip install requests discord_webhook
   ```
3. **Install dependencies and shell if you are using pipenv**:

   ```bash
   pipenv install
   ```

     ```bash
   pipenv shell
   ```
   
4. **Set up your environment variables**. This tool relies on environment variables for configuration to keep sensitive and dynamic information secure.

   ```bash
   export WEBHOOK_URL="your_discord_webhook_url"
   export USER_AGENT="your_desired_user_agent"
   export MODEL_NUMBERS="MU663LL/A,MU6A3LL/A,..."
   export SPECIFIED_STORES="Aventura,Brickell,..."
   export ZIP_CODE="your_zip_code"
   ```

   Remember to replace placeholders with your actual information.

## Usage

Run the script with:

```bash
python stock_checker.py
```

Or if you usinf pipenv:

```bash
pipenv run python stock_checker.py
```

Monitor the logs for information on stock availability for specific models, I used this to get the iPhone 15 Pro Max on day one @ the store.

## Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. Ensure your PRs improve the project functionality, structure, or content.

## License

[MIT](https://choosealicense.com/licenses/mit/)
