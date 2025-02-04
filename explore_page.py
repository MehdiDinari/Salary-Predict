import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Function to Shorten Country Categories
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


# Function to Clean Experience Data
def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


# Function to Clean Education Data
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


# Cache the Data Loading Function
@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    # Apply Country Filtering
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[(df["ConvertedComp"] >= 10000) & (df["ConvertedComp"] <= 250000)]
    df = df[df["Country"] != "Other"]

    # Clean Experience and Education Columns
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)

    df = df.rename({"ConvertedComp": "Salary"}, axis=1)

    return df


df = load_data()


# Function to Show Exploration Page
def show_explore_page():
    st.title("📊 Explore Software Engineer Salaries 💰")

    st.markdown(
        """
        ## 🔍 Insights from the Stack Overflow Developer Survey 2020
        Explore salary trends based on different factors such as **country, experience, and education.**
        """
    )

    # ====== Country Data Count - Pie Chart ======
    st.subheader("🌍 Number of Responses Per Country")

    country_data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax1.pie(
        country_data, labels=country_data.index, autopct="%1.1f%%",
        startangle=140, textprops={'fontsize': 10}, wedgeprops={'edgecolor': 'white'}
    )
    plt.setp(autotexts, size=10, weight="bold")
    ax1.set_title("Distribution of Survey Responses by Country", fontsize=14)

    st.pyplot(fig1)

    # ====== Mean Salary by Country - Bar Chart ======
    st.subheader("💵 Average Salary by Country")

    salary_by_country = df.groupby("Country")["Salary"].mean().sort_values()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=salary_by_country.values, y=salary_by_country.index, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("Average Salary (USD)", fontsize=12)
    ax2.set_ylabel("Country", fontsize=12)
    ax2.set_title("Mean Salary Based on Country", fontsize=14)
    st.pyplot(fig2)

    # ====== Mean Salary by Experience - Line Chart ======
    st.subheader("📈 Salary Trends Based on Experience")

    salary_by_experience = df.groupby("YearsCodePro")["Salary"].mean()

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=salary_by_experience.index, y=salary_by_experience.values, marker="o", linewidth=2.5, color="red",
                 ax=ax3)
    ax3.set_xlabel("Years of Experience", fontsize=12)
    ax3.set_ylabel("Average Salary (USD)", fontsize=12)
    ax3.set_title("Mean Salary Based on Experience", fontsize=14)
    st.pyplot(fig3)

    # ====== Additional Summary Stats ======
    st.subheader("📊 Quick Statistics")
    st.write(f"**Total Data Points:** {df.shape[0]}")
    st.write(f"**Average Salary:** ${df['Salary'].mean():,.2f}")
    st.write(f"**Highest Salary:** ${df['Salary'].max():,.2f}")
    st.write(f"**Lowest Salary:** ${df['Salary'].min():,.2f}")


# Run the Streamlit Page
if __name__ == "__main__":
    show_explore_page()
