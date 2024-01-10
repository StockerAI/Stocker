from yahoo_fin import stock_info as si

ticker = "AAPL"
hist = si.get_data(ticker)
print(hist)

balance_sheet = si.get_balance_sheet(ticker)
# income_statement = si.get_income_statement(ticker)
# cash_flow = si.get_cash_flow(ticker)

print(balance_sheet)
# print(income_statement)
# print(cash_flow)

# options_chain = si.get_options_chain(ticker)
# print(options_chain)

earnings = si.get_earnings_history(ticker)
print(earnings)
