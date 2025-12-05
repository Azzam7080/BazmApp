# logic/ai_service.py
from google import genai
from data.database import fetch_all

# ==========================================
# PASTE YOUR API KEY HERE
API_KEY = "Insert API key here"
# ==========================================

class AIService:
    def __init__(self):
        self.client = None
        self.active = False
        
        # Check if key is present
        if API_KEY and "Insert" not in API_KEY:
            try:
                # NEW SDK INITIALIZATION
                self.client = genai.Client(api_key=API_KEY)
                self.active = True
                print("DEBUG: AI Client initialized (New SDK).")
            except Exception as e:
                print(f"DEBUG: AI Init Error: {e}")
        else:
            print("DEBUG: AI Key missing.")

    def _get_context_from_db(self):
        """Fetches real data to make the AI smart"""
        try:
            # 1. Get Events
            events = fetch_all("SELECT title, datetime, location FROM events")
            events_text = "Upcoming Events:\n"
            if events:
                for e in events:
                    events_text += f"- {e[0]} on {e[1]} at {e[2]}\n"
            else:
                events_text += "No upcoming events scheduled.\n"
            
            # 2. Get Announcements
            news = fetch_all("SELECT title, content FROM announcements ORDER BY created_at DESC LIMIT 3")
            news_text = "Latest News:\n"
            if news:
                for n in news:
                    news_text += f"- {n[0]}: {n[1]}\n"
            else:
                news_text += "No recent announcements.\n"

            return events_text + "\n" + news_text
        except Exception as e:
            print(f"DEBUG: Database Context Error: {e}")
            return "Context unavailable."

    def get_response(self, user_query):
        if not self.active:
            return "AI Service is offline. Check terminal for details."

        # 1. Get Context
        db_context = self._get_context_from_db()
        
        # 2. Construct Prompt
        full_prompt = f"""
        SYSTEM INSTRUCTION:
        You are 'Bazm AI', a helpful assistant for the Bazm-e-Paigham community.
        Use this DATABASE CONTEXT to answer questions:
        {db_context}
        
        USER QUERY:
        {user_query}
        """

        try:
            # 3. Generate Content (New SDK Syntax)
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            print(f"DEBUG: Generation Error: {e}")
            return "I am having trouble connecting to Google right now."