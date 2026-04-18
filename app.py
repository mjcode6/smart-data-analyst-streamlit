# -------------------------
# 1️⃣ Import libraries
# -------------------------
import streamlit as st
import pandas as pd
import io
import utils
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# 2️⃣ App Title
# -------------------------
st.title("📊 AI Data Analyst")
st.markdown("Upload your dataset and get simple, human-friendly insights.")

# -------------------------
# 3️⃣ File uploader
# -------------------------
file = st.file_uploader("📁 Upload your CSV file")

# -------------------------
# 4️⃣ If file uploaded
# -------------------------
if file is not None:

    df = pd.read_csv(file)

    # -------------------------
    # 📌 DATA OVERVIEW
    # -------------------------
    st.divider()
    st.subheader("📌 Data Overview")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])

    st.write("Preview of your data:")
    st.dataframe(df.head())

    # -------------------------
    # 🧹 CLEANING
    # -------------------------
    df_clean = utils.clean_data(df)

    # -------------------------
    # 📊 VISUALS
    # -------------------------
    st.divider()
    st.subheader("📊 Visual Insights")

    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:
        column = st.selectbox("Choose a numeric column", numeric_cols)
        st.bar_chart(df[column].value_counts())
    else:
        st.info("No numeric columns available for visualization.")

    # -------------------------
    # 🧠 INSIGHTS
    # -------------------------
    st.divider()
    st.subheader("🧠 Key Insights")

    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        st.warning("Some columns contain missing values.")
        st.write(missing[missing > 0])
    else:
        st.success("No missing values detected.")

    # Skewness + Outliers
    for col in numeric_cols:

        st.write(f"### {col}")

        # Histogram
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=20)
        st.pyplot(fig)

        # Skewness
        skew = df[col].skew()

        if skew > 1:
            st.warning("This column is highly unbalanced (skewed to one side).")
        elif skew < -1:
            st.warning("This column is highly unbalanced in the opposite direction.")
        else:
            st.success("This column is fairly balanced.")

        # Outliers
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

        if len(outliers) > 0:
            st.warning(f"{len(outliers)} potential outliers detected.")
        else:
            st.success("No significant outliers detected.")

    # -------------------------
    # 🔗 RELATIONSHIPS
    # -------------------------
    st.divider()
    st.subheader("🔗 Relationships Between Variables")

    corr = df_clean.corr(numeric_only=True)

    if not corr.empty:

        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

        st.subheader("🧠 Correlation Insights")

        found = False

        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                value = corr.iloc[i, j]

                if abs(value) > 0.7:
                    found = True

                    col1 = corr.columns[i]
                    col2 = corr.columns[j]

                    if value > 0:
                        st.info(f"{col1} and {col2} move together strongly.")
                    else:
                        st.info(f"{col1} and {col2} move in opposite directions strongly.")

        if not found:
            st.success("No strong relationships detected.")

    else:
        st.info("Not enough numeric data for correlation analysis.")