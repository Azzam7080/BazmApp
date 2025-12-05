# ui/views.py
import flet as ft
import json
from logic.event_service import EventService
from logic.ai_service import AIService
from logic.report_service import ReportService
from logic.announcement_service import AnnouncementService

# --- ANNOUNCEMENTS TAB (Unchanged) ---
def AnnouncementsView(user_session):
    service = AnnouncementService()
    news_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    def load_news():
        news_list.controls.clear()
        data = service.get_announcements()
        if not data:
            news_list.controls.append(ft.Text("No announcements yet."))
        for item in data:
            # item: (id, title, content, date)
            news_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(item[1], weight="bold", size=16), # Title
                            ft.Text(item[3], size=12, italic=True),   # Date
                            ft.Divider(),
                            ft.Text(item[2])                          # Content
                        ]),
                        padding=15
                    )
                )
            )
        return news_list

    # Admin Controls
    admin_col = ft.Column()
    if user_session["role"] == "Admin":
        title_box = ft.TextField(label="Title")
        content_box = ft.TextField(label="Message", multiline=True)
        
        def post_news(e):
            if not title_box.value: return
            service.create_announcement(title_box.value, content_box.value)
            title_box.value = ""
            content_box.value = ""
            load_news() # Refresh list
            news_list.update()
            
        admin_col.controls = [
            ft.Text("Post New Announcement", weight="bold"),
            title_box,
            content_box,
            ft.ElevatedButton("Post", on_click=post_news),
            ft.Divider()
        ]

    return ft.Container(
        content=ft.Column([
            ft.Text("Community News", size=20, weight="bold"),
            admin_col,
            load_news()
        ]),
        padding=20, expand=True
    )
# --- EVENTS TAB (Unchanged) ---
def EventsView(user_session):
    event_service = EventService()
    events_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    def load_events():
        events_list.controls.clear()
        data = event_service.get_all_events()
        if not data: events_list.controls.append(ft.Text("No events found."))
        for event in data:
            event_id = event[0]
            is_registered = event_service.is_user_registered(event_id, user_session['email'])
            
            def on_register_click(e, e_id=event_id):
                success, msg = event_service.register_event(e_id, user_session['email'])
                if success:
                    e.control.text = "Registered"
                    e.control.disabled = True
                    e.control.icon = ft.Icons.CHECK
                    e.control.update()
                    e.page.snack_bar = ft.SnackBar(ft.Text(f"Registered for {event[1]}!"))
                    e.page.snack_bar.open = True
                    e.page.update()

            reg_btn = ft.ElevatedButton(
                "Registered" if is_registered else "Register",
                icon=ft.Icons.CHECK if is_registered else ft.Icons.ADD,
                disabled=is_registered,
                on_click=on_register_click
            )

            events_list.controls.append(
                ft.Card(content=ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.EVENT), title=ft.Text(event[1]), subtitle=ft.Text(f"{event[3]} @ {event[4]}")),
                    ft.Container(content=ft.Text(event[2]), padding=10),
                    ft.Row([reg_btn], alignment=ft.MainAxisAlignment.END)
                ]), padding=10))
            )
        return events_list

    admin_controls = []
    if user_session['role'] == "Admin":
        def add_dummy_event(e):
            event_service.create_event("New Event", "Description", "2025-12-01", "Lahore", "admin")
            events_list.controls = load_events().controls
            events_list.update()
        admin_controls.append(ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_dummy_event))

    return ft.Container(content=ft.Column([ft.Text("Upcoming Events", size=20, weight="bold"), load_events(), *admin_controls]), padding=20, expand=True)

# --- CHATBOT TAB (Unchanged) ---
def ChatbotView(user_session):
    ai = AIService()
    chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    user_query = ft.TextField(hint_text="Ask about events...", expand=True)
    
    def send_message(e):
        if not user_query.value: return
        chat_history.controls.append(ft.Row([ft.Container(content=ft.Text(f"You: {user_query.value}", color="white"), bgcolor=ft.Colors.BLUE_GREY_800, padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.END))
        q = user_query.value
        user_query.value = ""
        e.page.update()
        response = ai.get_response(q)
        chat_history.controls.append(ft.Row([ft.Container(content=ft.Text(f"Bazm AI: {response}", color="black"), bgcolor=ft.Colors.GREEN_100, padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.START))
        e.page.update()

    return ft.Container(content=ft.Column([chat_history, ft.Row([user_query, ft.IconButton(icon=ft.Icons.SEND, on_click=send_message)])]), padding=20, expand=True)

# --- REPORTS TAB (THE NEW MEGA FORM) ---
# ui/views.py (Replace ONLY ReportsView)
def ReportsView(user_session):
    report_service = ReportService()
    
    if user_session["role"] != "Admin":
        return ft.Container(content=ft.Text("Admins Only"), alignment=ft.alignment.center)

    # 1. HELPER: Create a row of 3 number inputs
    def create_stat_row(label):
        return ft.Row([
            ft.Text(label, width=80, weight="bold"),
            ft.TextField(label="New", width=60, keyboard_type=ft.KeyboardType.NUMBER, value="0", text_size=12),
            ft.TextField(label="Rem", width=60, keyboard_type=ft.KeyboardType.NUMBER, value="0", text_size=12),
            ft.TextField(label="Total", width=60, keyboard_type=ft.KeyboardType.NUMBER, value="0", text_size=12),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # 2. HELPER: Extract data
    def get_stat_data(row_control):
        return {
            "new": row_control.controls[1].value,
            "removed": row_control.controls[2].value,
            "total": row_control.controls[3].value
        }

    # --- UI COMPONENTS ---
    month_dd = ft.Dropdown(label="Month", options=[ft.dropdown.Option(m) for m in ["Jan", "Feb", "Mar", "Dec"]], width=150)
    year_dd = ft.Dropdown(label="Year", options=[ft.dropdown.Option("2025"), ft.dropdown.Option("2026")], width=150)
    
    stat_members = create_stat_row("Members")
    stat_shaheen = create_stat_row("Shaheen")
    stat_rufaqa = create_stat_row("Rufaqa")
    stat_arkaan = create_stat_row("Arkaan")
    
    stat_baqaida = create_stat_row("Baqaida")
    stat_zaili = create_stat_row("Zaili")
    stat_raabta = create_stat_row("Raabta")

    prog_home = ft.TextField(label="Home Meetups (Qty)", keyboard_type=ft.KeyboardType.NUMBER, value="0")
    prog_school = ft.TextField(label="School Programs (Qty)", keyboard_type=ft.KeyboardType.NUMBER, value="0")

    other_rows = ft.Column()
    def add_other_row(e):
        other_rows.controls.append(
            ft.Row([
                ft.Text(f"{len(other_rows.controls)+1}."),
                ft.TextField(hint_text="Program Name", expand=2),
                ft.TextField(hint_text="Audience", expand=1),
            ])
        )
        e.page.update()
    
    tabsra_box = ft.TextField(label="Tabsra (Comments)", multiline=True, min_lines=3)

    # --- SUBMIT LOGIC ---
    def submit_report(e):
        if not month_dd.value or not year_dd.value:
            e.page.snack_bar = ft.SnackBar(ft.Text("Please select Month and Year"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        other_data = []
        for row in other_rows.controls:
            other_data.append({
                "name": row.controls[1].value,
                "audience": row.controls[2].value
            })

        full_data = {
            "afraadsazi": {
                "members": get_stat_data(stat_members),
                "shaheen": get_stat_data(stat_shaheen),
                "rufaqa": get_stat_data(stat_rufaqa),
                "arkaan": get_stat_data(stat_arkaan),
            },
            "units": {
                "baqaida": get_stat_data(stat_baqaida),
                "zaili": get_stat_data(stat_zaili),
                "raabta": get_stat_data(stat_raabta),
            },
            "programs": {
                "home": prog_home.value,
                "school": prog_school.value
            },
            "other": other_data,
            "tabsra": tabsra_box.value
        }

        success, msg = report_service.create_report(month_dd.value, year_dd.value, full_data, user_session['email'])
        e.page.snack_bar = ft.SnackBar(ft.Text(msg))
        e.page.snack_bar.open = True
        
        if success:
            show_report_list()
        e.page.update()

    # --- VIEWS SWITCHING ---
    main_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def show_create_form(e):
        main_content.controls = [
            ft.Text("New Report", size=20, weight="bold"),
            ft.Row([month_dd, year_dd]),
            ft.Divider(),
            ft.Text("Section: Afraadsazi", weight="bold", color=ft.Colors.GREEN),
            stat_members, stat_shaheen, stat_rufaqa, stat_arkaan,
            ft.Divider(),
            ft.Text("Section: School Units", weight="bold", color=ft.Colors.GREEN),
            stat_baqaida, stat_zaili, stat_raabta,
            ft.Divider(),
            ft.Text("Section: Programs", weight="bold", color=ft.Colors.GREEN),
            prog_home, prog_school,
            ft.Divider(),
            ft.Row([ft.Text("Section: Other", weight="bold", color=ft.Colors.GREEN), ft.IconButton(ft.Icons.ADD, on_click=add_other_row)]),
            other_rows,
            ft.Divider(),
            tabsra_box,
            ft.ElevatedButton("Submit Report", on_click=submit_report, width=300)
        ]
        main_content.update() # <--- CHANGED FROM e.page.update()

    def show_report_details(report):
        data = json.loads(report[3])
        
        main_content.controls = [
            ft.Text(f"Report: {report[1]} {report[2]}", size=20, weight="bold"),
            ft.Text(f"Author: {report[4]}", size=12, italic=True),
            ft.Divider(),
            ft.Text(f"Tabsra: {data.get('tabsra', '')}"),
            ft.Divider(),
            ft.Text("JSON Data (Raw View):"),
            ft.Text(json.dumps(data, indent=2), font_family="monospace"),
            ft.ElevatedButton("Back", on_click=lambda e: show_report_list())
        ]
        main_content.update() # <--- FIXED: Changed e.page.update() to main_content.update()

    def show_report_list():
        reports = report_service.get_all_reports()
        
        report_rows = []
        for r in reports:
            def view_click(e, rep=r):
                show_report_details(rep)
                
            report_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(r[1])),
                        ft.DataCell(ft.Text(r[2])),
                        ft.DataCell(ft.Text(r[4])),
                    ],
                    on_select_changed=view_click
                )
            )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Month")),
                ft.DataColumn(ft.Text("Year")),
                ft.DataColumn(ft.Text("Author")),
            ],
            rows=report_rows
        )

        main_content.controls = [
            ft.Row([ft.Text("Reports", size=20, weight="bold"), ft.IconButton(ft.Icons.ADD, on_click=show_create_form)]),
            data_table
        ]
        if main_content.page: main_content.update()

    show_report_list()
    return ft.Container(content=main_content, padding=20, expand=True)