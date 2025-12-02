"""
LedgerCLI Core Package
----------------------
Handles database interactions and Plaid API synchronization logic.
"""

__version__ = "0.1.0"
__author__ = "David Mark Dunn Jr."

# Expose key functions to the package level (Optional but clean)
# This allows you to do: 'from ledger import sync_account' 
# instead of: 'from ledger.sync import sync_account'
from .database import init_db, get_monthly_summary, save_transaction
from .sync import sync_account