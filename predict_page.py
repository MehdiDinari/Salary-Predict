import streamlit as st
import pickle
import numpy as np
import os



# Load Model with Caching for Efficiency
@st.cache_resource
def load_model():
    model_path = "saved_steps.pkl"
    if not os.path.exists(model_path):
        st.error("Error: Model file not found! Please check 'saved_steps.pkl'.")
        return None
    try:
        with open(model_path, "rb") as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


data = load_model()
if data:
    regressor = data.get("model")
    le_country = data.get("le_country")
    le_education = data.get("le_education")


# Function to Show Prediction Page
def show_predict_page():
    st.title("💼 Software Developer Salary Prediction 💰")

    st.markdown(
        """
        ### 🔍 **Provide the following details to estimate your salary:**
        """
    )

    # Country Selection
    countries = [
        "United States", "India", "United Kingdom", "Germany", "Canada",
        "Brazil", "France", "Spain", "Australia", "Netherlands", "Poland",
        "Italy", "Russian Federation", "Sweden"
    ]
    country = st.selectbox("🌍 Select Your Country", countries)

    # Education Level Selection
    education_levels = [
        "Less than a Bachelor's", "Bachelor’s degree",
        "Master’s degree", "Post grad"
    ]
    education = st.selectbox("🎓 Highest Education Level", education_levels)

    # Experience Input
    experience = st.slider("💼 Years of Experience", 0, 50, 3)

    # Prediction Button
    if st.button("📊 Predict Salary"):
        if not data:
            st.error("⚠️ Model is unavailable. Please check and reload the page.")
            return

        # Prepare input for prediction
        try:
            X = np.array([[country, education, experience]])
            X[:, 0] = le_country.transform(X[:, 0])
            X[:, 1] = le_education.transform(X[:, 1])
            X = X.astype(float)

            # Predict Salary
            salary = regressor.predict(X)
            st.success(f"🤑 **Estimated Salary:** ${salary[0]:,.2f} per year")

        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")


# Run the Streamlit Page
if __name__ == "__main__":
    show_predict_page()
