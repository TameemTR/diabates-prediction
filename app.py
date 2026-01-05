import streamlit as st
from utils.auth import login_user, register_user
from datetime import datetime
import os
import pandas as pd


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""


if not st.session_state.logged_in:
    st.markdown("""
        <style>
            .login-box {
                background-color: #f4f4f4;
                padding: 30px;
                width: 400px;
                margin: auto;
                margin-top: 50px;
                border-radius: 15px;
                box-shadow: 0px 0px 12px rgba(0,0,0,0.2);
            }
            input, select {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                width: 100%;
                border: none;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### 🔐 Login or Register", unsafe_allow_html=True)

    option = st.radio("Select option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Register":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Account created! Please log in.")
            else:
                st.error("Username already exists or input is empty.")
    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid login.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


if st.session_state.logged_in:
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.username}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.markdown(f"### Welcome, **{st.session_state.username}**!")
    st.markdown("## Health Risk Prediction")

    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.selectbox("Location", ["Alabama", "Alaska", "Arizona", "Other"])
    smoking = st.selectbox("Smoking History", ["never", "current", "former", "No Info"])
    bmi = st.number_input("BMI", min_value=0.0)
    hba1c = st.number_input("HbA1c Level", min_value=0.0)
    glucose = st.number_input("Blood Glucose Level", min_value=0)
    race = st.selectbox("Race", ["AfricanAmerican", "Asian", "Caucasian", "Hispanic", "Other"])
    has_hypertension = st.checkbox("Do you have hypertension?")
    has_heart_disease = st.checkbox("Do you have heart disease?")

    if st.button("Predict"):
        from utils.predict import predict_diabetes

        input_data = {
            "age": age,
            "gender": gender,
            "location": location,
            "smoking_history": smoking,
            "bmi": bmi,
            "hbA1c_level": hba1c,
            "blood_glucose_level": glucose,
            "hypertension": int(has_hypertension),
            "heart_disease": int(has_heart_disease),
            "race:AfricanAmerican": int(race == "AfricanAmerican"),
            "race:Asian": int(race == "Asian"),
            "race:Caucasian": int(race == "Caucasian"),
            "race:Hispanic": int(race == "Hispanic"),
            "race:Other": int(race == "Other"),
        }


        prediction = predict_diabetes(input_data)

        # Prepare and save the result
        row = {
            "username": st.session_state.username,
            **input_data,
            "diabetes": prediction,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        os.makedirs("data", exist_ok=True)
        file_path = "data/user_data.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            df = pd.DataFrame([row])
        df.to_csv(file_path, index=False)

        # Show result
        if prediction:
            st.error("High risk of diabetes detected.")
        else:
            st.success("Low risk of diabetes.")

    
    if os.path.exists("data/user_data.csv"):
        df = pd.read_csv("data/user_data.csv")
        df_user = df[df["username"] == st.session_state.username]
        if not df_user.empty:
            st.markdown("## 📂 Your Prediction History")
            st.dataframe(df_user.sort_values("timestamp", ascending=False))
        else:
            st.info("No predictions submitted yet.")
