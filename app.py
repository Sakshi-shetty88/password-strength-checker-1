from flask import Flask, request, render_template

app = Flask(__name__)

import re  # Importing regular expressions module

# Function to check password strength
def check_password_strength(password):
    if len(password) < 8:
        return "Weak: Password must be at least 8 characters long."
    common_passwords = [
        "password", "123456", "qwerty", "letmein", "admin", "welcome", "monkey", "12345", 
        "123123", "sunshine", "iloveyou", "1234", "password1", "123qwe", "abc123", "football"
    ]
    if password.lower() in common_passwords:
        return "Weak: Avoid using common passwords."
    if not re.search(r'[A-Z]', password):
        return "Weak: Include at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Weak: Include at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return "Weak: Include at least one number."
    if not re.search(r'[^a-zA-Z0-9]', password):
        return "Weak: Include at least one special character."
    return "Strong: Your password is secure!"

# Flask route to handle form submission
@app.route("/", methods=["GET", "POST"])
def password_checker():
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            return render_template("index.html", message="Error: Please enter a password.")
        feedback = check_password_strength(password)
        return render_template("index.html", message=feedback)
    return render_template("index.html", message="")

if __name__ == "__main__":
    app.run(debug=True)
