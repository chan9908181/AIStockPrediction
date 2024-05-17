import os

import pandas
from dotenv import load_dotenv

load_dotenv()

df = pandas.read_csv(os.getenv("TEST_CSV_FILE_PATH"))


def calculate_rsi(window: int):
    df_close = df['close']
    close_diff = df_close.diff()

    df_gain = close_diff.apply(lambda x: x if x > 0 else 0)  # we separate positive and negative difference
    df_loss = -close_diff.apply(lambda x: x if x < 0 else 0)
    # because we want our negative number be positive when calculating the formular

    df_average_gain = df_gain.rolling(window=window, min_periods=1).mean()
    df_average_loss = df_loss.rolling(window=window, min_periods=1).mean()

    rs = df_average_gain / df_average_loss

    df['rsi'] = 100 - (100 / (1 + rs))

    return df[['rsi', 'rsi_7', 'rsi_14']]


def calculate_rsi_7():
    return calculate_rsi(7)


def calculate_rsi_14():
    return calculate_rsi(14)


def calculate_cci(window: int):
    df['TP'] = (df['close'] + df['high'] + df['low']) / 3

    df['SMA'] = df['TP'].rolling(window=window).mean()

    df['Mean Deviation'] = df['TP'].rolling(window=window).apply(lambda x: (x - x.mean()).abs().mean())

    df['cci'] = (df['TP'] - df['SMA']) / (0.015 * df['Mean Deviation'])

    return df[['cci', 'cci_7', 'cci_14']]


def calculate_cci_7():
    return calculate_cci(7)


def calculate_cci_14():
    return calculate_cci(14)


print(calculate_cci_7())
