# ui/login_screen.py
import flet as ft
from logic.auth_service import AuthService

def LoginScreen(page: ft.Page, on_login_success):
    auth = AuthService()

    email_input = ft.TextField(label="Email", width=300)
    pass_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    name_input = ft.TextField(label="Full Name", width=300, visible=False)
    
    role_input = ft.Dropdown(
        label="Select Role",
        width=300,
        options=[
            ft.dropdown.Option("Member"),
            ft.dropdown.Option("Admin"),
        ],
        value="Member",
        visible=False
    )
    
    is_register_mode = False

    def toggle_mode(e):
        nonlocal is_register_mode
        is_register_mode = not is_register_mode
        name_input.visible = is_register_mode
        role_input.visible = is_register_mode
        action_btn.text = "Register" if is_register_mode else "Login"
        toggle_btn.text = "Already have an account? Login" if is_register_mode else "New here? Register"
        page.update()

    def handle_click(e):
        if is_register_mode:
            # REGISTER - FIXED: Removed the empty string argument
            success, msg = auth.register_user(
                name_input.value, 
                email_input.value, 
                pass_input.value, 
                role_input.value
            )
            
            page.snack_bar = ft.SnackBar(ft.Text(str(msg)))
            page.snack_bar.open = True
            if success:
                toggle_mode(None)
        else:
            # LOGIN
            user = auth.login_user(email_input.value, pass_input.value)
            if user:
                on_login_success(user)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid Credentials"))
                page.snack_bar.open = True
        page.update()

    action_btn = ft.ElevatedButton("Login", on_click=handle_click, width=300)
    toggle_btn = ft.TextButton("New here? Register", on_click=toggle_mode)

    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.MOSQUE, size=50, color=ft.Colors.GREEN),
                ft.Text("Bazm-e-Paigham", size=30, weight="bold"),
                name_input,
                role_input,
                email_input,
                pass_input,
                action_btn,
                toggle_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True
    )