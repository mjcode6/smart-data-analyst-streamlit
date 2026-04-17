# -------------------------
# 1️⃣ Import libraries
# -------------------------
import streamlit as st
import pandas as pd
import io               # used to capture df.info()
import utils            # placeholder for future (Day 2)
import matplotlib.pyplot as plt
import seaborn as sns
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

# Day 3: Data Visualization with Pandas + Streamlit
    st.subheader("Numeric Column Distribution")
    column = st.selectbox("Choose column", df.select_dtypes(include='number').columns)

    st.bar_chart(df[column].value_counts())


    # Step 2: Add basic insights
    st.subheader("QuickInsights")
    st.write("shape of the data: ", df.shape)
    st.write("missing values:")
    st.write(df.isnull().sum())

# Step 3: Add correlation (important DS skill)
  
    st.subheader("Correlation Heatmap")

    corr = df.corr(numeric_only=True)

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

    st.pyplot(fig)

# Step 4: Automatic insights (bonus for Day 4)
    st.subheader("📊 Automatic Data Analysis")

    for col in df.columns:

     st.write(f"### {col}")

    # CATEGORICAL
    if df[col].dtype == "object":
        st.bar_chart(df[col].value_counts().head(10))

    # NUMERIC
    if pd.api.types.is_numeric_dtype(df[col]):

        fig, ax = plt.subplots()
    ax.hist(df[col].dropna(), bins=20)
    st.pyplot(fig)

    # Skewness
    skew = df[col].skew()

    if skew > 1:
        st.write(f"📈 {col} is right-skewed")
    elif skew < -1:
        st.write(f"📉 {col} is left-skewed")
    else:
        st.write(f"✅ {col} is fairly balanced")

    # 🔥 OUTLIERS
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

    if len(outliers) > 0:
        st.write(f"⚠️ {col} has {len(outliers)} possible outliers")
    else:
        st.write(f"✅ {col} has no significant outliers")
    # STEP 3 — Smart Correlation Insight 🔥
    st.subheader("🧠 Correlation Insights (Clean)")

    st.write("Looking for strong relationships between variables...")

    corr = df_clean.corr(numeric_only=True)

    found = False

    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            value = corr.iloc[i, j]

            if abs(value) > 0.7:
                found = True

                col1 = corr.columns[i]
                col2 = corr.columns[j]

                if value > 0.7:
                    st.write(f"📈 {col1} and {col2} have strong positive correlation ({value:.2f})")
                elif value < -0.7:
                    st.write(f"📉 {col1} and {col2} have strong negative correlation ({value:.2f})")

    if not found:
        st.write("No strong correlations found")