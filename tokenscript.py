import requests
from bs4 import BeautifulSoup
import pandas as pd

# Telegram bot configuration
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token
telegram_chat_id = "YOUR_CHAT_ID"  # Replace with your chat ID
telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

# API URLs
rugcheck_url = "https://rugcheck.xyz/api/check"  # Replace with the actual RugCheck API endpoint
tweetscout_url = "https://tweetscout.io/api/check"  # Replace with the actual TweetScout API endpoint

# Function to fetch data from GMGN
url_gmgn = "https://gmgn.com/popular-tokens"  # Replace with the actual GMGN URL
def fetch_gmgn_data():
    try:
        response = requests.get(url_gmgn, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        tokens = []
        rows = soup.select("table.token-table tbody tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) > 0:
                token_data = {
                    "Token Name": columns[0].get_text(strip=True),
                    "Liquidity": float(columns[4].get_text(strip=True).replace(',', '').replace('$', '')),
                    "Volume": float(columns[1].get_text(strip=True).replace(',', '').replace('$', '')),
                    "Age (hours)": int(columns[5].get_text(strip=True).replace(' hours', '')),
                    "Holders": int(columns[6].get_text(strip=True).replace(',', '')),
                    "Contract Address": columns[7].get_text(strip=True)
                }
                tokens.append(token_data)
        return tokens
    except Exception as e:
        print(f"Error fetching GMGN data: {e}")
        return []

# Function to check safety report via RugCheck
def check_rugcheck(contract_address):
    try:
        response = requests.post(rugcheck_url, json={"contract_address": contract_address})
        response.raise_for_status()
        data = response.json()
        return data if "score" in data and data["score"].lower() in ["good", "excellent"] else None
    except requests.exceptions.RequestException as e:
        print(f"Error checking RugCheck for {contract_address}: {e}")
        return None

# Function to fetch Twitter engagement via TweetScout
def check_twitter_engagement(twitter_handle):
    try:
        response = requests.post(tweetscout_url, json={"twitter_handle": twitter_handle})
        response.raise_for_status()
        data = response.json()
        return data if data and "engagement_score" in data else None
    except requests.exceptions.RequestException as e:
        print(f"Error checking TweetScout for {twitter_handle}: {e}")
        return None

# Function to send a message to the Telegram bot
def send_to_telegram(message):
    try:
        response = requests.post(telegram_url, json={"chat_id": telegram_chat_id, "text": message})
        response.raise_for_status()
        print("Message sent to Telegram successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

# Main function to combine all steps
def main():
    print("Fetching data from GMGN...")
    tokens = fetch_gmgn_data()

    for token in tokens:
        print(f"Checking token {token['Token Name']} with CA {token['Contract Address']}...")

        if (
            token["Liquidity"] < 100000 and
            token["Volume"] < 250000 and
            token["Age (hours)"] >= 24 and
            token["Holders"] <= 300
        ):
            print("Token meets criteria. Verifying with RugCheck...")
            rugcheck_result = check_rugcheck(token["Contract Address"])

            if rugcheck_result:
                print("RugCheck passed. Checking Twitter engagement...")
                twitter_data = check_twitter_engagement(token['Token Name'])  # Replace with actual handle extraction

                if twitter_data:
                    message = (
                        f"Token Passed All Checks:\n"
                        f"Name: {token['Token Name']}\n"
                        f"Contract Address: {token['Contract Address']}\n"
                        f"Liquidity: {token['Liquidity']}\n"
                        f"Volume: {token['Volume']}\n"
                        f"Age (hours): {token['Age (hours)']}\n"
                        f"Holders: {token['Holders']}\n"
                        f"Engagement Score: {twitter_data['engagement_score']}\n"
                        f"RugCheck Score: {rugcheck_result['score']}"
                    )
                    send_to_telegram(message)
                else:
                    print("Twitter check failed.")
            else:
                print("RugCheck failed.")
        else:
            print("Token does not meet initial criteria.")

if __name__ == "__main__":
    main()
