from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
from src.helper_modules import cli_functions as cl
import argparse
import pandas as pd
import sys


def main() -> None:

    logger = get_logger(__name__)
    parser = cli()
    args = parser.parse_args()

    if args.get_name_ticker == "name":
        print(dr.get_ticker())
    elif args.get_name_ticker == "ticker":
        print(dr.get_name())

    if args.balance_sheet:
        cl.get_balance_sheet(args.balance_sheet)
    elif args.income_statement:
        cl.get_income_statement(args.income_statement)
    elif args.cash_flows:
        cl.get_cash_flows(args.cash_flows)
            
    # ratios
    if args.ratios:
        ticker = input("Please provide a valid company ticker: ").strip()
        try:
            if "liquidity" in args.ratios:
                # obtain the balance sheet data for the selected company and then extract the FSLI's which will be used in the liquidity ratio computations
                limit = dr.get_period()
                cl.liquidity(ticker, limit)
            elif "profitability" in args.ratios:
                limit = dr.get_period()
                cl.profitability(ticker, limit)
            elif "gearing"  in args.ratios:
                limit = dr.get_period()
                cl.gearing(ticker, limit)
            elif "valuation" in args.ratios:
                # obtain the data across all financial statements to compute the ratios
                limit = dr.get_period()
                cl.valuation(ticker, limit)
            elif "all" in args.ratios:
                limit = dr.get_period()
                cl.all_ratios(ticker, limit)
            logger.info(f"user has successfully used the {args.ratios} function")
            shared_logger.info(f"user has successfully used the {args.ratios} function")
        except Exception as e:
            logger.warning(f"user has unsuccessfully used the {args.ratios} function")
            shared_logger.warning(f"user has unsuccessfully used the {args.ratios} function")

    if len(sys.argv) <= 1:
        logger.info(f"User did not provide any options")
        shared_logger.info(f"User did not provide any options")
        sys.exit("Please provide an argument to the CLI. Use '-h' or '--help' to view options")
    


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program is a CLI tool which allows users to fetch the financial statements and accounting ratios of listed companies when provided the ticker.")
    parser.add_argument("-bs", "--balance_sheet", type=str, help="Use this flag to obtain the balance sheet data for a given listed company. Provide the company ticker.")
    parser.add_argument("-is", "--income_statement", type=str, help="Use this flag to obtain the income statement data for a given listed company. Provide the company ticker.")
    parser.add_argument("-cf", "--cash_flows", type=str, help="Use this flag to obtain the cash flows data for a given listed company. Provide the company ticker.")
    parser.add_argument("-r", "--ratios", type=str, choices=["liquidity", "profitability", "gearing", "valuation", "all"], help="Use this flag to obtain the financial ratios of a selected listed company. Provide a choice which which category of ratios or all.")
    parser.add_argument("-gnt", "--get_name_ticker", type=str, choices=["name", "ticker"], help="Use this flag to obtain the legally registered company name or ticker per the ticker and company name respectively.")
    return parser

if __name__ == "__main__":
    main()