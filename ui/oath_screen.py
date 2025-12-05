# ui/oath_screen.py
import flet as ft
from logic.auth_service import AuthService

def OathScreen(page: ft.Page, user_session, on_oath_accepted):
    auth = AuthService()
    user_name = user_session['name']

    # The Oath Text (Translated)
    oath_text = f"""
    I, '{user_name}', upon becoming a member of Bazm-e-Paigham, pledge that:

    1. I will offer my prayers (Salah) regularly.
    2. I will obey my parents and teachers.
    3. I will remain loyal to Pakistan and Islam.
    4. I will acquire knowledge with heart and dedication.
    5. I will become righteous and spread righteousness.
    """

    checkbox = ft.Checkbox(label="This oath is between me and Allah, and I will uphold it.", value=False)

    def submit_oath(e):
        if not checkbox.value:
            e.page.snack_bar = ft.SnackBar(ft.Text("Please check the box to agree."))
            e.page.snack_bar.open = True
            e.page.update()
            return
        
        # Save to DB
        auth.accept_oath(user_session['email'])
        
        # Move to Dashboard
        on_oath_accepted(user_session)

    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.SECURITY, size=60, color=ft.Colors.GREEN),
            ft.Text("Membership Oath", size=24, weight="bold"),
            ft.Container(
                content=ft.Text(oath_text, size=16, text_align=ft.TextAlign.LEFT),
                padding=20,
                bgcolor=ft.Colors.GREEN_50,
                border_radius=10
            ),
            ft.Container(height=20),
            checkbox,
            ft.ElevatedButton("I Pledge", on_click=submit_oath, width=200)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        padding=20,
        expand=True
    )