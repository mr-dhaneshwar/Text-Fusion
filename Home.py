import streamlit as st
from mail import send_verification_email  # Ensure send_verification_email is defined and configured

# Page configuration
st.title("Text and Image Fusion")
st.header("Interact with PDF or Image Content")

# Function to handle email and OTP verification
def sent_mail():
    if st.session_state.get("logged_in"):
        # Clear all widgets and display the success message
        st.empty()  # Remove all widgets
        # Show only success message
        st.page_link("pages/1_Text_Fusion.py", label="Text Fusion", icon="1️⃣")
        st.page_link("pages/2_Image_Fusion.py", label="Image Fusion", icon="2️⃣")
    else:
        # Placeholder for dynamic updates
        container = st.container()

        # Email input and send button
        with container:
            email_address = st.text_input("Enter your email address")
            if st.button("Send Email"):
                if email_address:
                    otp = send_verification_email(email_address)
                    if otp:
                        st.session_state["otp"] = otp
                        st.session_state["email_sent"] = True
                        st.success("Email sent successfully. Please check your inbox for the OTP.")
                    else:
                        st.error("Something went wrong. Please try again.")
                else:
                    st.warning("Please enter a valid email address")

        # OTP input and verify button
        if st.session_state.get("email_sent"):
            with container:
                user_otp = st.text_input("Enter OTP", type="password")
                # if st.button("Submit"):
                if st.button("Submit"):
                    if "otp" in st.session_state and str(st.session_state["otp"]) == str(user_otp.strip()):
                        
                        st.session_state["logged_in"] = True  # Mark the user as logged in
                        st.success("Login Successful!")
                        st.button("Go to Home..")
                        # Use query parameters to refresh the app
                        # st.set_query_params(logged_in="true")
                    else:
                        st.error("Incorrect OTP. Please try again.")

# Logout function to reset session state
def logout():
    st.session_state.clear()
    st.set_query_params(logged_in="false")

# Main function
def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check query parameters to update session state
    # query_params = st.query_params
    # if query_params.get("logged_in") == ["true"]:
    #     st.session_state["logged_in"] = True
    # elif query_params.get("logged_in") == ["false"]:
    #     st.session_state["logged_in"] = False
    st.session_state["logged_in"] = True

    sent_mail()

if __name__ == "__main__":
    main()
