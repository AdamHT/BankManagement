
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
#:include login.kv


#class BankWidget(BoxLayout):
 #   def updateText(self):
  #      self.ids.clicked.text = "Has been clicked"


class LoginPage(Screen):
    def verify_credentials(self):
        if self.ids["username"].text == "Admin" and self.ids["password"].text == "password" and self.ids["account_type"].text == "Admin":
            self.manager.current = "admin"
        elif self.ids["username"].text == "Teller" and self.ids["password"].text == "password" and self.ids["account_type"].text == "Teller":
            self.manager.current = "teller"
    pass

class AdminPage(Screen):
    pass

class TellerPage(Screen):
    pass

class ScreenManagement(ScreenManager):
    login_page = ObjectProperty(None)
    admin_page = ObjectProperty(None)
    teller_page = ObjectProperty(None)

class BankManagementApp(App):
    def build(self):
        m = ScreenManagement(transition=FadeTransition())
        return m



if __name__ == "__main__":
    BankManagementApp().run()