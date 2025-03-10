import os
import pandas as pd
from data_loader import load_data
from text_cleaner import clean_dataframe
from feature_generator import generate_features
from calculateKPI import calculateKPI
from analyze_tweets import analyze

def main():
    file_path = "./filtered_tweets_engie.csv"
    result_path = "./result_csv/cleaned_data.csv"

    df = load_data(file_path)
    df = clean_dataframe(df)
    df = generate_features(df)

    df = calculateKPI()
    df = analyze()

    df.to_csv(result_path, sep=';', index=False)

if __name__ == "__main__":
    main()
