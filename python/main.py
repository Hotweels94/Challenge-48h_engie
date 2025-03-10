import pandas as pd
from data_loader import load_data
from text_cleaner import clean_dataframe
from feature_generator import generate_features

def main():
    file_path = "./filtered_tweets_engie.csv"

    df = load_data(file_path)

    df = clean_dataframe(df)

    df = generate_features(df)

    print(df.head())

    df.to_csv("./result_csv/cleaned_data.csv", sep=';', index=False)

if __name__ == "__main__":
    main()