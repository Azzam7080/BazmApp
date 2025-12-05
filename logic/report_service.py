# logic/report_service.py
import json
from data.database import execute_query, fetch_all

class ReportService:
    def create_report(self, month, year, data_dict, author_email):
        try:
            # Convert the complex python dictionary to a text string (JSON)
            json_data = json.dumps(data_dict)
            
            execute_query(
                "INSERT INTO reports (month, year, structured_data, author_email, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
                (month, year, json_data, author_email)
            )
            return True, "Report saved successfully."
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_all_reports(self):
        return fetch_all("SELECT * FROM reports ORDER BY created_at DESC")