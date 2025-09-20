from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
from tabulate import tabulate
import argparse
import pandas as pd


def main() -> None:

    logger = get_logger(__name__)
    parser = cli()
    args = parser.parse_args()

    if args.get_name_ticker == "name":
        print(dr.get_ticker())
    elif args.get_name_ticker == "ticker":
        print(dr.get_name())

    # .tolist() used as if the dataframe is passed directly to tabulate() the type checker will raise a warning though the function still executes without issue
    if args.balance_sheet:
        if (df := dr.get_bs(args.balance_sheet)) is not None and not df.empty:
            print(tabulate(df.reset_index().values.tolist(), tablefmt="grid"))
            logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
            shared_logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
        else:
            print("There was an issue rendering your request. Please try again.")
            logger.warning(f"Function returned: {df}")
            shared_logger.warning(f"Function returned: {df}")
    elif args.income_statement:
        if (df := dr.get_is(args.income_statement)) is not None and not df.empty: 
            print(tabulate(df.reset_index().values.tolist(), tablefmt="grid"))
            logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
            shared_logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
        else:
            print("There was an issue rendering your request. Please try again.")
            logger.warning(f"Function returned: {df}")
            shared_logger.warning(f"Function returned: {df}")
    elif args.cash_flows:
        if (df := dr.get_cf(args.cash_flows)) is not None and not df.empty: 
            print(tabulate(df.reset_index().values.tolist(), tablefmt="grid"))
            logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
            shared_logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df[0]["symbol"]}")
        else:
            print("There was an issue rendering your request. Please try again.")
            logger.warning(f"Function returned: {df}")
            shared_logger.warning(f"Function returned: {df}")
            
    # ratios
    if args.ratios:
        ticker = input("Please provide a valid company ticker: ").strip()

        for ratio in args.ratios:
            if "liquidity" in args.ratios:
                if (bs := dr.get_bs(ticker)) is not None:
                    print(bs.loc["totalCurrentAssets"])
               


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program is a CLI tool which allows users to fetch the accounting ratios of listed companies when provided the ticker.")
    parser.add_argument("-bs", "--balance_sheet", type=str, help="Use this flag to obtain the balance sheet data for a given listed company. Provide the company ticker.")
    parser.add_argument("-is", "--income_statement", type=str, help="Use this flag to obtain the income statement data for a given listed company. Provide the company ticker.")
    parser.add_argument("-cf", "--cash_flows", type=str, help="Use this flag to obtain the cash flows data for a given listed company. Provide the company ticker.")
    parser.add_argument("-r", "--ratios", type=str, nargs="+", choices=["liquidity", "profitability", "gearing", "valuation", "all"], help="Use this flag to obtain the financial ratios of a selected listed company. Provide a choice which which category of ratios or all.")
    parser.add_argument("-nt", "--name_ticker", action="store_true", help="Omit this flag for tickers and include for the legally registered company name.")
    parser.add_argument("-gnt", "--get_name_ticker", type=str, choices=["name", "ticker"], help="Use this flag to obtain the legally registered company name or ticker per the ticker and company name respectively.")
    return parser

if __name__ == "__main__":
    main()