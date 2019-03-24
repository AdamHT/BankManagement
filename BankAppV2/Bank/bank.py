from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition, WipeTransition
from kivy.core.window import Window
Window.minimum_height = 500
Window.minimum_width = 700

class LoginScreen(Screen):
    def verify_credentials(self):
        app = App.get_running_app()
        app.root.transition = WipeTransition()
        if self.ids["username"].text == "Admin" and self.ids["password"].text == "password":# and self.ids["account_type"].text == "Admin":
            app.root.current = 'admin_screen'
        elif self.ids["username"].text == "Teller" and self.ids["password"].text == "password":# and self.ids["account_type"].text == "Teller":
            app.root.current = 'teller_screen'
        #self.reset()
    #def reset():
        #self.ids
    pass

class AdminScreen(Screen):
    app = App.get_running_app()

    def change_screen(self, instance):
        app = App.get_running_app()
        self.ids.screen_manager.transition = NoTransition()
        if instance.text == 'Manage Users':
            self.ids.screen_manager.current = 'user_screen'
        elif instance.text == 'Add Account':
            self.ids.screen_manager.current = 'add_account_screen'
        elif instance.text == 'Delete Account':
            self.ids.screen_manager.current = 'delete_account_screen'

    def SearchCustomerClick(self):
        #add the if statemtn logic stuff if a user is found
        self.ids.customer_search_label_admin.text = self.ids.lookup_ti_admin.text + " account found!"
        self.ids.current_customer_status_bar.text = self.ids.lookup_ti_admin.text
    def GoToAddUserScreen(self):
        self.ids.screen_manager.transition.direction = 'left'
        self.ids.screen_manager.current = 'add_user_screen'

    def BackToAdminScreen(self):
        self.ids.screen_manager.transition.direction = 'right'
        self.ids.screen_manager.current = 'user_screen'

    def AcceptNewCustomerClick(self):
        self.ids.screen_manager.current = 'add_account_screen'

    def ResetUserScreen(self):
        pass

    def ResetAddUserScreen(self):
        pass

    def ResetAddAccountScreen(self):
        pass

    def logout(self):
        app = App.get_running_app()
        app.root.transition = NoTransition()
        app.root.current = 'login_screen'


class TellerScreen(Screen):
    app = App.get_running_app()
    def change_screen(self, instance):
        app = App.get_running_app()
        self.ids.screen_manager.transition = NoTransition()
        if instance.text == 'Lookup Customer':
            self.ids.screen_manager.current = 'customer_lookup_screen'
        elif instance.text == 'Transfers':
            self.ids.screen_manager.current = 'transfer_screen'
        elif instance.text == 'Deposits':
            self.ids.screen_manager.current = 'deposit_screen'
        elif instance.text == 'Withdrawals':
            self.ids.screen_manager.current = 'withdrawal_screen'
    def logout(self):
        app = App.get_running_app()
        app.root.transition = NoTransition()
        app.root.current = 'login_screen'
        #self.reset()

class ScreenManagement(ScreenManager):
    pass

class BankWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BankApp(App):
    def build(self):
        return


if __name__ == '__main__':
    BankApp().run()
