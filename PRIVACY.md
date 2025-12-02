**`PRIVACY.md`**
*(Fixed the contradiction regarding external servers)*
```markdown
# Privacy Policy for LedgerCLI

**Effective Date:** December 1, 2025

## 1. Data Collection
LedgerCLI is a self-hosted, personal finance tool. It collects financial transaction data (amount, date, merchant, category) specifically for the purpose of personal budgeting.

## 2. Data Storage
* **Primary Storage:** All financial data retrieved via the Plaid API is stored locally on the user's machine in a secured SQLite database (`db.sqlite3`).
* **External Transmission:** Generally, no data is transmitted to external servers, cloud storage, or third-party analytics platforms, with the single exception of the optional AI feature described below.

## 3. Data Usage
Data is used solely for the following local operations:
* Calculating monthly spending totals.
* Categorizing expenses.
* Displaying historical trends in the CLI dashboard.

## 4. AI & Third-Party Processors
**Google Gemini (Generative AI):**
If the user enables AI features (by providing their own API Key), specific transaction descriptions and amounts are sent to Google's Gemini API for the sole purpose of categorization and spending analysis.
* Data sent to the AI model is **ephemeral** (stateless) and is not used to train Google's models.
* Users may opt out of this feature entirely by leaving the `GEMINI_API_KEY` blank.

## 5. Plaid Integration
Connection to financial institutions is handled directly between the local client and Plaid. LedgerCLI does not see, store, or transmit your online banking credentials. Access is managed via secure OAuth tokens.

## 6. Contact
For privacy concerns, please open an issue in this repository.