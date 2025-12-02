import os
import plaid
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
import datetime
from ledger.database import save_transaction
# Import the AI module safely
try:
    from ledger.gemini import categorize_transaction
except ImportError:
    categorize_transaction = None

# Ensure env vars are loaded even if this file is run standalone
load_dotenv()

def get_plaid_client():
    """
    Initialize the Plaid API Client with correct environment config.
    """
    client_id = os.getenv('PLAID_CLIENT_ID')
    secret = os.getenv('PLAID_SECRET')
    
    if not client_id or not secret:
        raise ValueError("Missing Plaid Credentials in .env")

    # Use Development by default for this project
    configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': client_id,
            'secret': secret,
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def sync_account():
    """
    Connect to Plaid and download transactions.
    """
    access_token = os.getenv('PLAID_ACCESS_TOKEN')
    
    if not access_token:
        print("⚠️  No Access Token found.")
        print("   Please run 'python main.py link' to connect a bank account first.")
        return

    try:
        client = get_plaid_client()
        
        # Fetch last 30 days of data
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
        end_date = datetime.datetime.now().date()

        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options=TransactionsGetRequestOptions(
                count=100,
                offset=0
            )
        )

        print("🔄 Fetching transactions from Plaid...")
        response = client.transactions_get(request)
        transactions = response['transactions']
        
        print(f"✅ Retrieved {len(transactions)} transactions.")
        
        # Check if AI is enabled
        use_ai = os.getenv("GEMINI_API_KEY") and categorize_transaction
        if use_ai:
            print("🧠 AI Auto-Categorization Enabled.")

        for txn in transactions:
            category = txn['category']
            
            # If AI is enabled, try to refine the category
            if use_ai:
                ai_cat = categorize_transaction(txn['name'], txn['amount'])
                if ai_cat and ai_cat != "Uncategorized":
                    category = [ai_cat] # Override Plaid category with AI's specific tag

            txn_data = {
                'transaction_id': txn['transaction_id'],
                'account_id': txn['account_id'],
                'amount': txn['amount'],
                'date': str(txn['date']),
                'name': txn['name'],
                'category': category
            }
            save_transaction(txn_data)
            
    except plaid.ApiException as e:
        print(f"❌ Plaid API Error: {e}")
    except Exception as e:
        print(f"❌ Sync Error: {e}")