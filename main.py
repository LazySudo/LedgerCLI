import click
import os
from dotenv import load_dotenv
from ledger.sync import sync_account
from ledger.database import init_db, get_monthly_summary
from ledger.gemini import get_spending_advice

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """LedgerCLI: A personal finance dashboard."""
    init_db()

@cli.command()
def sync():
    """Fetch latest transactions from connected accounts."""
    click.echo("Initiating secure sync with Plaid...")
    
    if not os.getenv("PLAID_CLIENT_ID"):
        click.echo("Error: PLAID_CLIENT_ID not found in .env")
        return

    try:
        sync_account()
        click.echo("Sync complete. Local database updated.")
    except Exception as e:
        click.echo(f"Sync failed: {e}")

@cli.command()
@click.option('--month', default='current', help='Month to analyze')
def budget(month):
    """Show budget status."""
    summary = get_monthly_summary(month)
    
    # Basic Display
    click.echo("\n--- Monthly Summary ---")
    click.echo(f"Total Spent: ${summary['total']:.2f}")
    click.echo("-----------------------")

@cli.command()
def analyze():
    """Ask Gemini for financial advice based on current data."""
    click.echo("🧠 Contacting Google Gemini for analysis...")
    
    # Mock data for the 'dummy' project so it works without a DB population
    # In production, this would pull from sqlite
    mock_data = {
        "Groceries": 450.00,
        "Dining Out": 200.00,
        "Utilities": 150.00,
        "Subscriptions": 45.00
    }
    
    advice = get_spending_advice(mock_data)
    
    click.echo("\n--- AI Financial Insight ---")
    click.echo(advice)
    click.echo("----------------------------")

@cli.command()
def link():
    """(Setup) Generate a Link Token to connect a bank."""
    click.echo("--- Bank Connection Setup ---")
    click.echo("1. LedgerCLI will generate a 'Link Token' via the Plaid API.")
    click.echo("2. You will open the provided URL in your browser to authenticate with your bank.")
    click.echo("3. Copy the 'Public Token' from the browser back to this terminal.")
    click.echo("4. LedgerCLI will exchange it for a permanent 'Access Token' stored locally.")
    click.echo("\n(To implement this flow, refer to the Plaid Quickstart documentation)")

if __name__ == '__main__':
    cli()