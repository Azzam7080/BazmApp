# test_logic.py
from logic.auth_service import AuthService
from logic.event_service import EventService

auth = AuthService()
event = EventService()

# 1. Test Registration
success, msg = auth.register_user("Abdullah", "BSCS-22143", "abdullah@test.com", "password123", "Admin")
print(f"Registration: {msg}")

# 2. Test Login
user = auth.login_user("abdullah@test.com", "password123")
if user:
    print(f"Login Success: Welcome {user['name']} ({user['role']})")
    
    # 3. Test Event Creation (Only if logged in)
    success, msg = event.create_event("Bazm Meetup", "General Body Meeting", "2025-12-05", "Auditorium", user['email'])
    print(f"Event Creation: {msg}")
    
    # 4. List Events
    events = event.get_all_events()
    print("Current Events:", events)
else:
    print("Login Failed")