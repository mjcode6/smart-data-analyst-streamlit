# utils.py
# -------------------------
# This file will contain all your helper functions
# For Day 1, it is empty, but we create it now
# so app.py can import it and the project is ready for Day 2

# Example of future function (commented for now):
# def clean_data(df):
#     # drop duplicates, fill missing values
#     return df

def clean_data(df):
    #remove duplicated
    df = df.drop_duplicates()

    #  fill missing values with mean for numeric columns
    df = df.fillna(df.mean(numeric_only=True))
    return df

    