import streamlit as st
import re
from db_manager import create_user, verify_user, user_exists

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email)

def render_auth_page(role: str, mode: str = "login"):
    st.markdown(f"""
        <style>
        .auth-title {{
            text-align: center;
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)


    st.markdown(f"<div class='auth-title'>{'🆕 Signup' if mode == 'signup' else '🔐 Login'} - {role.capitalize()}</div>", unsafe_allow_html=True)

    email = st.text_input("📧 Email")
    
    if role == "interviewer":
        credential = st.text_input("🔒 Password", type="password")
    elif role == "candidate":
        credential = st.text_input("🆔 Candidate ID", type="password")
    elif role == "hr":
        credential = st.text_input("🔑 Access Code", type="password")

    submit_btn_label = "Create Account ✅" if mode == "signup" else "Login 🔓"
    if st.button(submit_btn_label, type="primary"):
        # === Validations ===
        if not email or not credential:
            st.error("⚠️ All fields are required.")
        elif not is_valid_email(email):
            st.error("📧 Email must be in the format: abc@gmail.com")
        elif len(credential) < 8:
            st.error("🔒 Password / ID must be at least 8 characters long.")
        else:
            if mode == "signup":
                if user_exists(role, email):
                    st.error(f"❗ {role.capitalize()} already exists. Try logging in instead.")
                else:
                    success = create_user(role, email, credential)
                    if success:
                        st.success(f"🎉 {role.capitalize()} account created successfully!")
                        st.rerun()
                    else:
                        st.error("⚠️ Account creation failed. Try again.")
            elif mode == "login":
                if verify_user(role, email, credential):
                    st.success(f"✅ {role.capitalize()} login successful!")
                    st.info(f"Redirecting to {role.capitalize()} dashboard...")
                else:
                    st.error("🚫 Invalid credentials. Please check and try again.")

    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if mode == "login":
            if st.button(f"👉 Create a {role} account"):
                st.query_params.update({"page": f"{role}_signup"})
                st.rerun()
    with col2:
        if mode == "signup":
            if st.button("🔙 Back to Login"):
                st.query_params.update({"page": f"{role}"})
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
