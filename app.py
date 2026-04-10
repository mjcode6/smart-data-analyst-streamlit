# -------------------------
# 1️⃣ Import libraries
# -------------------------
import streamlit as st
import pandas as pd
import io               # used to capture df.info()
import utils            # placeholder for future (Day 2)

# -------------------------
# 2️⃣ App title
# -------------------------
st.title("AI Data Analyst")

# -------------------------
# 3️⃣ File uploader
# -------------------------
file = st.file_uploader("Upload your CSV file")

# -------------------------
# 4️⃣ If file is uploaded
# -------------------------
if file is not None:

    # Read CSV
    df = pd.read_csv(file)

    # -------------------------
    # Preview data
    # -------------------------
    st.subheader("Preview of your data")
    st.write(df.head())

    # -------------------------
    # Data info (FIXED ✅)
    # -------------------------
    st.subheader("Basic info about the data")
    st.text("Columns, non-null counts, and data types")

    buffer = io.StringIO()       # create memory buffer
    df.info(buf=buffer)          # send info to buffer
    info_str = buffer.getvalue() # get text from buffer

    st.text(info_str)            # display in app

    # -------------------------
    # Descriptive stats
    # -------------------------
    st.subheader("Descriptive statistics for numeric columns")
    st.write(df.describe())

    # -------------------------
    # Placeholder for Day 2
    # -------------------------
    # df = utils.clean_data(df)

    st.subheader("missing values in each column")
    st.write(df.isnull().sum())

    st.subheader("Before Cleaning")
    st.write(df)

    df_clean = utils.clean_data(df)

    st.subheader("After Cleaning")
    st.write(df_clean)