# logic/auth_service.py
import hashlib
from data.database import execute_query, fetch_one

class AuthService:
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # REMOVED student_id argument
    def register_user(self, name, email, password, role="Member"):
        if fetch_one("SELECT email FROM users WHERE email=?", (email,)):
            return False, "Email already exists."
        
        hashed_pw = self.hash_password(password)
        try:
            # FIXED: Removed 'student_id' from this query
            execute_query(
                "INSERT INTO users (name, email, password_hash, role, has_oath) VALUES (?, ?, ?, ?, 0)",
                (name, email, hashed_pw, role)
            )
            return True, "Registration successful."
        except Exception as e:
            return False, f"Registration Error: {str(e)}"

    def login_user(self, email, password):
        hashed_pw = self.hash_password(password)
        user = fetch_one("SELECT name, role, has_oath FROM users WHERE email=? AND password_hash=?", (email, hashed_pw))
        
        if user:
            return {
                "name": user[0], 
                "role": user[1], 
                "email": email, 
                "has_oath": user[2]
            }
        else:
            return None

    def accept_oath(self, email):
        try:
            execute_query("UPDATE users SET has_oath=1 WHERE email=?", (email,))
            return True
        except:
            return False