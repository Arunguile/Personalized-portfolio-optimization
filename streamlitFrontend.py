import streamlit as st
import plotly.express as px
from llmProcessing import *
from riskScoreCalculation import *
from assetWeightageCalculation import *


def display_pie_charts(weights1, weights2, weights3):
    # Converting weights dictionaries into lists of labels and values
    labels1, values1 = zip(*weights1.items())
    labels2, values2 = zip(*weights2.items())
    labels3, values3 = zip(*weights3.items())
    
    # Creating three pie charts using plotly
    fig1 = px.pie(names=labels1, values=values1, title="MVO (High Risk)")
    fig2 = px.pie(names=labels2, values=values2, title="Risk Parity (Medium Risk)")
    fig3 = px.pie(names=labels3, values=values3, title="Min Variance (Low Risk)")
    
    # Display the pie charts in three columns below the title
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.plotly_chart(fig2)
    with col3:
        st.plotly_chart(fig3)
        
    
    risk_level = st.session_state["risk_category"]  # Getting risk category
    if 'optimized_weights1' in st.session_state and 'optimized_weights2' in st.session_state and 'optimized_weights3' in st.session_state:
        optimized_weights1 = st.session_state.optimized_weights1
        optimized_weights2 = st.session_state.optimized_weights2
        optimized_weights3 = st.session_state.optimized_weights3
        optimized_portfolio1 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights1.items()])
        optimized_portfolio2 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights2.items()])
        optimized_portfolio3 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights3.items()])
            
        result = optimize_portfolio_with_llm(risk_level, optimized_portfolio1, optimized_portfolio2, optimized_portfolio3)
        st.session_state["result"] = result
        st.write("LLM Optimized Portfolio:", result)
    else:
        st.warning("Please calculate portfolio allocation first!")


st.title("Personalized Portfolio Optimization")

# -- sidebar -- 
with st.sidebar:

    # Risk Calculation Section
    st.subheader("Risk Calculation")
    age = st.slider("Age", min_value=18, max_value=70, value=30)
    credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=600)
    employment_status_text = st.selectbox("Employment Status", ["Employed", "Self-employed", "Unemployed"])
    employment_status = 0 if employment_status_text == "Employed" else 1 if employment_status_text == "Self-employed" else 2
    experience = st.slider("Experience (years)", min_value=0, max_value=40, value=5)
    goal_amount = st.number_input("Goal Amount ($)", min_value=10000, max_value=500000, value=50000)
    goal_duration = st.slider("Goal Duration (months)", min_value=6, max_value=240, value=60)
    monthly_debt_payments = st.number_input("Monthly Debt Payments ($)", min_value=0, max_value=5000, value=500)
    monthly_income = st.number_input("Monthly Income ($)", min_value=2000, max_value=15000, value=4000)
    
    debt_to_income_ratio = monthly_debt_payments / monthly_income if monthly_income > 0 else 0.0
    savings_account_balance = st.number_input("Savings Account Balance ($)", min_value=0, max_value=100000, value=5000)
    checking_account_balance = st.number_input("Checking Account Balance ($)", min_value=0, max_value=50000, value=2000)
    total_assets = st.number_input("Total Assets ($)", min_value=10000, max_value=1000000, value=100000)
    total_liabilities = st.number_input("Total Liabilities ($)", min_value=0, max_value=500000, value=20000)

    # Calculate risk score on button click
    if st.button("Calculate Risk Score"):
        inputs = [
            age, credit_score, employment_status, experience, goal_amount, goal_duration,
            monthly_debt_payments, debt_to_income_ratio, savings_account_balance,
            checking_account_balance, total_assets, total_liabilities, monthly_income
        ]
        print(inputs)
        
        predicted_risk_score, risk_category = calculate_risk_score(inputs)
        
        st.session_state["risk_category"]=risk_category
        st.session_state["risk_score"]=predicted_risk_score
    if "risk_score" in st.session_state.keys() and "risk_category" in st.session_state.keys():
        st.write(f"Predicted Risk Score: {st.session_state["risk_score"]:.2f}")


    # Portfolio Optimization Section
    st.subheader("Portfolio")
    available_tickers = ['SPY', 'VEA', 'EEM', 'GLD', 'AGG', 'AAPL', 'TSLA', 'MSFT', 'GOOG', 'AMZN']
    selected_tickers = st.multiselect(
        "Select assets to add to your portfolio", available_tickers, default=['SPY', 'AAPL', 'GOOG']
    )

    if st.button("Calculate Portfolio Allocation"):
        df = download_data(selected_tickers)
        if df.empty:
            st.warning("No data retrieved for the selected tickers. Please check tickers and date range.")
        else:
            optimized_weights1, optimized_weights2, optimized_weights3  = calculate_optimization(df)
            print(st.session_state.risk_category)
            st.session_state.optimized_weights1 = optimized_weights1  # Save optimized weights in session state
            st.session_state.optimized_weights2 = optimized_weights2
            st.session_state.optimized_weights3 = optimized_weights3
            
            
    if "optimized_weights1" in st.session_state.keys() and "optimized_weights2" in st.session_state.keys() and "optimized_weights3" in st.session_state.keys():
        st.write("Optimized Portfolio Weights:", st.session_state["optimized_weights1"])
        st.write("Optimized Portfolio Weights:", st.session_state["optimized_weights2"])
        st.write("Optimized Portfolio Weights:", st.session_state["optimized_weights3"])


if "optimized_weights1" in st.session_state and "optimized_weights2" in st.session_state and "optimized_weights3" in st.session_state:
    display_pie_charts(st.session_state["optimized_weights1"], st.session_state["optimized_weights2"], st.session_state["optimized_weights3"])

