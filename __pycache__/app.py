from flask import Flask, render_template, request, redirect, url_for, flash
import re
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Simple in-memory "database"
users_db = {}

def check_password_strength(password):
    issues = []
    
    # Check password length
    if len(password) < 8:
        issues.append("Password must be at least 8 characters long.")
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        issues.append("Include at least one uppercase letter.")
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        issues.append("Include at least one lowercase letter.")
    
    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        issues.append("Include at least one number.")
    
    # Check for at least one special character
    if not re.search(r'[^a-zA-Z0-9]', password):
        issues.append("Include at least one special character.")
    
    # Check for common passwords
    common_passwords = ["password", "123456", "qwerty", "letmein", "admin"]
    if password.lower() in common_passwords:
        issues.append("Avoid using common passwords.")
    
    if issues:
        return "Weak: " + " ".join(issues)
    
    # If all conditions are met
    return "Strong: Your password is secure!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check password strength
        password_strength = check_password_strength(password)
        
        # Flash message if password is weak
        if "Weak" in password_strength:
            flash(password_strength, "danger")
            return redirect(url_for('signup'))
        
        # Hash password and store it in "database"
        users_db[username] = hash_password(password)
        flash("Account created successfully!", "success")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
