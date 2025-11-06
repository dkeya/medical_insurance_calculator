import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Medical Insurance Calculator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Hide Streamlit footer */
    footer {visibility: hidden;}

    /* Hide GitHub viewer badge (handle any container class) */
    [data-testid="stAppViewContainer"] > .main > div:has(> .viewerBadge_link__1S137),
    .viewerBadge_container__r5tak,
    .st-emotion-cache-1b4cjjp {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .price-display {
        background-color: #f0f8ff;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
        border-left: 5px solid #1f77b4;
    }
    .summary-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        position: relative;
    }
    .step {
        text-align: center;
        flex: 1;
        padding: 0.5rem;
        position: relative;
        z-index: 2;
    }
    .step.active {
        font-weight: bold;
        color: #1f77b4;
    }
    .step.completed {
        color: #28a745;
    }
    .progress-bar {
        position: absolute;
        top: 25px;
        left: 0;
        height: 3px;
        background-color: #1f77b4;
        z-index: 1;
        transition: width 0.3s ease;
    }
    .progress-background {
        position: absolute;
        top: 25px;
        left: 0;
        right: 0;
        height: 3px;
        background-color: #e9ecef;
        z-index: 1;
    }
    .currency-toggle {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .currency-btn {
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        border: 1px solid #1f77b4;
        border-radius: 5px;
        cursor: pointer;
        background-color: white;
    }
    .currency-btn.active {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Rate card data
ALL_HOSPITALS_RATES = {
    "justMe": {
        "18-30": {
            "500K": {"IP only": 20000, "IP & OP": 48000, "IP,OP,Maternity": 78000, "IP,OP,Maternity,dental & Optical": 83000},
            "1M": {"IP only": 25000, "IP & OP": 52000, "IP,OP,Maternity": 84000, "IP,OP,Maternity,dental & Optical": 92000},
            "2M": {"IP only": 33000, "IP & OP": 62000, "IP,OP,Maternity": 97000, "IP,OP,Maternity,dental & Optical": 110000},
            "5M": {"IP only": 50000, "IP & OP": 98000, "IP,OP,Maternity": 140000, "IP,OP,Maternity,dental & Optical": 175000}
        },
        "31-40": {
            "500K": {"IP only": 22000, "IP & OP": 49000, "IP,OP,Maternity": 80000, "IP,OP,Maternity,dental & Optical": 85000},
            "1M": {"IP only": 26000, "IP & OP": 53000, "IP,OP,Maternity": 86000, "IP,OP,Maternity,dental & Optical": 93000},
            "2M": {"IP only": 32000, "IP & OP": 64000, "IP,OP,Maternity": 99000, "IP,OP,Maternity,dental & Optical": 113000},
            "5M": {"IP only": 51000, "IP & OP": 101000, "IP,OP,Maternity": 143000, "IP,OP,Maternity,dental & Optical": 179000}
        },
        "41-50": {
            "500K": {"IP only": 23000, "IP & OP": 53000, "IP,OP,Maternity": 84000, "IP,OP,Maternity,dental & Optical": 89000},
            "1M": {"IP only": 32000, "IP & OP": 62000, "IP,OP,Maternity": 95000, "IP,OP,Maternity,dental & Optical": 102000},
            "2M": {"IP only": 39000, "IP & OP": 79000, "IP,OP,Maternity": 114000, "IP,OP,Maternity,dental & Optical": 129000},
            "5M": {"IP only": 62000, "IP & OP": 118000, "IP,OP,Maternity": 160000, "IP,OP,Maternity,dental & Optical": 196000}
        },
        "51-60": {
            "500K": {"IP only": 31000, "IP & OP": 66000, "IP,OP,Maternity": 97000, "IP,OP,Maternity,dental & Optical": 102000},
            "1M": {"IP only": 39000, "IP & OP": 75000, "IP,OP,Maternity": 107000, "IP,OP,Maternity,dental & Optical": 114000},
            "2M": {"IP only": 48000, "IP & OP": 95000, "IP,OP,Maternity": 130000, "IP,OP,Maternity,dental & Optical": 144000},
            "5M": {"IP only": 79000, "IP & OP": 140000, "IP,OP,Maternity": 182000, "IP,OP,Maternity,dental & Optical": 218000}
        }
    },
    "meAndFamily": {
        "18-30": {
            "500K": {"IP only": 37000, "IP & OP": 90000, "IP,OP,Maternity": 120000, "IP,OP,Maternity,dental & Optical": 131000},
            "1M": {"IP only": 47000, "IP & OP": 100000, "IP,OP,Maternity": 133000, "IP,OP,Maternity,dental & Optical": 147000},
            "2M": {"IP only": 55000, "IP & OP": 120000, "IP,OP,Maternity": 155000, "IP,OP,Maternity,dental & Optical": 183000},
            "5M": {"IP only": 91000, "IP & OP": 191000, "IP,OP,Maternity": 233000, "IP,OP,Maternity,dental & Optical": 305000}
        },
        "31-40": {
            "500K": {"IP only": 41000, "IP & OP": 94000, "IP,OP,Maternity": 125000, "IP,OP,Maternity,dental & Optical": 136000},
            "1M": {"IP only": 48000, "IP & OP": 102000, "IP,OP,Maternity": 135000, "IP,OP,Maternity,dental & Optical": 149000},
            "2M": {"IP only": 59000, "IP & OP": 123000, "IP,OP,Maternity": 158000, "IP,OP,Maternity,dental & Optical": 187000},
            "5M": {"IP only": 95000, "IP & OP": 195000, "IP,OP,Maternity": 237000, "IP,OP,Maternity,dental & Optical": 309000}
        },
        "41-50": {
            "500K": {"IP only": 42000, "IP & OP": 103000, "IP,OP,Maternity": 134000, "IP,OP,Maternity,dental & Optical": 144000},
            "1M": {"IP only": 58000, "IP & OP": 119000, "IP,OP,Maternity": 151000, "IP,OP,Maternity,dental & Optical": 165000},
            "2M": {"IP only": 72000, "IP & OP": 152000, "IP,OP,Maternity": 187000, "IP,OP,Maternity,dental & Optical": 216000},
            "5M": {"IP only": 115000, "IP & OP": 227000, "IP,OP,Maternity": 268000, "IP,OP,Maternity,dental & Optical": 340000}
        },
        "51-60": {
            "500K": {"IP only": 57000, "IP & OP": 128000, "IP,OP,Maternity": 139000, "IP,OP,dental & Optical": 139000},
            "1M": {"IP only": 72223, "IP & OP": 143000, "IP,OP,Maternity": 158000, "IP,OP,dental & Optical": 158000},
            "2M": {"IP only": 89000, "IP & OP": 182000, "IP,OP,Maternity": 211000, "IP,OP,dental & Optical": 211000},
            "5M": {"IP only": 145000, "IP & OP": 268000, "IP,OP,Maternity": 339000, "IP,OP,dental & Optical": 339000}
        }
    },
    "myChildOnly": {
        "1": {
            "500K": {"IP only": 21000, "IP & OP": 47000, "IP,OP,Maternity,dental & Optical": 52000},
            "1M": {"IP only": 25000, "IP & OP": 51000, "IP,OP,Maternity,dental & Optical": 58000},
            "2M": {"IP only": 30000, "IP & OP": 62000, "IP,OP,Maternity,dental & Optical": 76000},
            "5M": {"IP only": 48000, "IP & OP": 98000, "IP,OP,Maternity,dental & Optical": 132000}
        }
    },
    "myParents": {
        "1": {
            "500K": {"IP only": 57000, "IP & OP": 117080, "IP,OP,dental & Optical": 145216},
            "1M": {"IP only": 81000, "IP & OP": 141080, "IP,OP,dental & Optical": 169216},
            "2M": {"IP only": 121000, "IP & OP": 181080, "IP,OP,dental & Optical": 209216},
            "5M": {"IP only": 140000, "IP & OP": 200080, "IP,OP,dental & Optical": 228216}
        },
        "2": {
            "500K": {"IP only": 107000, "IP & OP": 167000, "IP,OP,dental & Optical": 195000},
            "1M": {"IP only": 149000, "IP & OP": 209000, "IP,OP,dental & Optical": 237000},
            "2M": {"IP only": 222000, "IP & OP": 282000, "IP,OP,dental & Optical": 310000},
            "5M": {"IP only": 257000, "IP & OP": 317000, "IP,OP,dental & Optical": 345000}
        }
    }
}

RESTRICTED_HOSPITALS_RATES = {
    "justMe": {
        "18-30": {
            "500K": {"IP only": 16000, "IP,OP,Maternity,dental & Optical": 38000},
            "1M": {"IP only": 18000, "IP,OP,Maternity,dental & Optical": 40000},
            "1.5M": {"IP only": 21000, "IP,OP,Maternity,dental & Optical": 42000}
        },
        "31-40": {
            "500K": {"IP only": 17000, "IP,OP,Maternity,dental & Optical": 40000},
            "1M": {"IP only": 20000, "IP,OP,Maternity,dental & Optical": 42000},
            "1.5M": {"IP only": 22000, "IP,OP,Maternity,dental & Optical": 43000}
        },
        "41-50": {
            "500K": {"IP only": 17000, "IP,OP,Maternity,dental & Optical": 40000},
            "1M": {"IP only": 20000, "IP,OP,Maternity,dental & Optical": 42000},
            "1.5M": {"IP only": 22000, "IP,OP,Maternity,dental & Optical": 43000}
        },
        "51-60": {
            "500K": {"IP only": 20000, "IP,OP,Maternity,dental & Optical": 41000},
            "1M": {"IP only": 22000, "IP,OP,Maternity,dental & Optical": 43000},
            "1.5M": {"IP only": 24000, "IP,OP,Maternity,dental & Optical": 46000}
        }
    },
    "meAndFamily": {
        "18-30": {
            "500K": {"IP only": 30000, "IP,OP,Maternity,dental & Optical": 73000},
            "1M": {"IP only": 34000, "IP,OP,Maternity,dental & Optical": 77000},
            "1.5M": {"IP only": 38000, "IP,OP,Maternity,dental & Optical": 81000}
        },
        "31-40": {
            "500K": {"IP only": 32000, "IP,OP,Maternity,dental & Optical": 75000},
            "1M": {"IP only": 35000, "IP,OP,Maternity,dental & Optical": 79000},
            "1.5M": {"IP only": 39000, "IP,OP,Maternity,dental & Optical": 82000}
        },
        "41-50": {
            "500K": {"IP only": 32000, "IP,OP,Maternity,dental & Optical": 75000},
            "1M": {"IP only": 35000, "IP,OP,Maternity,dental & Optical": 79000},
            "1.5M": {"IP only": 39000, "IP,OP,Maternity,dental & Optical": 82000}
        },
        "51-60": {
            "500K": {"IP only": 35000, "IP,OP,Maternity,dental & Optical": 78000},
            "1M": {"IP only": 39000, "IP,OP,Maternity,dental & Optical": 82000},
            "1.5M": {"IP only": 43000, "IP,OP,Maternity,dental & Optical": 86000}
        }
    }
}

def format_currency(amount, currency):
    """Format currency with proper formatting"""
    if currency == "KES":
        return f"KES {amount:,.0f}"
    else:
        return f"USD {amount:,.2f}"

def get_premium_from_rates(cover_type, myself_age, spouse_age, children_count, parent1_age, parent2_age, benefit_package, cover_limit, hospital_type):
    """Get premium from rate cards"""
    rate_card = ALL_HOSPITALS_RATES if hospital_type == "allHospitals" else RESTRICTED_HOSPITALS_RATES
    
    # For budget hospitals, map cover limits to available options
    actual_cover_limit = cover_limit
    if hospital_type == "budgetHospitals":
        if cover_limit == "500K":
            actual_cover_limit = "500K"
        elif cover_limit == "1M":
            actual_cover_limit = "1M"
        else:
            actual_cover_limit = "1.5M"  # For 2M, 5M, above5M in budget hospitals
    
    try:
        if cover_type == "justMe":
            return rate_card["justMe"][myself_age][actual_cover_limit][benefit_package]
        elif cover_type == "meAndFamily":
            return rate_card["meAndFamily"][myself_age][actual_cover_limit][benefit_package]
        elif cover_type == "myChildOnly":
            base_rate = rate_card["myChildOnly"]["1"][actual_cover_limit][benefit_package]
            return base_rate * children_count
        elif cover_type == "myParents":
            parent_count = 2 if parent1_age and parent2_age else 1
            return rate_card["myParents"][str(parent_count)][actual_cover_limit][benefit_package]
    except KeyError:
        # Fallback calculation if specific rate not found
        return calculate_fallback_premium(cover_type, children_count, benefit_package, cover_limit, hospital_type)
    
    return calculate_fallback_premium(cover_type, children_count, benefit_package, cover_limit, hospital_type)

def calculate_fallback_premium(cover_type, children_count, benefit_package, cover_limit, hospital_type):
    """Fallback premium calculation"""
    base_premium = 0
    
    # Base premium by cover type
    if cover_type == "justMe":
        base_premium = 25000
    elif cover_type == "meAndFamily":
        base_premium = 50000 + (children_count * 10000)
    elif cover_type == "myChildOnly":
        base_premium = 15000 * children_count
    elif cover_type == "myParents":
        base_premium = 40000
    
    # Adjust for benefit package
    if benefit_package == "IP & OP":
        base_premium *= 1.5
    elif benefit_package == "IP,OP,Maternity":
        base_premium *= 2
    elif "dental & Optical" in benefit_package:
        base_premium *= 2.5
    
    # Adjust for cover limit
    if cover_limit == "500K":
        base_premium *= 0.8
    elif cover_limit == "2M":
        base_premium *= 1.2
    elif cover_limit == "5M":
        base_premium *= 1.5
    elif cover_limit == "above5M":
        base_premium *= 2
    
    # Adjust for hospital type
    if hospital_type == "budgetHospitals":
        base_premium *= 0.65
    
    return base_premium

def main():
    # Initialize session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'currency' not in st.session_state:
        st.session_state.currency = "KES"
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Header
    st.markdown('<div class="main-header">Medical Insurance Calculator</div>', unsafe_allow_html=True)
    
    # Currency toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="currency-toggle">', unsafe_allow_html=True)
        col_kes, col_usd = st.columns(2)
        with col_kes:
            kes_active = "active" if st.session_state.currency == "KES" else ""
            if st.button(f"KES {kes_active}", key="kes_btn", use_container_width=True):
                st.session_state.currency = "KES"
                st.rerun()
        with col_usd:
            usd_active = "active" if st.session_state.currency == "USD" else ""
            if st.button(f"USD {usd_active}", key="usd_btn", use_container_width=True):
                st.session_state.currency = "USD"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress bar
    steps = ["Cover Who", "Ages", "Benefits", "Health", "Cover Limit", "Hospital Type", "Start Date"]
    progress_width = (st.session_state.current_step - 1) / (len(steps) - 1) * 100
    
    st.markdown(f"""
    <div class="step-indicator">
        <div class="progress-background"></div>
        <div class="progress-bar" style="width: {progress_width}%"></div>
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(steps, 1):
        step_class = "active" if i == st.session_state.current_step else "completed" if i < st.session_state.current_step else ""
        st.markdown(f'<div class="step {step_class}">{i}. {step}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 1: Who do you want to cover?
    if st.session_state.current_step == 1:
        st.markdown('<div class="sub-header">Step 1: Who do you want to cover?</div>', unsafe_allow_html=True)
        
        cover_type = st.radio(
            "Select coverage type:",
            ["justMe", "meAndFamily", "myChildOnly", "myParents"],
            format_func=lambda x: {
                "justMe": "Just me",
                "meAndFamily": "Me and my family",
                "myChildOnly": "My child only", 
                "myParents": "My parents"
            }[x],
            key="cover_type"
        )
        
        if cover_type == "meAndFamily":
            st.info("Family means you + spouse + kids below 18. Or you and your kids.")
        
        col1, col2 = st.columns(2)
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 2
                st.session_state.form_data["cover_type"] = cover_type
                st.rerun()
    
    # Step 2: What are their ages?
    elif st.session_state.current_step == 2:
        st.markdown('<div class="sub-header">Step 2: What are their ages?</div>', unsafe_allow_html=True)
        
        cover_type = st.session_state.form_data.get("cover_type", "justMe")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if cover_type in ["justMe", "meAndFamily"]:
                myself_age = st.selectbox(
                    "Myself Age Group:",
                    ["18-30", "31-40", "41-50", "51-60"],
                    key="myself_age"
                )
                st.session_state.form_data["myself_age"] = myself_age
            
            if cover_type == "meAndFamily":
                spouse_age = st.selectbox(
                    "Spouse Age Group:",
                    ["18-30", "31-40", "41-50", "51-60"],
                    key="spouse_age"
                )
                st.session_state.form_data["spouse_age"] = spouse_age
            
            if cover_type == "myParents":
                parent1_age = st.selectbox(
                    "Parent 1 Age Group:",
                    ["51-60", "61-70", "71-plus"],
                    key="parent1_age"
                )
                st.session_state.form_data["parent1_age"] = parent1_age
        
        with col2:
            if cover_type in ["meAndFamily", "myChildOnly"]:
                children_count = st.selectbox(
                    "Number of Children:",
                    [0, 1, 2, 3, 4, 5],
                    key="children_count"
                )
                st.session_state.form_data["children_count"] = children_count
            
            if cover_type == "myParents":
                parent2_age = st.selectbox(
                    "Parent 2 Age Group:",
                    ["51-60", "61-70", "71-plus"],
                    key="parent2_age"
                )
                st.session_state.form_data["parent2_age"] = parent2_age
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 3
                st.rerun()
    
    # Step 3: Optional benefits
    elif st.session_state.current_step == 3:
        st.markdown('<div class="sub-header">Step 3: Optional Benefits</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            outpatient = st.checkbox("Outpatient", help="Doctor visits, labs, prescriptions")
            dental = st.checkbox("Dental", help="Checkups, fillings, extractions")
        
        with col2:
            optical = st.checkbox("Optical", help="Eye tests, glasses")
            maternity = st.checkbox("Maternity & newborn care", help="Prenatal care, delivery, and newborn care")
        
        inpatient_only = st.checkbox("Inpatient only (uncheck all above)")
        
        # Store in session state
        st.session_state.form_data.update({
            "outpatient": outpatient,
            "dental": dental,
            "optical": optical,
            "maternity": maternity,
            "inpatient_only": inpatient_only
        })
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 4
                st.rerun()
    
    # Step 4: Health conditions
    elif st.session_state.current_step == 4:
        st.markdown('<div class="sub-header">Step 4: Health Conditions</div>', unsafe_allow_html=True)
        
        st.write("Some covers handle pre-existing conditions differently. This affects waiting periods or what's paid out in case of an admission.")
        
        health_conditions = st.radio(
            "Do you or anyone you want covered have any of these conditions?",
            ["no", "yesOne", "yesMore"],
            format_func=lambda x: {
                "no": "No",
                "yesOne": "Yes, one person", 
                "yesMore": "Yes, more than one person"
            }[x],
            key="health_conditions"
        )
        
        st.session_state.form_data["health_conditions"] = health_conditions
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 3
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 5
                st.rerun()
    
    # Step 5: Cover limit
    elif st.session_state.current_step == 5:
        st.markdown('<div class="sub-header">Step 5: Annual Cover Limit</div>', unsafe_allow_html=True)
        
        cover_limit_options = {
            "500K": "500K - Entry-level (Accidents, emergencies)",
            "1M": "500K-1M - Standard (Most admissions)", 
            "2M": "1M-2M - Comprehensive (Surgeries, specialist care)",
            "5M": "2M-5M - Premium (Major or long-term cases)",
            "above5M": "5M+ - High-end (Full private hospital access)",
            "notSure": "Not sure - I'd like help choosing"
        }
        
        cover_limit = st.radio(
            "Select your annual cover limit:",
            list(cover_limit_options.keys()),
            format_func=lambda x: cover_limit_options[x],
            key="cover_limit"
        )
        
        st.session_state.form_data["cover_limit"] = cover_limit
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 4
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 6
                st.rerun()
    
    # Step 6: Hospital access type
    elif st.session_state.current_step == 6:
        st.markdown('<div class="sub-header">Step 6: Hospital Access Type</div>', unsafe_allow_html=True)
        
        hospital_type = st.radio(
            "Select hospital access type:",
            ["allHospitals", "budgetHospitals"],
            format_func=lambda x: {
                "allHospitals": "All hospitals (includes top private ones)",
                "budgetHospitals": "Budget hospitals (selected list of standard hospitals)"
            }[x],
            key="hospital_type"
        )
        
        if hospital_type == "budgetHospitals":
            st.warning("Note: If you choose 'Budget hospitals', your cover limit will be limited to 500K, 1M, or 1.5M.")
        
        st.session_state.form_data["hospital_type"] = hospital_type
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 5
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_step = 7
                st.rerun()
    
    # Step 7: Start date
    elif st.session_state.current_step == 7:
        st.markdown('<div class="sub-header">Step 7: Start Date</div>', unsafe_allow_html=True)
        
        start_date = st.radio(
            "When would you like cover to begin?",
            ["immediately", "1-3months", "exploring"],
            format_func=lambda x: {
                "immediately": "Immediately",
                "1-3months": "In 1-3 months", 
                "exploring": "Just exploring options"
            }[x],
            key="start_date"
        )
        
        st.session_state.form_data["start_date"] = start_date
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 6
                st.rerun()
        with col2:
            if st.button("Calculate Premium →", use_container_width=True, type="primary"):
                st.session_state.current_step = 8  # Results step
                st.rerun()
    
    # Results step
    elif st.session_state.current_step == 8:
        st.markdown('<div class="sub-header">Your Insurance Estimate</div>', unsafe_allow_html=True)
        
        # Calculate premium
        form_data = st.session_state.form_data
        
        # Determine benefit package
        benefit_package = "IP only"
        if form_data.get("inpatient_only"):
            benefit_package = "IP only"
        elif form_data.get("outpatient") and not form_data.get("dental") and not form_data.get("optical") and not form_data.get("maternity"):
            benefit_package = "IP & OP"
        elif form_data.get("outpatient") and form_data.get("maternity") and not form_data.get("dental") and not form_data.get("optical"):
            benefit_package = "IP,OP,Maternity"
        elif form_data.get("outpatient") and form_data.get("dental") and form_data.get("optical"):
            benefit_package = "IP,OP,Maternity,dental & Optical" if form_data.get("maternity") else "IP,OP,dental & Optical"
        
        # Get premium from rates
        annual_premium = get_premium_from_rates(
            form_data["cover_type"],
            form_data.get("myself_age"),
            form_data.get("spouse_age"),
            form_data.get("children_count", 0),
            form_data.get("parent1_age"),
            form_data.get("parent2_age"),
            benefit_package,
            form_data["cover_limit"],
            form_data["hospital_type"]
        )
        
        # Apply health condition loading
        health_conditions = form_data.get("health_conditions", "no")
        if health_conditions == "yesOne":
            annual_premium *= 1.1
        elif health_conditions == "yesMore":
            annual_premium *= 1.2
        
        # Currency conversion
        exchange_rate = 110  # 1 USD = 110 KES
        if st.session_state.currency == "USD":
            annual_premium = annual_premium / exchange_rate
        
        monthly_premium = annual_premium / 12
        
        # Display summary
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.write("**Coverage Summary:**")
        
        # Coverage for
        cover_type = form_data["cover_type"]
        if cover_type == "justMe":
            st.write(f"• **Coverage For:** Yourself")
        elif cover_type == "meAndFamily":
            st.write(f"• **Coverage For:** Yourself, spouse, and {form_data.get('children_count', 0)} child(ren)")
        elif cover_type == "myChildOnly":
            st.write(f"• **Coverage For:** {form_data.get('children_count', 0)} child(ren) only")
        elif cover_type == "myParents":
            st.write(f"• **Coverage For:** Your parents")
        
        # Ages
        ages_text = ""
        if form_data.get("myself_age"):
            ages_text += f"You: {form_data['myself_age']}"
        if form_data.get("spouse_age"):
            ages_text += f", Spouse: {form_data['spouse_age']}"
        if form_data.get("parent1_age"):
            ages_text += f", Parent 1: {form_data['parent1_age']}"
        if form_data.get("parent2_age"):
            ages_text += f", Parent 2: {form_data['parent2_age']}"
        if form_data.get("children_count", 0) > 0:
            ages_text += f", Children: {form_data['children_count']}"
        
        if ages_text:
            st.write(f"• **Ages:** {ages_text}")
        
        st.write(f"• **Benefits:** {benefit_package}")
        
        # Health conditions
        health_text = {
            "no": "No pre-existing conditions",
            "yesOne": "One person with pre-existing conditions", 
            "yesMore": "Multiple people with pre-existing conditions"
        }[health_conditions]
        st.write(f"• **Health Conditions:** {health_text}")
        
        # Cover limit
        limit_text = {
            "500K": "KES 500,000",
            "1M": "KES 1,000,000",
            "2M": "KES 2,000,000", 
            "5M": "KES 5,000,000",
            "above5M": "KES 5,000,000+",
            "notSure": "Not sure - need advice"
        }[form_data["cover_limit"]]
        st.write(f"• **Annual Cover Limit:** {limit_text}")
        
        # Hospital type
        hospital_text = "All hospitals" if form_data["hospital_type"] == "allHospitals" else "Budget hospitals"
        st.write(f"• **Hospital Access:** {hospital_text}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Price display
        st.markdown('<div class="price-display">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 2.5rem; font-weight: bold; color: #1f77b4;">{format_currency(annual_premium, st.session_state.currency)}</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: #666; margin-top: 0.5rem;">per year</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.8rem; font-weight: bold; color: #1f77b4; margin-top: 1rem;">{format_currency(monthly_premium, st.session_state.currency)}</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: #666;">per month</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("This is an estimate based on your choices. Actual premium may vary based on underwriting.")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Get Exact Quote", use_container_width=True)
        with col2:
            st.button("Talk to an Advisor", use_container_width=True, type="secondary")
        with col3:
            st.button("Compare Plans", use_container_width=True, type="secondary")
        
        if st.button("Start Over", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.form_data = {}
            st.rerun()

if __name__ == "__main__":
    main()