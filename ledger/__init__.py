"""
LedgerCLI Core Package
----------------------
Handles database interactions and Plaid API synchronization logic.
"""

__version__ = "0.1.0"
__author__ = "David Mark Dunn Jr."

from .database import init_db, get_monthly_summary, save_transaction
from .sync import sync_account