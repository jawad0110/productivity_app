import datetime
import flet as ft
import pyrebase
import os
import pages.home as home  # import your home module
from http import cookies



# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDqhNZPYlPeGDV12yPQXbTEbvT286Psqas",
    "authDomain": "productivity-app-e2cbe.firebaseapp.com",
    "projectId": "productivity-app-e2cbe",
    "storageBucket": "productivity-app-e2cbe.appspot.com",
    "messagingSenderId": "203922436505",
    "appId": "1:203922436505:web:073360efa5001a30c92308",
    "measurementId": "G-62YXKEYV0B",
    "databaseURL": "https://productivity-app-e2cbe-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window.maximized = True
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf"
    }

    # Check if auth token exists and load user
    token = page.client_storage.get("auth_token")
    if token:
        try:
            user_info = auth.get_account_info(token)
            user_id = user_info['users'][0]['localId']
            user_data = db.child("users").child(user_id).get().val()
            success_message.value = f"Welcome Back, {user_data['name']}!"
            go_home()
        except Exception as e:
            page.client_storage.remove("auth_token")


    def set_cookie(token):
        import datetime
        expiry = datetime.datetime.now() + datetime.timedelta(days=30)
        ft.utils.cookies.set_cookie("auth_token", token, expires=expiry)

    def get_cookie():
        cookie_string = os.environ.get('HTTP_COOKIE', '')
        cookie = cookies.SimpleCookie()
        cookie.load(cookie_string)
        return cookie.get('auth_token').value if 'auth_token' in cookie else None

    def clear_cookie():
        ft.utils.cookies.set_cookie("auth_token", "", expires=datetime.datetime.now())

    def check_user_logged_in():
        token = get_cookie()
        if token:
            try:
                user = auth.get_account_info(token)
                go_home()
            except Exception:
                clear_cookie()

    check_user_logged_in()  

    name_field = ft.TextField(
        label='Username',
        width=250,
        height=40,
        text_size=15,
        text_style=ft.TextStyle(color='white'),
        border_color='#4c4f64',
        bgcolor='#2b2d37',
        border_radius=10,
        border_width=2,
        keyboard_type=ft.KeyboardType.NAME,
        icon=ft.icons.PERSON
    )

    email_field = ft.TextField(
        label='Email',
        width=250,
        height=40,
        text_size=15,
        text_style=ft.TextStyle(color='white'),
        border_color='#4c4f64',
        bgcolor='#2b2d37',
        border_radius=10,
        border_width=2,
        keyboard_type=ft.KeyboardType.EMAIL,
        icon=ft.icons.EMAIL_ROUNDED
    )

    password_field = ft.TextField(
        label='Password',
        width=250,
        height=40,
        text_size=15,
        text_style=ft.TextStyle(color='white'),
        border_color='#4c4f64',
        bgcolor='#2b2d37',
        border_radius=10,
        border_width=2,
        password=True,
        can_reveal_password=True,
        keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
        icon=ft.icons.LOCK_ROUNDED
    )

    error_message = ft.Text(
        value='',
        color=ft.colors.RED,
        size=15
    )

    success_message = ft.Text(
        value='',
        color=ft.colors.GREEN,
        size=15
    )

    def go_home(e):
        home.HomePage(page)

    def signin_btn(e):
        try:
            user = auth.sign_in_with_email_and_password(email_field.value, password_field.value)
            user_id = user['localId']
            user_data = db.child("users").child(user_id).get().val()
            page.client_storage.set("auth_token", user['idToken'])
            error_message.value = ""
            success_message.value = f"Welcome Back, {user_data['name']}!"
            page.update()
            go_home(e)
        except Exception as e:
            success_message.value = ""
            error_message.value = "Wrong, incorrect email or password!\n                Please try again."
            page.update()

    def signup_btn(e):
        try:
            user = auth.create_user_with_email_and_password(email_field.value, password_field.value)
            user_id = user['localId']
            user_data = {
                "name": name_field.value,
                "email": email_field.value
            }
            db.child("users").child(user_id).set(user_data)
            page.client_storage.set("auth_token", user['idToken']) 
            error_message.value = ""
            success_message.value = "Account created successfully!"
            page.update()
            go_home(e)
        except Exception as e:
            success_message.value = ""
            error_message.value = "Error, Invalid Email or Password"    
            page.update()

    def handle_signup(e):
        login.visible = False
        register.visible = True
        page.update()

    def handle_login(e):
        login.visible = True
        register.visible = False
        page.update()

    login = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Container(
                    bgcolor='#2b2d37',
                    width=330,
                    height=500,
                    border_radius=10,
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.Text(
                            value='Welcome Back!',
                            size=30,
                            font_family="Nohemi Bold"
                        ),
                        ft.Container(height=70),
                        ft.Column([
                            email_field,
                            ft.Container(height=5),

                            password_field,
                            ft.Container(height=5),

                            error_message,
                            success_message,
                            ft.Container(height=40),

                            ft.ElevatedButton(
                                text='Sign in',
                                width=250,
                                height=40,
                                color=ft.colors.WHITE,
                                on_click=signin_btn
                            ),

                            ft.TextButton(
                                text='Create Account',
                                on_click=handle_signup
                            )

                        ], horizontal_alignment='center')
                    ], horizontal_alignment='center', alignment='top')
                ),
            ], horizontal_alignment='center', alignment='center')
        )
    ])

    register = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Container(
                    bgcolor='#2b2d37',
                    width=330,
                    height=500,
                    border_radius=10,
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.Text(
                            value='   Welcome To\n your New Life!',
                            size=25,
                            font_family="Nohemi Bold"
                        ),
                        ft.Container(height=30),
                        ft.Column([
                            name_field,
                            ft.Container(height=5),
                            
                            email_field,
                            ft.Container(height=5),

                            password_field,

                            error_message,
                            success_message,
                            ft.Container(height=5),

                            ft.ElevatedButton(
                                text='Create Account',
                                width=250,
                                height=40,
                                color=ft.colors.WHITE,
                                on_click=signup_btn
                            ),

                            ft.TextButton(
                                text='Log In',
                                on_click=handle_login
                            )

                        ], horizontal_alignment='center')
                    ], horizontal_alignment='center', alignment='top')
                ),
            ], horizontal_alignment='center', alignment='center')
        )
    ])

    login.visible = True
    register.visible = False
    page.add(login)
    page.add(register)

    # Add route to page


if __name__ == '__main__':
    ft.app(target=main)
