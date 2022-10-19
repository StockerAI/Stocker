from yahoo_fin import stock_info
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics

apple_daily = stock_info.get_data("aapl", start_date="12/04/2009", end_date="12/30/2009", index_as_date = True, interval="1d")

# print(apple_daily)

def add_daily_result(row):
    '''
    Function that returns 'GOOD' or 'BAD' depending
    on the result of the 'close' and 'open' values.
    '''
    if row['close'] > row['open']:
        return 1
    else:
        return 0

apple_daily['result'] = apple_daily.apply(lambda row: add_daily_result(row), axis=1)

apple_daily = apple_daily.fillna(0)

# print(apple_daily)

# apple_daily_for_test = stock_info.get_data("aapl", start_date="12/04/2022", end_date="12/10/2022", index_as_date = True, interval="1d")

X_train, X_test, y_train, y_test = train_test_split(apple_daily[['open', 'high', 'low', 'close', 'adjclose', 'volume']].to_numpy(), apple_daily[['result']].to_numpy(), test_size=0.33, shuffle=False)

# print(X_train)

clf = svm.SVC(kernel='linear').fit(X_train, y_train.ravel())
y_pred = clf.predict(X_test)
print('Accuracy:', metrics.accuracy_score(y_test, y_pred))

print('\n\nClosed...')
