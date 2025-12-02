import click
import os
from dotenv import load_dotenv
from ledger.sync import sync_account
from ledger.database import init_db, get_monthly_summary

load_dotenv()

@click.group()
def cli():
    """LedgerCLI: A personal finance dashboard."""
    init_db()

@cli.command()
def sync():
    """Fetch latest transactions."""
    click.echo("Initiating secure sync with Plaid...")
    if not os.getenv("PLAID_CLIENT_ID"):
        click.echo("Error: PLAID_CLIENT_ID not found in .env")
        return
    try:
        sync_account()
        click.echo("Sync complete.")
    except Exception as e:
        click.echo(f"Sync failed: {e}")

@cli.command()
@click.option('--month', default='current', help='Month to analyze')
def budget(month):
    """Show budget status."""
    summary = get_monthly_summary(month)
    click.echo(f"Total Spent: ${summary['total']:.2f}")

if __name__ == '__main__':
    cli()
