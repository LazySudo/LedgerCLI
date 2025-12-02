# LedgerCLI: Personal Finance Dashboard

LedgerCLI is a local-first, command-line interface tool designed for personal financial management (PFM). It aggregates transaction data from connected financial institutions and optionally uses AI to provide categorized insights.

**Note:** This project is currently in active development.

## 🚀 Features

* **Unified Account View:** Aggregates balances from checking, savings, and credit card accounts.
* **Smart Categorization (Optional):** Users can provide a Google Gemini API Key to intelligently categorize uncategorized transactions.
* **Privacy-First Architecture:** Financial data is stored locally in SQLite. External transmission is limited strictly to Plaid (for fetching data) and Google Gemini (if AI is enabled).
* **Read-Only Access:** The application requests strictly read-only permissions from Plaid. It cannot move funds.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Database:** SQLite3
* **Bank API:** Plaid
* **AI Engine:** Google Gemini (Generative AI)

## 📦 Installation

1.  Clone the repository.
2.  `pip install -r requirements.txt`
3.  Configure `.env` with your credentials.

## ⚙️ Configuration

Copy `.env.example` to `.env`:

```ini
PLAID_CLIENT_ID="your_plaid_id"
PLAID_SECRET="your_plaid_secret"
PLAID_ENV="development"
# Optional: Leave blank to disable AI features
GEMINI_API_KEY="your_google_ai_key"
```
## Usage

1. Setup Connections
```bash
python main.py link
```

2. Sync Transactions
```bash
python main.py sync
```

3. Generate AI Report:
```bash
python main.py analyze
```

