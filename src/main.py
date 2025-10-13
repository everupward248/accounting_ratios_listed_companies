from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
from src.helper_modules import cli_functions as cl
from tabulate import tabulate
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

    # .tolist() used, as if the dataframe is passed directly to tabulate() the type checker will raise a warning though the function still executes without issue
    if args.balance_sheet:
        cl.get_balance_sheet(args.balance_sheet)
    elif args.income_statement:
        cl.get_income_statement(args.income_statement)
    elif args.cash_flows:
        cl.get_cash_flows(args.cash_flows)
            
    # ratios
    if args.ratios:
        ticker = input("Please provide a valid company ticker: ").strip()

       
        if "liquidity" in args.ratios:
            # obtain the balance sheet data for the selected company and then extract the FSLI's which will be used in the liquidity ratio computations
            limit = dr.get_period()
            if (bs := dr.get_bs(ticker, limit)) is not None:
                # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
                ratio_data = bs.copy(deep=True)
                
                # apply the liquidity ratios to the balance sheet data
                ratio_data["current_ratio"] = ratio_data.apply(
                    lambda x: round(ar.current_ratio(x["totalCurrentAssets"], x["totalCurrentLiabilities"]), 3), axis=1
                    )
                ratio_data["quick_ratio"] = ratio_data.apply(
                    lambda x: round(ar.quick_ratio(x["totalCurrentAssets"], x["inventory"], x["totalCurrentLiabilities"]), 3), axis=1
                    )
                ratio_data["cash_ratio"] = ratio_data.apply(
                    lambda x: round(ar.cash_ratio(x["cashAndCashEquivalents"], x["totalCurrentLiabilities"]), 3), axis=1
                    )
                
                # create a list of the ratio columns and to pass as headers to tabulate
                cols = ["fiscalYear", "date", "current_ratio", "quick_ratio", "cash_ratio"]
                liquidity_ratios = ratio_data[cols]
                liquidity_ratios_list = liquidity_ratios.values.tolist()

                print(tabulate(liquidity_ratios_list, headers=cols, tablefmt="grid"))

                logger.info(f"The liquidity ratios have been provided for {ratio_data["symbol"][0]}")
                shared_logger.info(f"The liquidity ratios have been provided for {ratio_data["symbol"][0]}")
            else:
                logger.warning(f"The liquidity ratios failed, ensure valid ticker")
                shared_logger.warning(f"The liquidity ratios failed, ensure valid ticker")
                sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")
        elif "profitability" in args.ratios:
            limit = dr.get_period()
            # obtain the data across all financial statements to compute the ratios
            if (inc_s := dr.get_is(ticker, limit)) is not None and (bs := dr.get_bs(ticker, limit)) is not None and (cf := dr.get_cf(ticker, limit)) is not None:
                # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
                is_data = inc_s.copy(deep=True)
                bs_data = bs.copy(deep=True)
                cf_data = cf.copy(deep=True)
                # merge the financial statements on fiscal year
                # starting with the is and bs, then the cf
                merged_df = pd.merge(is_data, bs_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))
                merged_df = pd.merge(merged_df, cf_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))

                # apply the profitability ratios to the income statement data
                merged_df["gross_profit_margin"] = merged_df.apply(lambda x: round(ar.gross_profit_margin(x["grossProfit"], x["revenue"]), 3), axis=1)
                merged_df["operating_profit_margin"] = merged_df.apply(lambda x: round(ar.operating_profit_margin(x["operatingIncome"], x["revenue"]), 3), axis=1)
                merged_df["net_profit_margin"] = merged_df.apply(lambda x: round(ar.operating_profit_margin(x["netIncome"], x["revenue"]), 3), axis=1)
                
                # user provides an option for the calculation of capital employed to be passed to the roce computation
                while True:
                    try:
                        capital_employed_type = int(input("select 1 for total assets less current liabilities or select 2 for equity plus non-current liabilities as measure of capital employed? ").strip())

                        if capital_employed_type == 1:
                            merged_df["capital_employed"] = merged_df.apply(lambda x: round(ar.capital_employed(x["totalAssets"], x["totalCurrentLiabilities"], 1), 3), axis=1)
                            break
                        elif capital_employed_type == 2:
                            merged_df["capital_employed"] = merged_df.apply(lambda x: round(ar.capital_employed(x["totalStockholdersEquity"], x["longTermDebt"] + x["capitalLeaseObligations"], 2), 3), axis=1)
                            break
                        else:
                            print("must select a number 1 or 2")
                            continue
                    except EOFError:
                        sys.exit("program quit...")
                    except Exception as e:
                        print(e)
                        continue

                merged_df["return_on_capital_employed"] = merged_df.apply(lambda x: round(ar.roce(x["operatingIncome"], x["capital_employed"]), 3), axis=1)
                merged_df["operating_cash_flow_margin"] = merged_df.apply(lambda x: round(ar.operating_cash_flow_margin(x["operatingCashFlow"], x["revenue"]), 3), axis=1)
                merged_df["free_cash_flow_margin"] = merged_df.apply(lambda x: round(ar.free_cash_flow_margin(x["freeCashFlow"], x["revenue"]), 3), axis=1)
                merged_df["return_on_equity"] = merged_df.apply(lambda x: round(ar.return_on_equity(x["netIncome"], x["totalStockholdersEquity"]), 3), axis=1)
                merged_df["return_on_assets"] = merged_df.apply(lambda x: round(ar.return_on_assets(x["netIncome"], x["totalAssets"]), 3), axis=1)
                
                
                # create a list of the ratio columns and to pass as headers to tabulate
                cols = ["fiscalYear", "date", "gross_profit_margin", "operating_profit_margin", "net_profit_margin", "return_on_capital_employed", "operating_cash_flow_margin", "free_cash_flow_margin", "return_on_equity", "return_on_assets"]
                profitability_ratios = merged_df[cols]
                profitability_ratios_list = profitability_ratios.values.tolist()

                print(tabulate(profitability_ratios_list, headers=cols, tablefmt="grid"))
                logger.info(f"The profitability ratios have been provided for {merged_df["symbol"][0]}")
                shared_logger.info(f"The profitability ratios have been provided for {merged_df["symbol"][0]}")
            else:
                logger.warning(f"The profitability ratios failed, ensure valid ticker")
                shared_logger.warning(f"The profitability ratios failed, ensure valid ticker")
                sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")
        elif "gearing"  in args.ratios:
            limit = dr.get_period()
            # obtain the data across all financial statements to compute the ratios
            if (inc_s := dr.get_is(ticker, limit)) is not None and (bs := dr.get_bs(ticker, limit)) is not None:
                # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
                is_data = inc_s.copy(deep=True)
                bs_data = bs.copy(deep=True)
                merged_df = pd.merge(is_data, bs_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))

                merged_df["debt_to_equity"] = merged_df.apply(lambda x: round(ar.debt_equity_ratio(x["totalLiabilities"], x["totalStockholdersEquity"]), 3), axis=1)
                merged_df["interest_cover"] = merged_df.apply(lambda x: round(ar.interest_cover(x["ebit"], x["interestExpense"]), 3), axis=1)
                merged_df["equity_ratio"] = merged_df.apply(lambda x: round(ar.equity_ratio(x["totalEquity"], x["totalAssets"]), 3), axis=1)
                merged_df["debt_ratio"] = merged_df.apply(lambda x: round(ar.debt_ratio(x["totalDebt"], x["totalAssets"]), 3), axis=1)


                # create a list of the ratio columns and to pass as headers to tabulate
                cols = ["fiscalYear", "date", "debt_to_equity", "interest_cover", "equity_ratio", "debt_ratio"]
                gearing_ratios = merged_df[cols]
                gearing_ratios_list = gearing_ratios.values.tolist()

                print(tabulate(gearing_ratios_list, headers=cols, tablefmt="grid"))
                logger.info(f"The gearing ratios have been provided for {merged_df["symbol"][0]}")
                shared_logger.info(f"The gearing ratios have been provided for {merged_df["symbol"][0]}")
            else:
                logger.warning(f"The profitability ratios failed, ensure valid ticker")
                shared_logger.warning(f"The profitability ratios failed, ensure valid ticker")
                sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")
        elif "valuation" in args.ratios:
            # obtain the data across all financial statements to compute the ratios
            limit = dr.get_period()
            if (inc_s := dr.get_is(ticker, limit)) is not None:
                is_data = inc_s.copy(deep=True)
                
                # convert the dates for the search into a list and slice the earliest and lates periods to pass as query parameters into the stock price search
                dates = list(is_data["date"])
                from_date = dates[-1]
                to_date = dates[0]

                # obtain the rows of the stock prices for only the financial statement year end dates
                if (stock_prices := dr.stock_prices(ticker, from_date, to_date)) is not None:
                    # initialize a dataframe to extract only the ye dates, 
                    df = pd.DataFrame(columns=stock_prices.columns)

                    # append only the year date prices
                    for i in range(len(stock_prices)):
                        if stock_prices.loc[i]["date"] in dates:
                            df.loc[i] = stock_prices.loc[i]
                
                    stock_price_data = df.copy(deep=True)
                    # merge the data sets
                    merged_df = pd.merge(is_data, stock_price_data, on="date", how="inner", suffixes=("", "_df2"))

                    merged_df["p/e_ratio"] = merged_df.apply(lambda x: round(ar.pe_ratio(x["close"], x["eps"]), 3), axis=1)
                    merged_df["p/e_ratio_diluted"] = merged_df.apply(lambda x: round(ar.pe_ratio(x["close"], x["epsDiluted"]), 3), axis=1)

                    # create a list of the ratio columns and to pass as headers to tabulate
                    cols = ["fiscalYear", "date", "eps", "epsDiluted", "p/e_ratio", "p/e_ratio_diluted", "close"]
                    valuation_ratios = merged_df[cols]
                    valuation_ratios_list = valuation_ratios.values.tolist()

                    print(tabulate(valuation_ratios_list, headers=cols, tablefmt="grid"))
                    logger.info(f"The valuation ratios have been provided for {merged_df["symbol"][0]}")
                    shared_logger.info(f"The valuation ratios have been provided for {merged_df["symbol"][0]}")
                else:
                    logger.warning(f"The valuation ratios failed, ensure valid ticker")
                    shared_logger.warning(f"The valuation ratios failed, ensure valid ticker")
                    sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")
                            
            else:
                logger.warning(f"The valuation ratios failed, ensure valid ticker")
                shared_logger.warning(f"The valuation ratios failed, ensure valid ticker")
                sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")

               


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program is a CLI tool which allows users to fetch the accounting ratios of listed companies when provided the ticker.")
    parser.add_argument("-bs", "--balance_sheet", type=str, help="Use this flag to obtain the balance sheet data for a given listed company. Provide the company ticker.")
    parser.add_argument("-is", "--income_statement", type=str, help="Use this flag to obtain the income statement data for a given listed company. Provide the company ticker.")
    parser.add_argument("-cf", "--cash_flows", type=str, help="Use this flag to obtain the cash flows data for a given listed company. Provide the company ticker.")
    parser.add_argument("-r", "--ratios", type=str, choices=["liquidity", "profitability", "gearing", "valuation", "all"], help="Use this flag to obtain the financial ratios of a selected listed company. Provide a choice which which category of ratios or all.")
    parser.add_argument("-nt", "--name_ticker", action="store_true", help="Omit this flag for tickers and include for the legally registered company name.")
    parser.add_argument("-gnt", "--get_name_ticker", type=str, choices=["name", "ticker"], help="Use this flag to obtain the legally registered company name or ticker per the ticker and company name respectively.")
    return parser

if __name__ == "__main__":
    main()