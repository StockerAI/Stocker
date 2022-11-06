import pandas as pd
from sklearn.linear_model import LinearRegression
# from sklearn import datasets
# from sklearn.model_selection import train_test_split

nme = [523, 324, 23, 44]
deg = [1, 2, 3, 4]
scr = [90, 40, 80, 98]
dict = {'name': nme, 'degree': deg, 'score': scr}
df = pd.DataFrame(dict)

pnme = [523, 324, 23, 44]
pdeg = [1, 2, 3, 4]
pdict = {'name': pnme, 'degree': pdeg}
pdf = pd.DataFrame(dict)

def linear_regression(initial_dataframe, prediction_column_name, prediction_dataframe):
    x_train = initial_dataframe.drop(columns=[prediction_column_name])
    y_train = pd.DataFrame(initial_dataframe[prediction_column_name])
    lr = LinearRegression()
    lr.fit(X=x_train, y=y_train)
    prediction = lr.predict(prediction_dataframe)
    return prediction

print(linear_regression(initial_dataframe=df, prediction_column_name='score', prediction_dataframe=pdf))
