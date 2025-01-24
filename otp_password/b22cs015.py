import random
import string
import pyperclip
from random import choice
import pyotp
import smtplib

# Function to check the complexity of the password
def check_complexity(password):
    # Determine the length of the password
    length = len(password)

    # Check if the password contains uppercase letters, lowercase letters, digits, and special characters
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    complexity = 0
    # Add complexity points based on password characteristics
    if length >= 8:
        complexity += 1
    if has_upper:
        complexity += 1
    if has_lower:
        complexity += 1
    if has_digit:
        complexity += 1
    if has_special:
        complexity += 1

    # Determine the message based on the complexity score
    if complexity == 5:
        message="Strong"
    elif complexity == 4:
        message= "Moderate"
    else:
        message="Weak"

    return message


# Function to generate a One-Time Password (OTP) using pyotp
def generate_otp():
    # Generate a random base32 secret key for OTP
    secret_key = pyotp.random_base32()

    # Create a TOTP (Time-based One-Time Password) object with the generated key
    otp = pyotp.TOTP(secret_key)
    otp_code = otp.now()

    # Generate the OTP using the current time
    return otp_code


# Function to send the OTP to the user's email address
def send_otp_to_email(email, otp):
    # Establish a connection to the SMTP server using SSL
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Log into the Gmail SMTP server with your email credentials
    server.login("b22cs015@iitj.ac.in", "ayqy yxxb iipx tjlg")  # Use your email and app-specific password here

    # Send the OTP to the user's email address
    server.sendmail("b22cs015@iitj.ac.in", email, f"""Subject: OTP VERIFICATION
    Hi, your OTP for lab testing is {otp}""")

    # Close the connection to the SMTP server
    server.quit()

# Function to verify if the OTP entered by the user matches the actual OTP
def verify_otp(user_otp,actual_otp):
    if user_otp == actual_otp:
        return "OTP Verification Successful"
    else:
        return "OTP Verification Failed"


def main():

    password=input("Enter the password: ")

    # Check the complexity of the entered password
    password_strength=check_complexity(password)
    
    # If the password is strong, proceed to OTP verification
    if password_strength == "Strong":
        email = input("Enter your email address for OTP verification: ")
        otp = generate_otp()

        send_otp_to_email(email, otp)

        entered_otp = input("Enter the OTP sent to your email: ")
        result = verify_otp(entered_otp, otp)
        print(result)
    else:
        print("Password does not meet the complexity requirements. Try again.")

if __name__ == "__main__":
    main()
