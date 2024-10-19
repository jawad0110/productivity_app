import flet as ft
from flet_core import UserControl
from rich.table import Column
from pages.task_management import TaskManagementPage
from pages.pomodoro_timer import PomodoroTimerPage
from pages.quick_reminders import QuickRemindersPage
from pages.habit_tracking import HabitTrackingPage

def on_column_scroll(e: ft.OnScrollEvent):
    pass

def HomePage(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = 'center'
    page.window.maximized = True
    page.window.resizable = False

    # Register custom fonts
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf"
    }

    # Add a Header Text
    header_text = ft.Text(
        value="Be Productive",
        size=35,
        color="Black",
        font_family="Nohemi Black",
        text_align=ft.TextAlign.CENTER  # Center the header text
    )

    # Task Management Page
    def route_change(route):
        # Button Text style
        buttons_text_style = ft.TextStyle(
            font_family="Nohemi Bold",
            size=20
        )

        # The buttons style
        button_style = ft.ButtonStyle(
            text_style=buttons_text_style,
            bgcolor="#D9D9D9",
            shape=ft.RoundedRectangleBorder(radius=16)
        )

        # What does the page appear:
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    scroll=ft.ScrollMode.ALWAYS,
                    on_scroll=on_column_scroll,
                    route="/",
                    controls=[
                        # Use a Stack container to layer elements
                        ft.Stack(
                            controls=[
                                # Main Column container
                                ft.Column(
                                    controls=[
                                        # Header container
                                        ft.Container(
                                            content=header_text,
                                            margin=10,
                                            padding=10,
                                            bgcolor='#ffffff',
                                            width=325,
                                            height=80,
                                            border_radius=10,
                                            alignment=ft.alignment.center  # Center the header text within the container
                                        ),
                                        # Empty space
                                        ft.Container(height=20),
                                        # Buttons Container
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    # Task Management Button
                                                    ft.ElevatedButton(
                                                        "Task Management",
                                                        on_click=lambda _: page.go("/task_management"),
                                                        width=250, height=50,
                                                        color="Black",
                                                        style=button_style
                                                    ),
                                                    # Empty space
                                                    ft.Container(height=10),
                                                    # Time Tracking Button
                                                    ft.ElevatedButton(
                                                        "Pomodoro Timer",
                                                        on_click=lambda _: page.go("/pomodoro_timer"),
                                                        width=250, height=50,
                                                        color="Black",
                                                        style=button_style
                                                    ),
                                                    # Empty space
                                                    ft.Container(height=10),
                                                    # Quick Reminders Button
                                                    ft.ElevatedButton(
                                                        "Quick Reminders",
                                                        on_click=lambda _: page.go("/quick_reminders"),
                                                        width=250, height=50,
                                                        color="Black",
                                                        style=button_style
                                                    ),
                                                    # Empty space
                                                    ft.Container(height=10),
                                                    # Habit Tracking Button
                                                    ft.ElevatedButton(
                                                        "Habit Tracking",
                                                        on_click=lambda _: page.go("/habit_traking"),
                                                        width=250, height=50,
                                                        color="Black",
                                                        style=button_style
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,  # Center the buttons vertically
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Center the buttons horizontally
                                            ),
                                            alignment=ft.alignment.center  # Center the container itself
                                        ),
                                        # Empty space
                                        ft.Container(height=20),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Center the Column vertically
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center the Column horizontally
                                    spacing=20  # Add spacing between elements
                                )
                            ]
                        )
                    ]
                )
            )
        # If the task management button pressed, go to the task management page
        elif page.route == "/task_management":
            page.views.append(TaskManagementPage(page))
        # If the Pomodoro Timer button pressed, go to the Pomodoro Timer page
        elif page.route == "/pomodoro_timer":
            page.views.append(PomodoroTimerPage(page))
        # If the Quick Reminders button pressed, go to the Quick Reminders page
        elif page.route == "/quick_reminders":
            page.views.append(QuickRemindersPage(page))
        # If the Habit Tracking button pressed, go to the Habit Tracking page
        elif page.route == "/habit_traking":
            page.views.append(HabitTrackingPage(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# Run the application as a web server
