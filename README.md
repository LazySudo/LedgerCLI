# LedgerCLI: Personal Finance Dashboard

LedgerCLI is a local-first, command-line interface tool designed for personal financial management (PFM). It aggregates transaction data from connected financial institutions to provide users with a consolidated view of their cash flow.

**Note:** This project is currently in active development.

## 🚀 Features
* **Unified Account View:** Aggregates balances from checking, savings, and credit card accounts.
* **Privacy-First Architecture:** Financial data is stored locally in SQLite. External transmission is limited strictly to Plaid (for fetching data) and optionally Google Gemini (for categorization).
* **Smart Categorization (Optional):** Users can bring their own Google AI Key to intelligently categorize transactions.
* **Read-Only Access:** The application requests strictly read-only permissions (Transactions & Balance). It cannot move funds.

## 📦 Installation
1. `git clone https://github.com/yourusername/LedgerCLI.git`
2. `pip install -r requirements.txt`
3. Configure `.env` with your Plaid credentials.

## 📄 License
MIT License.
"""

PRIVACY_CONTENT = """
# Privacy Policy for LedgerCLI

**Effective Date:** December 1, 2025

## 1. Data Collection
LedgerCLI collects financial transaction data specifically for personal budgeting.

## 2. Data Storage
All data is stored locally (`db.sqlite3`). **No data is transmitted to external servers.**

## 3. Third-Party Access
LedgerCLI does not share user data. Connection to financial institutions is handled directly via Plaid.
"""