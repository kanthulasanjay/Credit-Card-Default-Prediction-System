import streamlit as st
import pandas as pd
import joblib

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Credit Card Default Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS — LIGHT, COLORFUL THEME
# =====================================================

st.markdown(
    """
    <style>
    /* Overall app background — soft light gradient, NOT black */
    .stApp {
        background: linear-gradient(135deg, #f4f7fb 0%, #eef2f9 40%, #f7f4fb 100%);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #eef3fb 100%);
        border-right: 1px solid #e0e6ef;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #1f3c88;
    }

    /* Hero title card */
    .hero-card {
        background: linear-gradient(120deg, #4f6ef7 0%, #7b5ef0 55%, #b06ae0 100%);
        padding: 28px 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(79, 110, 247, 0.25);
    }
    .hero-card h1 {
        color: white;
        margin-bottom: 6px;
        font-size: 2.1rem;
    }
    .hero-card p {
        color: rgba(255,255,255,0.92);
        font-size: 1.02rem;
        margin: 0;
    }

    /* Section header cards — each with its own colorful accent */
    .section-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 10px;
        margin-bottom: 14px;
        border: 1px solid #eef0f5;
        border-left: 6px solid #4f6ef7;
        box-shadow: 0 2px 10px rgba(20, 30, 60, 0.05);
    }
    .section-card h3 {
        margin: 0;
        color: #2b3a67;
        font-size: 1.15rem;
    }
    .section-card span.sub {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* Distinct accent colors per section */
    .card-repay {
        border-left-color: #4f6ef7;
        background: linear-gradient(120deg, #ffffff 0%, #eef2ff 100%);
    }
    .card-bill {
        border-left-color: #a259e6;
        background: linear-gradient(120deg, #ffffff 0%, #f6eefe 100%);
    }
    .card-pay {
        border-left-color: #16a34a;
        background: linear-gradient(120deg, #ffffff 0%, #eafcf1 100%);
    }
    .card-summary {
        border-left-color: #f2994a;
        background: linear-gradient(120deg, #ffffff 0%, #fff6ec 100%);
    }

    /* Fix Streamlit's default red hover on number-input +/- steppers (default/global) */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background: #eef1f8 !important;
        color: #2b3a67 !important;
        border: none !important;
    }
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {
        background: linear-gradient(120deg, #4f6ef7, #7b5ef0) !important;
        color: #ffffff !important;
    }

    /* Bill Amounts — purple-tinted number inputs */
    .st-key-bill_section div[data-baseweb="input"] {
        background: #f6eefe !important;
        border-radius: 8px;
    }
    .st-key-bill_section button[data-testid="stNumberInputStepDown"],
    .st-key-bill_section button[data-testid="stNumberInputStepUp"] {
        background: #ecd9fb !important;
        color: #6b21a8 !important;
    }
    .st-key-bill_section button[data-testid="stNumberInputStepDown"]:hover,
    .st-key-bill_section button[data-testid="stNumberInputStepUp"]:hover {
        background: linear-gradient(120deg, #a259e6, #c084fc) !important;
        color: #ffffff !important;
    }

    /* Previous Payments — green-tinted number inputs */
    .st-key-pay_section div[data-baseweb="input"] {
        background: #eafcf1 !important;
        border-radius: 8px;
    }
    .st-key-pay_section button[data-testid="stNumberInputStepDown"],
    .st-key-pay_section button[data-testid="stNumberInputStepUp"] {
        background: #d3f5e2 !important;
        color: #15803d !important;
    }
    .st-key-pay_section button[data-testid="stNumberInputStepDown"]:hover,
    .st-key-pay_section button[data-testid="stNumberInputStepUp"]:hover {
        background: linear-gradient(120deg, #16a34a, #4ade80) !important;
        color: #ffffff !important;
    }

    /* Metric-like custom containers */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px 10px;
        border: 1px solid #eef0f5;
        box-shadow: 0 2px 8px rgba(20,30,60,0.05);
    }

    /* Number inputs / sliders container */
    div[data-baseweb="input"] input {
        border-radius: 8px !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(120deg, #4f6ef7, #7b5ef0);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 6px 16px rgba(79,110,247,0.3);
        transition: transform 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(79,110,247,0.4);
        color: white;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #ffffff;
        border-radius: 10px;
        font-weight: 600;
        color: #2b3a67;
    }

    /* Result banners */
    .result-safe {
        background: linear-gradient(120deg, #d7f8e8, #c3f0e0);
        border: 1px solid #7fd8ad;
        color: #0f5132;
        padding: 22px;
        border-radius: 16px;
        font-size: 1.15rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 6px 18px rgba(15, 81, 50, 0.1);
    }
    .result-risk {
        background: linear-gradient(120deg, #ffe1e1, #ffd0d6);
        border: 1px solid #ff9aa8;
        color: #7a1f2b;
        padding: 22px;
        border-radius: 16px;
        font-size: 1.15rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 6px 18px rgba(122, 31, 43, 0.1);
    }

    /* Headings default color */
    h1, h2, h3, h4 {
        color: #2b3a67;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HERO TITLE
# =====================================================

st.markdown(
    """
    <div class="hero-card">
        <h1>💳 Credit Card Default Prediction System</h1>
        <p>Predict whether a customer is likely to default on their next credit card payment using a trained Machine Learning model.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():
    model = joblib.load("Model.pkl")
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"❌ Error loading model:\n\n{e}")
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("## 📝 Customer Details")
st.sidebar.markdown("Fill in the customer's profile information below.")
st.sidebar.markdown("---")

customer_id = st.sidebar.number_input(
    "Customer ID",
    min_value=1,
    value=1,
    step=1
)

limit_bal = st.sidebar.number_input(
    "Credit Limit (₹ / $)",
    min_value=10000,
    max_value=1000000,
    value=200000,
    step=1000
)

sex = st.sidebar.selectbox(
    "Gender",
    options=["F", "M"]
)

education = st.sidebar.selectbox(
    "Education",
    options=[
        "Graduate school",
        "University",
        "High School",
        "Others",
        "Unknown",
        "0"
    ]
)

marriage = st.sidebar.selectbox(
    "Marriage",
    options=[
        "Married",
        "Single",
        "Other",
        "0"
    ]
)

age = st.sidebar.slider(
    "Age",
    min_value=18,
    max_value=80,
    value=30
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Adjust repayment history and bill/payment amounts in the main panel, then click **Predict Default Risk**.")

# =====================================================
# REPAYMENT STATUS
# =====================================================

st.markdown(
    """
    <div class="section-card card-repay">
        <h3>📅 Repayment Status</h3>
        <span class="sub">Payment delay history over the last 6 months (-2 = no consumption, 0 = paid duly, 1-8 = months delayed)</span>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    pay_0 = st.slider("PAY_0 (most recent)", -2, 8, 0)
    pay_2 = st.slider("PAY_2", -2, 8, 0)

with col2:
    pay_3 = st.slider("PAY_3", -2, 8, 0)
    pay_4 = st.slider("PAY_4", -2, 8, 0)

with col3:
    pay_5 = st.slider("PAY_5", -2, 8, 0)
    pay_6 = st.slider("PAY_6 (oldest)", -2, 8, 0)

# =====================================================
# BILL AMOUNTS
# =====================================================

st.markdown(
    """
    <div class="section-card card-bill">
        <h3>💰 Bill Amounts</h3>
        <span class="sub">Statement balance for each of the last 6 months</span>
    </div>
    """,
    unsafe_allow_html=True
)

bill_container = st.container(key="bill_section")
with bill_container:
    b1, b2, b3 = st.columns(3)

    with b1:
        bill_amt1 = st.number_input("BILL_AMT1", value=5000)
        bill_amt2 = st.number_input("BILL_AMT2", value=5000)

    with b2:
        bill_amt3 = st.number_input("BILL_AMT3", value=5000)
        bill_amt4 = st.number_input("BILL_AMT4", value=5000)

    with b3:
        bill_amt5 = st.number_input("BILL_AMT5", value=5000)
        bill_amt6 = st.number_input("BILL_AMT6", value=5000)

# =====================================================
# PAYMENT AMOUNTS
# =====================================================

st.markdown(
    """
    <div class="section-card card-pay">
        <h3>💵 Previous Payments</h3>
        <span class="sub">Amount actually paid in each of the last 6 months</span>
    </div>
    """,
    unsafe_allow_html=True
)

pay_container = st.container(key="pay_section")
with pay_container:
    p1, p2, p3 = st.columns(3)

    with p1:
        pay_amt1 = st.number_input("PAY_AMT1", value=2000)
        pay_amt2 = st.number_input("PAY_AMT2", value=2000)

    with p2:
        pay_amt3 = st.number_input("PAY_AMT3", value=2000)
        pay_amt4 = st.number_input("PAY_AMT4", value=2000)

    with p3:
        pay_amt5 = st.number_input("PAY_AMT5", value=2000)
        pay_amt6 = st.number_input("PAY_AMT6", value=2000)

# =====================================================
# CREATE INPUT DATAFRAME
# =====================================================

input_df = pd.DataFrame({
    "id": [customer_id],
    "limit_bal": [float(limit_bal)],
    "sex": [sex],
    "education": [education],
    "marriage": [marriage],
    "age": [int(age)],
    "pay_0": [int(pay_0)],
    "pay_2": [int(pay_2)],
    "pay_3": [int(pay_3)],
    "pay_4": [int(pay_4)],
    "pay_5": [int(pay_5)],
    "pay_6": [int(pay_6)],
    "bill_amt1": [float(bill_amt1)],
    "bill_amt2": [float(bill_amt2)],
    "bill_amt3": [float(bill_amt3)],
    "bill_amt4": [float(bill_amt4)],
    "bill_amt5": [float(bill_amt5)],
    "bill_amt6": [float(bill_amt6)],
    "pay_amt1": [float(pay_amt1)],
    "pay_amt2": [float(pay_amt2)],
    "pay_amt3": [float(pay_amt3)],
    "pay_amt4": [float(pay_amt4)],
    "pay_amt5": [float(pay_amt5)],
    "pay_amt6": [float(pay_amt6)]
})

# =====================================================
# DISPLAY INPUT DATA
# =====================================================

st.markdown(
    """
    <div class="section-card card-summary">
        <h3>📋 Input Summary</h3>
        <span class="sub">Review the data that will be sent to the model</span>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("🔍 View Input Data"):
    st.dataframe(input_df, use_container_width=True)

with st.expander("🔍 View Data Types"):
    dtype_df = pd.DataFrame({
        "Column": input_df.columns,
        "Data Type": input_df.dtypes.astype(str)
    })
    st.dataframe(dtype_df, use_container_width=True)

# =====================================================
# PREDICTION
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

predict_btn = st.button(
    "🔍 Predict Default Risk",
    use_container_width=True
)

if predict_btn:

    try:

        # Make prediction
        prediction = model.predict(input_df)[0]

        # Get probability (if supported)
        probability = None
        try:
            probability = model.predict_proba(input_df)[0][1]
        except Exception:
            probability = None

        st.markdown("<br>", unsafe_allow_html=True)

        if probability is not None:
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Default Probability", f"{probability:.2%}")
            with m2:
                st.metric("Safe Probability", f"{(1 - probability):.2%}")
            with m3:
                st.metric("Predicted Class", "Default" if prediction == 1 else "No Default")

            st.progress(min(max(probability, 0.0), 1.0))

        st.markdown("<br>", unsafe_allow_html=True)

        if prediction == 1:
            st.markdown(
                '<div class="result-risk">⚠️ This customer is <u>likely to DEFAULT</u> on their next payment.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="result-safe">✅ This customer is <u>NOT likely to default</u> on their next payment.</div>',
                unsafe_allow_html=True
            )

    except Exception as e:

        st.error("Prediction Failed")

        st.code(str(e))

        st.subheader("Input Data")

        st.dataframe(input_df)

        st.subheader("Data Types")

        st.write(input_df.dtypes)