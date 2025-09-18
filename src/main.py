from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
import argparse


def main() -> None:

    logger = get_logger(__name__)
    parser = cli()
    args = parser.parse_args()

    if args.get_name_ticker == "name":
        print(dr.get_ticker())
    elif args.get_name_ticker == "ticker":
        print(dr.get_name())

    if args.balance_sheet:
        print(dr.get_bs(args.balance_sheet))
    elif args.income_statement:
        print(dr.get_is(args.income_statement))
    elif args.cash_flows:
        print(dr.get_cf(args.cash_flows))
    

def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program is a CLI tool which allows users to fetch the accounting ratios of listed companies when provided the ticker.")
    parser.add_argument("-bs", "--balance_sheet", type=str, help="Use this flag to obtain the balance sheet data for a given listed company. Provide the company ticker.")
    parser.add_argument("-is", "--income_statement", type=str, help="Use this flag to obtain the income statement data for a given listed company. Provide the company ticker.")
    parser.add_argument("-cf", "--cash_flows", type=str, help="Use this flag to obtain the cash flows data for a given listed company. Provide the company ticker.")
    parser.add_argument("-nt", "--name_ticker", action="store_true", help="Omit this flag for tickers and include for the legally registered company name.")
    parser.add_argument("-gnt", "--get_name_ticker", type=str, choices=["name", "ticker"], help="Use this flag to obtain the legally registered company name or ticker per the ticker and company name respectively.")
    return parser

if __name__ == "__main__":
    main()