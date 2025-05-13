import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

Stock = pd.read_csv('Transaction_Data.csv',  index_col=0)
df_Stock = Stock
df_Stock = df_Stock.rename(columns={'Amount':'Amount'})
print(df_Stock.head())

print(df_Stock.tail(5))

print(df_Stock.shape)

print(df_Stock.columns)

df_Stock['Amount'].plot(figsize=(10, 7))
plt.title("Ex Amount", fontsize=17)
plt.ylabel('Price', fontsize=14)
plt.xlabel('Time', fontsize=14)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

#df_Stock = df_Stock.drop(columns='Category')

print(df_Stock)


def create_train_test_set(df_Stock):
    features = df_Stock.drop(columns=[ 'Category'], axis=1)
    target = df_Stock['Amount']

    data_len = df_Stock.shape[0]
    print('Historical Stock Data length is - ', str(data_len))

    # create a chronological split for train and testing
    train_split = int(data_len * 0.88)
    print('Training Set length - ', str(train_split))

    val_split = train_split + int(data_len * 0.1)
    print('Validation Set length - ', str(int(data_len * 0.1)))

    print('Test Set length - ', str(int(data_len * 0.02)))

    # Splitting features and target into train, validation and test samples
    X_train, X_val, X_test = features[:train_split], features[train_split:val_split], features[val_split:]
    Y_train, Y_val, Y_test = target[:train_split], target[train_split:val_split], target[val_split:]

    # print shape of samples
    print(X_train.shape, X_val.shape, X_test.shape)
    print(Y_train.shape, Y_val.shape, Y_test.shape)

    return X_train, X_val, X_test, Y_train, Y_val, Y_test


X_train, X_val, X_test, Y_train, Y_val, Y_test = create_train_test_set(df_Stock)

from sklearn.neural_network import MLPRegressor
model = MLPRegressor(hidden_layer_sizes=(100, 50), activation="relu", solver="adam", max_iter=50 ,random_state=2)


#model = LinearRegression()
model.fit(X_train, Y_train )
#lr.fit(X_train, Y_train)
#print("Performance (R^2): ", lr.score(X_train, Y_train))

def get_mape(y_true, y_pred):
    """
    Compute mean absolute percentage error (MAPE)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


Y_train_pred = model.predict(X_train)
Y_val_pred = model.predict(X_val)
Y_test_pred = model.predict(X_test)

print("Training RMSE: ",round(np.sqrt(metrics.mean_squared_error(Y_train,Y_train_pred)),2))
print("Training MAE: ",round(metrics.mean_absolute_error(Y_train,Y_train_pred),2))

print("Test RMSE: ",round(np.sqrt(metrics.mean_squared_error(Y_test,Y_test_pred)),2))
print("Test MAE: ",round(metrics.mean_absolute_error(Y_test,Y_test_pred),2))

df_pred = pd.DataFrame(Y_val.values, columns=['Actual'], index=Y_val.index)
df_pred['Predicted'] = abs(Y_val_pred)
df_pred = df_pred.reset_index()
df_pred.loc[:, 'Date'] = pd.to_datetime(df_pred['Date'],format='%Y-%m-%d')
df_pred

print(df_pred)

df_pred[['Actual', 'Predicted']].plot()
plt.show()