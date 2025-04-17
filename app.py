import streamlit as st
from auth import render_auth_page
from db_manager import init_db, is_valid_candidate_email

init_db()

# Role-specific login pages
def interviewer_login():
    st.title("👨‍💼 Interviewer Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")
    # Create account link
    st.markdown("---")
    if st.button("Not a user? Create an account"):
        st.query_params.update({"page": "interviewer_signup"})
        st.rerun()

def interviewer_signup():
    st.title("🆕 Interviewer Signup")
    st.text_input("Create Username")
    st.text_input("Email")
    st.text_input("Create Password", type="password")
    st.button("Create Account")

    if st.button("Back to Login"):
        st.query_params.update({"page": "interviewer"})
        st.rerun()

def candidate_login():
    st.title("🙋 Candidate Portal Access")
    email = st.text_input("Enter your company-registered email")

    if st.button("Access Portal"):
        if is_valid_candidate_email(email):
            st.success("✅ Access granted!")
            st.session_state["candidate_email"] = email
            st.query_params.update({"page": "candidate_portal"})
            st.rerun()
        else:
            st.error("❌ You are not authorized to access this portal.")

    

def hr_login():
    st.title("👩‍💼 HR Login")
    st.text_input("HR Email")
    st.text_input("Access Code")
    st.button("Login")

def render_role_cards():
    st.markdown("""
    <style>
    .card-container {
        display: flex;
        justify-content: center;
        align-items: stretch;
        gap: 20px;
        margin-top: 0px;
        flex-wrap: wrap;
    }
    .card {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 30px 20px;
        text-align: center;
        width: 250px;
        min-height: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        flex-grow: 1;
    }
    .card:hover {
        transform: scale(1.1);
        z-index: 1;
    }
    .card-container:hover .card:not(:hover) {
        transform: scale(0.95);
        opacity: 0.8;
    }
    .card-header {
        font-size: 22px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .card-content {
        font-size: 14px;
        color: #555;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.markdown("""
    <div class="card-container">
        <div class="card">
            <div class="card-header">Interviewer</div>
            <div class="card-content">Review candidate responses, evaluate skills, and participate in interviews.</div>
        </div>
        <div class="card">
            <div class="card-header">Human resource team</div>
            <div class="card-content">Manage the interview process, review resumes, reschedule interviews, schedule interviews.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("----")

    st.markdown("## Select your role!")
    
    role = st.selectbox("I'm an", ["Select Role", "Interviewer", "HR"])

    if st.button("Submit"):
        if role == "Interviewer":
            st.query_params.update({"page": "interviewer"})
            st.rerun()
        elif role == "HR":
            st.query_params.update({"page": "hr"})
            st.rerun()
        else:
            st.warning("Please select a role before submitting.")

# -----------------------------
# Main App Logic
# -----------------------------

page = st.query_params.get("page", "")

if page == "interviewer":
    render_auth_page("interviewer", mode="login")
elif page == "interviewer_signup":
    render_auth_page("interviewer", mode="signup")
elif page == "candidate_portal":
    candidate_email = st.session_state.get("candidate_email", None)
    if candidate_email:
        st.title("🎯 Candidate Dashboard")
        st.write(f"Welcome, {candidate_email}!")
        # Add candidate-specific content here
    else:
        st.warning("Access denied. Please go to the home page.")
elif page == "hr":
    render_auth_page("hr", mode="login")
elif page == "hr_signup":
    render_auth_page("hr", mode="signup")
else:
    render_role_cards()  




