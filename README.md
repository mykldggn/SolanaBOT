## Overview
This Python script is designed to streamline the analysis of memecoins by integrating several functionalities into one cohesive workflow. It:

1. **Scrapes token data from GMGN**.
2. **Validates tokens against predefined criteria** such as liquidity, volume, age, and holders.
3. **Verifies the token's safety** using RugCheck.
4. **Analyzes the token's Twitter engagement and activity** using TweetScout.
5. **Notifies you via Telegram** if the token passes all checks.

---

## Features
- **Data Scraping**: Fetches real-time data from GMGN to identify potential tokens.
- **Criteria Validation**: Filters tokens based on:
  - Liquidity (< $100,000)
  - Volume (< $250,000)
  - Age (>= 24 hours)
  - Holders (≤ 300)
- **Safety Verification**: Ensures the token has a RugCheck score of "Good" or "Excellent."
- **Engagement Analysis**: Uses TweetScout to determine engagement scores and influencer activity.
- **Telegram Notifications**: Sends token details to your Telegram bot if all criteria are met.

---

## Setup
### Prerequisites
- Python 3.8+
- Install the required libraries:
  ```bash
  pip install requests beautifulsoup4 pandas
  ```

### Configuration
1. Replace placeholders with your actual values:
   - `YOUR_TELEGRAM_BOT_TOKEN`: Telegram bot token.
   - `YOUR_CHAT_ID`: Your Telegram chat ID.
2. Ensure API endpoints are correct:
   - RugCheck: `https://rugcheck.xyz/api/check`
   - TweetScout: `https://tweetscout.io/api/check`
   - GMGN: Update `url_gmgn` with the correct URL if needed.

---

## How It Works
1. **Fetch Data**:
   - Scrapes token data from GMGN's table structure.
   - Extracts details like liquidity, volume, holders, age, and contract address.

2. **Validate Criteria**:
   - Filters tokens based on predefined thresholds.

3. **RugCheck Validation**:
   - Submits the token's contract address to RugCheck for a safety score.

4. **Twitter Analysis**:
   - Analyzes Twitter activity for engagement scores and influencer impact.

5. **Telegram Notifications**:
   - Sends detailed information about the token to your Telegram chat.

---

## Execution
Run the script:
```bash
python comprehensive_token_script.py
```

---

## Output
If a token meets all checks, the following information is sent to Telegram:
- Token Name
- Contract Address
- Liquidity
- Volume
- Age (hours)
- Holders
- Engagement Score
- RugCheck Score

---

## Notes
- Ensure the APIs used (RugCheck, TweetScout) support the expected data structure.
- Validate GMGN's table structure to adjust the scraping logic if required.
- Debugging logs are printed for tokens that fail criteria or API checks.

---

## Limitations
- Requires updates if API endpoints or GMGN structure changes.
- Dependent on the availability of external services (RugCheck, TweetScout).
- Room for future improvements:
✦ Number of whales holding the token
✦ Has the dev sold their tokens?
✦ Is the Dex paid or not?
---
