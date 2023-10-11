# Apple Stock Checker 🍏
Automated stock checker that monitors the availability of Apple products in specified stores, and notifies users through Discord when items are in stock.

![Apple Logo](https://your_link_to_an_image/if_you_have_one.png)

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Contribution](#contribution)
6. [License](#license)

## Features

- Monitors Apple's stock for specified product model numbers.
- Notifies users through Discord when items are in stock at specified stores.
- Uses an enhanced logging mechanism with color-coded logs for better visibility.
- Resilient against network issues with built-in retry mechanisms.
- Uses environment variables for configuration, ensuring security and scalability.

## Requirements

- Python 3.x
- Required libraries: `requests`, `discord_webhook`, `json`, `logging`, `os`, and `random`.

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your_username/apple-stock-checker.git
   cd apple-stock-checker
   ```

2. **Install required Python libraries**:

   ```bash
   pip install requests discord_webhook
   ```

3. **Set up your environment variables**. This tool relies on environment variables for configuration to keep sensitive and dynamic information secure.

   ```bash
   export WEBHOOK_URL="your_discord_webhook_url"
   export USER_AGENT="your_desired_user_agent"
   export MODEL_NUMBERS="MU663LL/A,MU6A3LL/A,..."
   export SPECIFIED_STORES="Aventura,Waterside Shops,..."
   export ZIP_CODE="your_zip_code"
   ```

   Remember to replace placeholders with your actual information.

## Usage

Run the script with:

```bash
python stock_checker.py
```

Monitor the logs for information on stock availability for specific models, I used this to get the iPhone 15 Pro Max on day one @ the store.

## Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. Ensure your PRs improve the project functionality, structure, or content.

## License

[MIT](https://choosealicense.com/licenses/mit/)

