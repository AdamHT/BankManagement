from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class LoginScreen(Screen):
    def verify_credentials(self):
        app = App.get_running_app()
        if self.ids["username"].text == "Admin" and self.ids["password"].text == "password" and self.ids["account_type"].text == "Admin":
            app.root.current = 'admin_screen'
        elif self.ids["username"].text == "Teller" and self.ids["password"].text == "password" and self.ids["account_type"].text == "Teller":
            app.root.current = 'teller_screen'
    pass

class AdminScreen(Screen):
    app = App.get_running_app()
    def change_screen(self, instance):
        app = App.get_running_app()
        if instance.text == 'Manage Users':
            self.ids.screen_manager.current = 'screen_content'
        elif instance.text == 'Manage Accounts':
            self.ids.screen_manager.current = 'screen_content_one'
        else:
            self.ids.screen_manager.current = 'screen_content_two'
    def logout(self):
        app = App.get_running_app()
        app.root.current = 'login_screen'

class TellerScreen(Screen):
    app = App.get_running_app()
    def change_screen(self, instance):
        app = App.get_running_app()
        if instance.text == 'Lookup Customer':
            self.ids.screen_manager.current = 'customer_lookup_screen'
        elif instance.text == 'Transfers':
            self.ids.screen_manager.current = 'transfer_screen'
        elif instance.text == 'Customer History':
            self.ids.screen_manager.current = 'customer_history_screen'
    def logout(self):
        app = App.get_running_app()
        app.root.current = 'login_screen'
    pass

class ScreenManagement(ScreenManager):
    pass

class BankWindow(BoxLayout):
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #content = self.ids.screen_content
    

class BankApp(App):

    def build(self):
        return 

if __name__ == '__main__':
    BankApp().run()