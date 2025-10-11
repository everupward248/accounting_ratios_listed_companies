import logging
from src.helper_modules.logger_setup import get_logger, shared_logger

logger = get_logger(__name__)

# liquidity 
def current_ratio(current_assets: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities with its total current assets

    """
    return current_assets / current_liabilities

def quick_ratio(current_assets: float, inventory: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities with its total current assets but also accounts for the company's level of inventory as this is less liquid

    """
    return (current_assets - inventory) / current_liabilities

def cash_ratio(cash: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities using only its cash and cash equivalents

    """
    return cash / current_liabilities

# profitability
def gross_profit_margin(gross_profit: float, revenue: float) -> float:
    """
    this is a measure of how well a business converts its sales into profits before paying overheads, taxes, and financing costs

    """
    return gross_profit / revenue

def operating_profit_margin(operating_profit: float, revenue: float) -> float:
    """
    this is a measure of how well the business profits from its core business operations after deducting direct costs and operational expenses before taxes and finance costs
    
    """
    return operating_profit / revenue 

def net_profit_margin(net_profit: float, revenue: float) -> float:
    """
    this is the 'bottom line' after deducting all expenses
    how much each dollar of revenue is retained as profit for shareholders

    """
    return net_profit / revenue

def roce(ebit: float, capital_employed: float) -> float:
    """
    return on capital employed - a measure of how efficiently a company generates profit from the long-term capital invested

    """
    return ebit / capital_employed

def capital_employed(equity: float, non_current_liabilities: float, type: int) -> float:
    """
    capital employed - equity + non-current assets - the total long-term funding used by the business
    can also be total assets less current liabilities but the actual capital structure is prefered from an investor perspective
    
    """
    if type == 1:
        return equity - non_current_liabilities
    else:   
        return equity + non_current_liabilities

def operating_cash_flow_margin(operating_cash_flow: float, revenue: float) -> float:
    """
    cash flow margin is a measure of how efficiently a business converts its sales into actual cash
    
    """
    return operating_cash_flow / revenue

def free_cash_flow_margin(free_cash_flow: float, revenue: float) -> float:
    """
    cash flow margin is a measure of how efficiently a business converts its sales into actual cash
    
    """
    return free_cash_flow / revenue

def return_on_equity(net_income: float, shareholders_equity: float) -> float:
    """
    ROE is a measure of how well the company is converting equity financing to profits
    
    """
    return net_income / shareholders_equity

def return_on_assets(net_income: float, assets: float) -> float:
    """
    ROA is a measure of how well the company uses its assets to generate profits

    """
    return net_income / assets

# gearing
def debt_equity_ratio(total_liabilities: float, total_shareholder_equity: float) -> float:
    """
    measures how leveraged a company is, how much of its operations is financed by debt

    """
    return total_liabilities / total_shareholder_equity

def interest_cover():
    ...

def equity_ratio():
    ...

def debt_ratio():
    ...

# valuation
def eps():
    ...
    
def p_e():
    ...