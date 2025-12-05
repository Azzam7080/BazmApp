# logic/event_service.py
from data.database import execute_query, fetch_all, fetch_one

class EventService:
    def create_event(self, title, description, date, location, creator_email):
        try:
            execute_query(
                "INSERT INTO events (title, description, datetime, location, created_by) VALUES (?, ?, ?, ?, ?)",
                (title, description, date, location, creator_email)
            )
            return True, "Event created."
        except Exception as e:
            return False, str(e)

    def get_all_events(self):
        return fetch_all("SELECT * FROM events ORDER BY datetime")

    # --- NEW FUNCTIONS ---
    def register_event(self, event_id, user_email):
        try:
            execute_query(
                "INSERT INTO registrations (event_id, user_email) VALUES (?, ?)",
                (event_id, user_email)
            )
            return True, "Successfully registered!"
        except Exception:
            return False, "Already registered."

    def is_user_registered(self, event_id, user_email):
        # Returns True if the user is already in the registrations table
        result = fetch_one(
            "SELECT id FROM registrations WHERE event_id=? AND user_email=?",
            (event_id, user_email)
        )
        return result is not None