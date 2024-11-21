import streamlit as st
import plotly.express as px
from llmProcessing import *
from riskScoreCalculation import *
from assetWeightageCalculation import *

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: black;
            margin-bottom: 1rem;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1rem;
            color: #2C3E50;
        }
        .sidebar-section {
            border: 1px solid #ddd;
            padding: 1rem;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .info-box {
            background-color: #f2f2f2;
            padding: 0.5rem;
            border-left: 5px solid #4CAF50;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Personalized Portfolio Optimization</h1>', unsafe_allow_html=True)

# Function to display pie charts
# Function to display pie charts
def display_pie_charts(weights1, weights2, weights3):
    labels1, values1 = zip(*weights1.items())
    labels2, values2 = zip(*weights2.items())
    labels3, values3 = zip(*weights3.items())

    fig1 = px.pie(
        names=labels1, 
        values=values1, 
        title="MVO (High Risk)", 
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2 = px.pie(
        names=labels2, 
        values=values2, 
        title="Risk Parity (Medium Risk)", 
        color_discrete_sequence=px.colors.sequential.Turbo
    )
    fig3 = px.pie(
        names=labels3, 
        values=values3, 
        title="Min Variance (Low Risk)", 
        color_discrete_sequence=px.colors.sequential.Magma  # Updated color theme
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)

    risk_level = st.session_state["risk_category"]
    if 'optimized_weights1' in st.session_state and 'optimized_weights2' in st.session_state and 'optimized_weights3' in st.session_state:
        optimized_weights1 = st.session_state.optimized_weights1
        optimized_weights2 = st.session_state.optimized_weights2
        optimized_weights3 = st.session_state.optimized_weights3

        optimized_portfolio1 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights1.items()])
        optimized_portfolio2 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights2.items()])
        optimized_portfolio3 = ", ".join([f"{ticker}: {weight}" for ticker, weight in optimized_weights3.items()])

        result = optimize_portfolio_with_llm(risk_level, optimized_portfolio1, optimized_portfolio2, optimized_portfolio3)
        st.session_state["result"] = result

        # Redesigned LLM Optimized Portfolio Display
        st.markdown(f"""
        <div style="
            background-color: #e8f5e9; 
            padding: 1rem; 
            border-radius: 8px; 
            border-left: 5px solid #4CAF50;
            font-size: 1.1rem;
            color: #2C3E50;
            margin-top: 1rem;">
            <strong>LLM Optimized Portfolio:</strong> {result}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please calculate portfolio allocation first!")

# Sidebar with collapsible sections
# Sidebar with collapsible sections
with st.sidebar:
    st.markdown('<h2 class="section-title">Risk Calculation</h2>', unsafe_allow_html=True)
    with st.expander("Input Risk Details", expanded=True):
        gender = st.selectbox("Gender", ["Female", "Male"])
        gender_value = 0 if gender == "Female" else 1

        age = st.slider("Age", min_value=18, max_value=70, value=30)
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=600)
        employment_status_text = st.selectbox("Employment Status", ["Employed", "Self-employed", "Unemployed"])
        employment_status = 0 if employment_status_text == "Employed" else 1 if employment_status_text == "Self-employed" else 2
        dependents = st.slider("Dependents", min_value=0, max_value=10, value=0)

        goal_amount = st.number_input("Goal Amount ($)", min_value=10000, max_value=500000, value=50000)
        goal_duration = st.slider("Goal Duration (months)", min_value=6, max_value=240, value=60)

        monthly_debt_payments = st.number_input("Monthly Debt Payments ($)", min_value=0, max_value=5000, value=500)
        monthly_income = st.number_input("Monthly Income ($)", min_value=2000, max_value=15000, value=4000)

        debt_to_income_ratio = monthly_debt_payments / monthly_income if monthly_income > 0 else 0.0

        savings_account_balance = st.number_input("Savings Account Balance ($)", min_value=0, max_value=100000, value=5000)
        checking_account_balance = st.number_input("Checking Account Balance ($)", min_value=0, max_value=50000, value=2000)

        total_assets = st.number_input("Total Assets ($)", min_value=10000, max_value=1000000, value=100000)
        total_liabilities = st.number_input("Total Liabilities ($)", min_value=0, max_value=500000, value=20000)

        home_ownership_text = st.selectbox("Home Ownership", ["Mortgage", "Own", "Rent"])
        home_ownership = 0 if home_ownership_text == "Mortgage" else 1 if home_ownership_text == "Own" else 2

        monthly_expense = st.number_input("Monthly Expense ($)", min_value=0, max_value=15000, value=2000)
        medical_insurance_text = st.selectbox("Medical Insurance", ["No", "Yes"])
        medical_insurance = 0 if medical_insurance_text == "No" else 1

        if st.button("Calculate Risk Score"):
            inputs = [
                gender_value, age, credit_score, employment_status, goal_amount, goal_duration,
                monthly_debt_payments, debt_to_income_ratio, savings_account_balance,
                checking_account_balance, total_assets, total_liabilities, monthly_income,
                dependents, home_ownership, monthly_expense, medical_insurance
            ]
            predicted_risk_score, risk_category = calculate_risk_score(inputs)
            st.session_state["risk_category"] = risk_category
            st.session_state["risk_score"] = predicted_risk_score
        if "risk_score" in st.session_state and "risk_category" in st.session_state:
            st.markdown(f"<div class='info-box'>**Predicted Risk Score:** {st.session_state['risk_score']:.2f}</div>", unsafe_allow_html=True)
            


# Portfolio Optimization Section
st.markdown('<h2 class="section-title">Portfolio Optimization</h2>', unsafe_allow_html=True)
available_tickers = ['SPY', 'VEA', 'EEM', 'GLD', 'AGG', 'AAPL', 'TSLA', 'MSFT', 'GOOG', 'AMZN']
selected_tickers = st.multiselect(
    "Select assets to add to your portfolio",
    available_tickers,
    default=['SPY', 'AAPL', 'GOOG']
)

if st.button("Calculate Portfolio Allocation"):
    df = download_data(selected_tickers)
    if df.empty:
        st.warning("No data retrieved for the selected tickers. Please check tickers and date range.")
    else:
        optimized_weights1, optimized_weights2, optimized_weights3 = calculate_optimization(df)
        st.session_state.optimized_weights1 = optimized_weights1
        st.session_state.optimized_weights2 = optimized_weights2
        st.session_state.optimized_weights3 = optimized_weights3

# Display pie charts and risk score
if "optimized_weights1" in st.session_state:
    display_pie_charts(
        st.session_state["optimized_weights1"],
        st.session_state["optimized_weights2"],
        st.session_state["optimized_weights3"]
    )
