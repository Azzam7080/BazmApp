# main.py
import flet as ft
from ui.login_screen import LoginScreen
from ui.oath_screen import OathScreen  # <--- NEW IMPORT
from ui.views import EventsView, ChatbotView, ReportsView, AnnouncementsView

def main(page: ft.Page):
    page.title = "Bazm-e-Paigham"
    page.window_width = 380
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    current_user = None

    def logout(e):
        page.clean()
        page.add(LoginScreen(page, on_login_success))

    def show_dashboard(user):
        """Builds the main tabs"""
        page.clean()
        
        # Define Tabs
        my_tabs = [
            # NEW: Announcements is usually the first thing users should see
            ft.Tab(text="Announcements", icon=ft.Icons.ANNOUNCEMENT, content=AnnouncementsView(user)),
            ft.Tab(text="Events", icon=ft.Icons.EVENT, content=EventsView(user)),
            ft.Tab(text="AI Chat", icon=ft.Icons.CHAT, content=ChatbotView(user)),
        ]
        
        # Only add Reports tab if Admin
        if user["role"] == "Admin":
            my_tabs.append(
                ft.Tab(text="Reports", icon=ft.Icons.ASSESSMENT, content=ReportsView(user))
            )

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=my_tabs,
            expand=1,
        )

        page.add(
            ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"Welcome, {user['name']}", color="white", size=16, weight="bold"),
                        ft.IconButton(ft.Icons.LOGOUT, icon_color="white", on_click=logout)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.GREEN,
                    padding=10
                ),
                t
            ], expand=True)
        )

    def on_login_success(user):
        nonlocal current_user
        current_user = user
        
        # TRAFFIC CONTROL: Check Oath Status
        if user['has_oath'] == 1:
            show_dashboard(user)
        else:
            # Show Oath Screen first
            page.clean()
            page.add(OathScreen(page, user, on_oath_accepted=show_dashboard))

    page.add(LoginScreen(page, on_login_success))

if __name__ == "__main__":
    ft.app(target=main)