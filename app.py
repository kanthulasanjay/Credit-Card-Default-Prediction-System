
import streamlit as st
import pandas as pd
import joblib


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Credit Card Default Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #f4f7fb 0%,
            #eef2f9 40%,
            #f7f4fb 100%
        );
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #ffffff 0%,
            #eef3fb 100%
        );
        border-right: 1px solid #e0e6ef;
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #1f3c88;
    }

    .hero-card {
        background: linear-gradient(
            120deg,
            #4f6ef7 0%,
            #7b5ef0 55%,
            #b06ae0 100%
        );
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
        color: rgba(255, 255, 255, 0.92);
        font-size: 1.02rem;
        margin: 0;
    }

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

    .card-repay {
        border-left-color: #4f6ef7;
        background: linear-gradient(
            120deg,
            #ffffff 0%,
            #eef2ff 100%
        );
    }

    .card-bill {
        border-left-color: #a259e6;
        background: linear-gradient(
            120deg,
            #ffffff 0%,
            #f6eefe 100%
        );
    }

    .card-pay {
        border-left-color: #16a34a;
        background: linear-gradient(
            120deg,
            #ffffff 0%,
            #eafcf1 100%
        );
    }

    .card-summary {
        border-left-color: #f2994a;
        background: linear-gradient(
            120deg,
            #ffffff 0%,
            #fff6ec 100%
        );
    }

    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background: #eef1f8 !important;
        color: #2b3a67 !important;
        border: none !important;
    }

    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {
        background: linear-gradient(
            120deg,
            #4f6ef7,
            #7b5ef0
        ) !important;
        color: #ffffff !important;
    }

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
        background: linear-gradient(
            120deg,
            #a259e6,
            #c084fc
        ) !important;
        color: #ffffff !important;
    }

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
        background: linear-gradient(
            120deg,
            #16a34a,
            #4ade80
        ) !important;
        color: #ffffff !important;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px 10px;
        border: 1px solid #eef0f5;
        box-shadow: 0 2px 8px rgba(20,30,60,0.05);
    }

    div[data-baseweb="input"] input {
        border-radius: 8px !important;
    }

    .stButton > button {
        background: linear-gradient(
            120deg,
            #4f6ef7,
            #7b5ef0
        );
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

    .streamlit-expanderHeader {
        background: #ffffff;
        border-radius: 10px;
        font-weight: 600;
        color: #2b3a67;
    }

    .result-safe {
        background: linear-gradient(
            120deg,
            #d7f8e8,
            #c3f0e0
        );
        border: 1px solid #7fd8ad;
        color: #0f5132;
        padding: 22px;
        border-radius: 16px;
        font-size: 1.15rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 6px 18px rgba(15,81,50,0.1);
    }

    .result-risk {
        background: linear-gradient(
            120deg,
            #ffe1e1,
            #ffd0d6
        );
        border: 1px solid #ff9aa8;
        color: #7a1f2b;
        padding: 22px;
        border-radius: 16px;
        font-size: 1.15rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 6px 18px rgba(122,31,43,0.1);
    }

    h1, h2, h3, h4 {
        color: #2b3a67;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <h1>💳 Credit Card Default Prediction System</h1>
        <p>
            Predict whether a customer is likely to default on
            their next credit card payment using a trained
            Machine Learning model.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("Model.pkl")


try:
    model = load_model()

except Exception as e:
    st.error("❌ Error loading Model.pkl")
    st.code(str(e))
    st.stop()


# ============================================================
# EXPECTED FEATURES
# ============================================================

EXPECTED_FEATURES = [
    "LIMIT_BAL",
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "AGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6"
]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 📝 Customer Details")

st.sidebar.markdown(
    "Fill in the customer's profile information below."
)

st.sidebar.markdown("---")


customer_id = st.sidebar.number_input(
    "Customer ID",
    min_value=1,
    value=1,
    step=1
)


limit_bal = st.sidebar.number_input(
    "Credit Limit",
    min_value=10000,
    max_value=1000000,
    value=200000,
    step=1000
)


# ============================================================
# CATEGORICAL FEATURES
# ============================================================

# These values MUST remain strings.
# Your saved Model.pkl contains an OrdinalEncoder
# for these three columns.

sex = st.sidebar.selectbox(
    "Gender",
    [
        "F",
        "M"
    ]
)


education = st.sidebar.selectbox(
    "Education",
    [
        "0",
        "Graduate school",
        "High School",
        "Others",
        "University",
        "Unknown"
    ]
)


marriage = st.sidebar.selectbox(
    "Marriage",
    [
        "0",
        "Married",
        "Other",
        "Single"
    ]
)


age = st.sidebar.slider(
    "Age",
    min_value=18,
    max_value=80,
    value=30
)


st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Adjust repayment history and bill/payment "
    "amounts in the main panel, then click "
    "**Predict Default Risk**."
)


# ============================================================
# REPAYMENT STATUS
# ============================================================

st.markdown(
    """
    <div class="section-card card-repay">
        <h3>📅 Repayment Status</h3>
        <span class="sub">
            Payment delay history over the last 6 months.
            -2 = no consumption, 0 = paid duly,
            positive values = months delayed.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    pay_0 = st.slider(
        "PAY_0 (most recent)",
        min_value=-2,
        max_value=8,
        value=0
    )

    pay_2 = st.slider(
        "PAY_2",
        min_value=-2,
        max_value=8,
        value=0
    )


with col2:

    pay_3 = st.slider(
        "PAY_3",
        min_value=-2,
        max_value=8,
        value=0
    )

    pay_4 = st.slider(
        "PAY_4",
        min_value=-2,
        max_value=8,
        value=0
    )


with col3:

    pay_5 = st.slider(
        "PAY_5",
        min_value=-2,
        max_value=8,
        value=0
    )

    pay_6 = st.slider(
        "PAY_6 (oldest)",
        min_value=-2,
        max_value=8,
        value=0
    )


# ============================================================
# BILL AMOUNTS
# ============================================================

st.markdown(
    """
    <div class="section-card card-bill">
        <h3>💰 Bill Amounts</h3>
        <span class="sub">
            Statement balance for each of the last 6 months.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


bill_container = st.container(
    key="bill_section"
)


with bill_container:

    b1, b2, b3 = st.columns(3)


    with b1:

        bill_amt1 = st.number_input(
            "BILL_AMT1",
            min_value=0,
            value=5000,
            step=100
        )

        bill_amt2 = st.number_input(
            "BILL_AMT2",
            min_value=0,
            value=5000,
            step=100
        )


    with b2:

        bill_amt3 = st.number_input(
            "BILL_AMT3",
            min_value=0,
            value=5000,
            step=100
        )

        bill_amt4 = st.number_input(
            "BILL_AMT4",
            min_value=0,
            value=5000,
            step=100
        )


    with b3:

        bill_amt5 = st.number_input(
            "BILL_AMT5",
            min_value=0,
            value=5000,
            step=100
        )

        bill_amt6 = st.number_input(
            "BILL_AMT6",
            min_value=0,
            value=5000,
            step=100
        )


# ============================================================
# PREVIOUS PAYMENTS
# ============================================================

st.markdown(
    """
    <div class="section-card card-pay">
        <h3>💵 Previous Payments</h3>
        <span class="sub">
            Amount actually paid in each of the last 6 months.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


pay_container = st.container(
    key="pay_section"
)


with pay_container:

    p1, p2, p3 = st.columns(3)


    with p1:

        pay_amt1 = st.number_input(
            "PAY_AMT1",
            min_value=0,
            value=2000,
            step=100
        )

        pay_amt2 = st.number_input(
            "PAY_AMT2",
            min_value=0,
            value=2000,
            step=100
        )


    with p2:

        pay_amt3 = st.number_input(
            "PAY_AMT3",
            min_value=0,
            value=2000,
            step=100
        )

        pay_amt4 = st.number_input(
            "PAY_AMT4",
            min_value=0,
            value=2000,
            step=100
        )


    with p3:

        pay_amt5 = st.number_input(
            "PAY_AMT5",
            min_value=0,
            value=2000,
            step=100
        )

        pay_amt6 = st.number_input(
            "PAY_AMT6",
            min_value=0,
            value=2000,
            step=100
        )


# ============================================================
# CREATE INPUT DATAFRAME
# ============================================================

input_df = pd.DataFrame({

    "LIMIT_BAL": [
        float(limit_bal)
    ],

    "SEX": [
        sex
    ],

    "EDUCATION": [
        education
    ],

    "MARRIAGE": [
        marriage
    ],

    "AGE": [
        int(age)
    ],

    "PAY_0": [
        int(pay_0)
    ],

    "PAY_2": [
        int(pay_2)
    ],

    "PAY_3": [
        int(pay_3)
    ],

    "PAY_4": [
        int(pay_4)
    ],

    "PAY_5": [
        int(pay_5)
    ],

    "PAY_6": [
        int(pay_6)
    ],

    "BILL_AMT1": [
        float(bill_amt1)
    ],

    "BILL_AMT2": [
        float(bill_amt2)
    ],

    "BILL_AMT3": [
        float(bill_amt3)
    ],

    "BILL_AMT4": [
        float(bill_amt4)
    ],

    "BILL_AMT5": [
        float(bill_amt5)
    ],

    "BILL_AMT6": [
        float(bill_amt6)
    ],

    "PAY_AMT1": [
        float(pay_amt1)
    ],

    "PAY_AMT2": [
        float(pay_amt2)
    ],

    "PAY_AMT3": [
        float(pay_amt3)
    ],

    "PAY_AMT4": [
        float(pay_amt4)
    ],

    "PAY_AMT5": [
        float(pay_amt5)
    ],

    "PAY_AMT6": [
        float(pay_amt6)
    ]

})


# ============================================================
# EXACT FEATURE ORDER
# ============================================================

input_df = input_df[EXPECTED_FEATURES]


# ============================================================
# VALIDATE INPUT
# ============================================================

missing_columns = [
    column
    for column in EXPECTED_FEATURES
    if column not in input_df.columns
]


if missing_columns:

    st.error("❌ Missing model columns")

    st.write(missing_columns)

    st.stop()


# ============================================================
# INPUT SUMMARY
# ============================================================

st.markdown(
    """
    <div class="section-card card-summary">
        <h3>📋 Input Summary</h3>
        <span class="sub">
            Review the data that will be sent to the model.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VIEW INPUT
# ============================================================

with st.expander("🔍 View Input Data"):

    st.dataframe(
        input_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# VIEW DATA TYPES
# ============================================================

with st.expander("🔍 View Data Types"):

    dtype_df = pd.DataFrame({
        "Column": [
            str(column)
            for column in input_df.columns
        ],
        "Data Type": [
            str(dtype)
            for dtype in input_df.dtypes
        ]
    })


    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# VIEW CATEGORICAL VALUES
# ============================================================

with st.expander("🔤 View Categorical Values"):

    categorical_df = pd.DataFrame({
        "Feature": [
            "SEX",
            "EDUCATION",
            "MARRIAGE"
        ],
        "Selected Value": [
            str(sex),
            str(education),
            str(marriage)
        ]
    })


    st.dataframe(
        categorical_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PREDICT BUTTON
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)


predict_btn = st.button(
    "🔍 Predict Default Risk",
    use_container_width=True
)


# ============================================================
# PREDICTION
# ============================================================

if predict_btn:

    try:

        # ----------------------------------------------------
        # RAW MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            input_df
        )[0]


        prediction_str = str(
            prediction
        ).strip()


        prediction_upper = prediction_str.upper()


        # ----------------------------------------------------
        # POSSIBLE DEFAULT LABELS
        # ----------------------------------------------------

        default_values = {
            "Y",
            "YES",
            "1",
            "TRUE",
            "DEFAULT",
            "DEFAULTED",
            "D"
        }


        no_default_values = {
            "N",
            "NO",
            "0",
            "FALSE",
            "NO DEFAULT",
            "NON-DEFAULT",
            "NON DEFAULT",
            "ND"
        }


        # ----------------------------------------------------
        # DETERMINE RESULT
        # ----------------------------------------------------

        if prediction_upper in default_values:

            is_default = True


        elif prediction_upper in no_default_values:

            is_default = False


        else:

            # Numeric fallback
            try:

                numeric_prediction = float(
                    prediction_str
                )

                is_default = (
                    numeric_prediction == 1
                )

            except ValueError:

                # If the model produces an unknown
                # string label, don't crash.
                # Show it as the raw prediction.

                is_default = False


        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        probability = None


        try:

            probabilities = model.predict_proba(
                input_df
            )[0]


            # Get final classifier
            final_model = model.named_steps.get(
                "model",
                None
            )


            if (
                final_model is not None
                and hasattr(
                    final_model,
                    "classes_"
                )
            ):

                classes = list(
                    final_model.classes_
                )


                default_index = None


                for index, class_value in enumerate(
                    classes
                ):

                    class_string = str(
                        class_value
                    ).strip().upper()


                    if class_string in default_values:

                        default_index = index

                        break


                # If the model uses 0/1 classes
                if default_index is None:

                    for index, class_value in enumerate(
                        classes
                    ):

                        try:

                            if float(
                                class_value
                            ) == 1:

                                default_index = index

                                break

                        except Exception:

                            pass


                # Fallback for binary classifier
                if default_index is None:

                    if len(probabilities) == 2:

                        default_index = 1


                if default_index is not None:

                    probability = float(
                        probabilities[
                            default_index
                        ]
                    )


            else:

                if len(probabilities) == 2:

                    probability = float(
                        probabilities[1]
                    )


        except Exception:

            probability = None


        # ----------------------------------------------------
        # DISPLAY METRICS
        # ----------------------------------------------------

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        if probability is not None:

            m1, m2, m3 = st.columns(3)


            with m1:

                st.metric(
                    "Default Probability",
                    f"{probability:.2%}"
                )


            with m2:

                st.metric(
                    "Safe Probability",
                    f"{1 - probability:.2%}"
                )


            with m3:

                st.metric(
                    "Predicted Class",
                    "Default"
                    if is_default
                    else "No Default"
                )


            st.progress(
                min(
                    max(
                        probability,
                        0.0
                    ),
                    1.0
                )
            )


        else:

            st.metric(
                "Predicted Class",
                "Default"
                if is_default
                else "No Default"
            )


        # ----------------------------------------------------
        # RESULT MESSAGE
        # ----------------------------------------------------

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        if is_default:

            st.markdown(
                """
                <div class="result-risk">
                    ⚠️ This customer is
                    <u>LIKELY TO DEFAULT</u>
                    on their next payment.
                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            st.markdown(
                """
                <div class="result-safe">
                    ✅ This customer is
                    <u>NOT LIKELY TO DEFAULT</u>
                    on their next payment.
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # PREDICTION DETAILS
        # ----------------------------------------------------

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        st.subheader(
            "📊 Prediction Details"
        )


        result_df = pd.DataFrame({
            "Customer ID": [
                customer_id
            ],

            "Raw Model Prediction": [
                prediction_str
            ],

            "Prediction": [
                "Default"
                if is_default
                else "No Default"
            ],

            "Default Probability": [
                f"{probability:.2%}"
                if probability is not None
                else "N/A"
            ]
        })


        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # RISK INTERPRETATION
        # ----------------------------------------------------

        if probability is not None:

            st.subheader(
                "💡 Risk Interpretation"
            )


            if probability >= 0.70:

                st.error(
                    "🔴 High Risk: "
                    "The model estimates a high probability "
                    "of credit-card default."
                )


            elif probability >= 0.40:

                st.warning(
                    "🟠 Moderate Risk: "
                    "The customer shows some indicators "
                    "of potential default."
                )


            else:

                st.success(
                    "🟢 Lower Risk: "
                    "The model estimates a relatively "
                    "low probability of default."
                )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        st.error(
            "❌ Prediction Failed"
        )


        st.code(
            str(e)
        )


        st.subheader(
            "Input Data Sent to Model"
        )


        st.dataframe(
            input_df,
            use_container_width=True,
            hide_index=True
        )


        st.subheader(
            "Input Data Types"
        )


        error_dtype_df = pd.DataFrame({
            "Column": [
                str(column)
                for column in input_df.columns
            ],

            "Data Type": [
                str(dtype)
                for dtype in input_df.dtypes
            ]
        })


        st.dataframe(
            error_dtype_df,
            use_container_width=True,
            hide_index=True
        )

