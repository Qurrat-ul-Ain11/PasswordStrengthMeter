import streamlit as st
import re
import zxcvbn  # Password strength estimation library

def check_password_strength(password):
    # Check password using zxcvbn
    results = zxcvbn.zxcvbn(password)
    score = results['score']
    feedback = results['feedback']['suggestions']
    
    # Additional checks
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # Strength assessment
    strength = "Very Weak"
    if score == 0:
        strength = "Very Weak"
    elif score == 1:
        strength = "Weak"
    elif score == 2:
        strength = "Moderate"
    elif score == 3:
        strength = "Strong"
    elif score == 4:
        strength = "Very Strong"
    
    return {
        'strength': strength,
        'score': score,
        'feedback': feedback,
        'length': length,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_special': has_special
    }

def main():
    st.title("🔒 Password Strength Meter")
    st.write("Check how strong your password is and get improvement suggestions.")
    
    password = st.text_input("Enter your password:", type="password")
    
    if password:
        with st.spinner("Analyzing password..."):
            result = check_password_strength(password)
        
        # Display strength meter
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Strength", result['strength'])
        with col2:
            st.progress((result['score'] + 1) * 20)
        
        # Display detailed feedback
        st.subheader("Password Analysis:")
        
        cols = st.columns(4)
        cols[0].metric("Length", result['length'], 
                      "Good" if result['length'] >= 8 else "Too short",
                      delta_color="normal")
        cols[1].metric("Uppercase", "✔" if result['has_upper'] else "✖", 
                      help="Should contain at least one uppercase letter")
        cols[2].metric("Lowercase", "✔" if result['has_lower'] else "✖",
                      help="Should contain at least one lowercase letter")
        cols[3].metric("Special Char", "✔" if result['has_special'] else "✖",
                      help="Should contain at least one special character")
        
        if result['feedback']:
            st.subheader("Suggestions:")
            for suggestion in result['feedback']:
                st.write(f"- {suggestion}")
        
        # Additional warnings
        if result['length'] < 8:
            st.warning("Your password is too short. Use at least 8 characters.")
        if not result['has_upper']:
            st.warning("Add uppercase letters to strengthen your password.")
        if not result['has_special']:
            st.warning("Add special characters to strengthen your password.")
        
        # Time to crack estimation
        crack_time = zxcvbn.zxcvbn(password)['crack_times_display']['online_no_throttling_10_per_second']
        st.info(f"Estimated time to crack: {crack_time}")

if __name__ == "__main__":
    main()