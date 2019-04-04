import requests
import json
import re

from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition, WipeTransition
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
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
    def login(self):
        app = App.get_running_app()
        App.get_running_app().sess = requests.Session()
        sess = App.get_running_app().sess
        userID = self.ids["username"].text
        password = self.ids["password"].text
        r = sess.post('https://localhost/token_login/',data={'username': userID, 'password': password}, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")
        print(r)
        json_response = json.loads(r.text)
        App.get_running_app().token = json_response['token']

        if json_response['usertype'] == 2:
            app.root.current = 'teller_screen'
        elif json_response['usertype'] == 1:
            app.root.current = 'admin_screen'

    def reset(self):
        self.ids["username"].text = ""
        self.ids["password"].text = ""
    pass

class AdminScreen(Screen):
    app = App.get_running_app()
    def change_screen(self, instance):
        #app = App.get_running_app()
        self.ids.screen_manager.transition = NoTransition()
        if instance.text == 'Create Account':
            if self.ids.screen_manager.current == 'add_user_screen' or self.ids.screen_manager.current == 'add_account_screen':
                pass
            else:
                self.ids.screen_manager.current = 'add_user_screen'
        elif instance.text == 'Manage Accounts':
            self.ids.screen_manager.current = 'user_screen'
        # elif instance.text == 'Delete Account':
        #     self.ids.screen_manager.current = 'delete_account_screen'
    
    def SetCurrentCustomer(self,firstname, lastname, address, city, state, zipcode, email, phone, ssn, username):
        App.get_running_app().adminCustomer.first_name = firstname
        App.get_running_app().adminCustomer.last_name = lastname
        App.get_running_app().adminCustomer.street_address = address
        App.get_running_app().adminCustomer.city = city
        App.get_running_app().adminCustomer.state = state
        App.get_running_app().adminCustomer.zipcode = zipcode
        App.get_running_app().adminCustomer.email = email
        App.get_running_app().adminCustomer.phone_number = phone
        App.get_running_app().adminCustomer.first_name = firstname
        App.get_running_app().adminCustomer.ssn = ssn
        App.get_running_app().adminCustomer.username = username

    def SetStatus(self, status, user):
        self.ids.status_text.text = status
        self.ids.current_customer_status_bar = user


    def SearchCustomerClick(self):
        #add the if statemtn logic stuff if a user is found
        self.ids.customer_search_label_admin.text = self.ids.lookup_ti_admin.text + " account found!"
        self.ids.current_customer_status_bar.text = self.ids.lookup_ti_admin.text

    def GoToAddAccountFromAddUser(self):
        self.ids.screen_manager.transition.direction = 'left'
        self.ids.screen_manager.current = 'add_account_screen'

    def GoToAddUserScreen(self):
        self.ids.screen_manager.transition.direction = 'left'
        self.ids.screen_manager.current = 'add_user_screen'

    def FinishAddUser(self):
        isAdmin = False
        isTeller = False

        token = App.get_running_app().token
        sess = App.get_running_app().sess
        if(self.ids.accountType.text == 'Teller'):
            isAdmin = False
            isTeller = True
        elif self.ids.accountType.text == 'Admin':
            isAdmin = True
            isTeller = False


        firstname = self.ids.firstName.text
        lastname = self.ids.lastName.text
        address = self.ids.streetAddress.text
        city = self.ids.city.text
        state = self.ids.state.text
        zipcode = self.ids.zipcode.text
        email = self.ids.email.text
        phonenumber = self.ids.phoneNumber.text
        ssn = self.ids.ssn.text
        username = self.ids.newUsername.text
        password = self.ids.newPassword.text

        cDict = { #must use dictionary, is requirement of the request library
            "first_name": firstname,
            "last_name" : lastname,
            "ss_number": ssn,
            "street_address": address,
            "city": city,
            "state": state,
            "zip_code": zipcode,
            "email_address": email,
            "phone_number": phonenumber,
            "username" : username,
            "password" : password,
            "isAdmin": isAdmin,
            "isTeller": isTeller,
					}
        hDict = {
                "Authorization": "Token " + token
            }
        r = sess.post('https://localhost/create_acct/', data = cDict, headers = hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        self.SetCurrentCustomer(firstname, lastname, address, city, state, zipcode, email, phonenumber, ssn, username)
        self.SetStatus("New Customer Added", firstname + " " + lastname)
        self.ids.screen_manager.current = 'add_account_screen'

    def AddAccount(self):
        for index, text in enumerate(self.ids.newAccountType.values):
            if index == 1:
                # caDict = {  # must use dictionary, is requirement of the request library
				# 		"username" : username,
				# 		"acct_type": acct_type,
				# 		"acct_number": acct_number,
				# 		"acct_balance": acct_balance,
				# 		}
                # hDict = {
                #     "Authorization": "Token " + token
                # }
				# 	r = sess.post('https://localhost/create_customerAcct/', data=caDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")
                #self.ids.current_customer_status_bar.text = self.ids.newAccountType.text
                self.SetStatus(self.ids.newAccountType.text + " account added!")



    def ClearDetails(self):
        self.ids['firstName'].text = ""
        self.ids['lastName'].text = ""
        self.ids['streetAddress'].text = ""
        self.ids['city'].text = ""
        self.ids['state'].text = ""
        self.ids['zipcode'].text = ""
        self.ids['email'].text = ""
        self.ids['phoneNumber'].text = ""
        self.ids['accountType'].text = "Select Amount"
        self.ids['ssn'].text = ""
        self.ids['newUsername'].text = ""
        self.ids['newPassword'].text = ""

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



class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''
    background_normal = StringProperty("")
    background_color = ListProperty([.3, .3, .7, 1])


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    background_normal = StringProperty("")
    background_color = ListProperty([.3, .3, .7, 1])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(BoxLayout):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_info()

    def get_info(self):
        w, h = 4, 3
        Matrix = [[0 for x in range(w)] for y in range(h)]
        a = [[1,2,3], [4,5,6], [7, 8, 9], [1,2,3], [4,5,6], [7, 8, 9],[1,2,3], [4,5,6], [7, 8, 9]]

        for row in a:
            for col in row:
                self.data_items.append(col)
        #self.data = [{'text': str(x)} for x in range(100)]












class CurrentAdminCustomer:
    def __init__(self):
        first_name = ""
        last_name = ""
        street_address= ""
        city= ""
        state= ""
        zipcode= ""
        email= ""
        phone_number= ""
        account_type= ""
        ssn= ""
        username = ""

class TellerScreen(Screen):
    app = App.get_running_app()
    def change_screen(self, instance):
        #app = App.get_running_app()
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

class EmailInput(TextInput):
    def __init__(self, *args, **kwargs):
        TextInput.__init__(self, *args, **kwargs)
        self.multiline = False
        self.write_tab = False

    pat = re.compile('[^@]+@[^@]+\.[^@]+')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if "@" in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '@'.join([re.sub(pat, '', s) for s in substring.split('@', 1)])
        return super(EmailInput, self).insert_text(s, from_undo=from_undo)



class ScreenManagement(ScreenManager):
    pass

class BankWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BankApp(App):
    def build(self):
        adminCustomer = CurrentAdminCustomer()
        token = ""
        sess = ""
        return




if __name__ == '__main__':
    BankApp().run()
