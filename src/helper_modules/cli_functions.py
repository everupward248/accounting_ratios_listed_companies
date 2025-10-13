from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
from tabulate import tabulate
import pandas as pd
import sys

logger = get_logger(__name__)

def main():
    get_cash_flows("NVDA")

def get_balance_sheet(ticker: str) -> None:
    """
    retrieves the balance sheet data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_bs(ticker, limit)) is not None and not df.empty:
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

def get_income_statement(ticker: str) -> None:
    """
    retrieves the income statement data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_is(ticker, limit)) is not None and not df.empty: 
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

def get_cash_flows(ticker: str) -> None:
    """
    retrieves the cash flows data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_cf(ticker, limit)) is not None and not df.empty: 
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

if __name__ == "__main__":
    main()