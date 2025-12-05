# logic/announcement_service.py
from data.database import execute_query, fetch_all

class AnnouncementService:
    def create_announcement(self, title, content):
        try:
            execute_query(
                "INSERT INTO announcements (title, content, created_at) VALUES (?, ?, datetime('now'))",
                (title, content)
            )
            return True, "Announcement posted."
        except Exception as e:
            return False, str(e)

    def get_announcements(self):
        # Newest first
        return fetch_all("SELECT * FROM announcements ORDER BY created_at DESC")