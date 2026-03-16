import pandas as pd

def load_data():
    df = pd.read_csv("data/air_quality.csv")
    return df

def clean_data(df):
    df = df.dropna()
    return df