import requests
import json
import re
import random

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
Window.minimum_width = 800

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

        loggedin = True

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

    def SetCurrentCustomer(self, ssn):
        App.get_running_app().adminCustomer = CurrentCustomer()
        App.get_running_app().adminCustomer.ssn = ssn

    def SetStatus(self, status):
        self.ids.status_text.text = status

    def parse_account_info(self, acct_number):

        token = App.get_running_app().token
        sess = App.get_running_app().sess

        aDict = {  # must use dictionary, is requirement of the request library
            "acct_number": acct_number

        }
        hDict = {
            "Authorization": "Token " + token
        }
        r = sess.post('https://localhost/view_customerAcct/', data=aDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")
        
        test = json.loads(r.text)
        print(test['acct_infoToBePrinted'])
        input()

        y = json.loads(r.text)
        
        print('Customer Name:', y['acct_infoToBePrinted']['first_name'], y['acct_infoToBePrinted']['last_name'])
        # print('Last Name:', y['acct_infoToBePrinted']['last_name'])
        print('Account Number:', y['acct_infoToBePrinted']['acct_number'])
        print('Account Type:', y['acct_infoToBePrinted']['acct_type'])
        # acct_balance_to_view= locale.format("%d", y['acct_infoToBePrinted']['acct_balance'], grouping=True)
        acct_balance_to_view = "{:,}".format(y['acct_infoToBePrinted']['acct_balance'])
        # print('Account Balance:$', y['acct_infoToBePrinted']['acct_balance'])
        print('Account Balance:$', acct_balance_to_view)

    def LookUpSSN(self, ssn):
        token = App.get_running_app().token
        sess = App.get_running_app().sess
        ssnDict = {"ss_number": ssn}

        hDict = {"Authorization": "Token " + token}
        r = sess.post('https://localhost/find_customerAcct/', data=ssnDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")
        test = json.loads(r.text)

    def SearchCustomerClick(self):
        #if LookUpSSN(self.ids.customer_search_label_admin.text) == true
        #App.get_running_app().recycle.get_info()
        self.SetCurrentCustomer(self.ids.customer_search_label_admin.text)
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

        self.SetCurrentCustomer(ssn)
        self.SetStatus("New Customer Added")
        self.ids.screen_manager.current = 'add_account_screen'

    def AddAccount(self):

        token = App.get_running_app().token
        sess = App.get_running_app().sess
        if App.get_running_app().adminCustomer.ssn == "":
            pass
        
        acct_number = random.randint(0, 999999999)
        caDict = {
                "ss_number" : App.get_running_app().adminCustomer.ssn,
                "acct_type": self.ids.newAccountType.text,
                "acct_number": acct_number,
                "acct_balance": self.ids.startingBalance.text,
                }
        hDict = {
            "Authorization": "Token " + token
        }
        r = sess.post('https://localhost/create_customerAcct/', data=caDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")
        #self.ids.current_customer_status_bar = self.ids.newAccountType.text
        self.SetStatus(self.ids.newAccountType.text + " account added!")
        self.ResetAddAccountScreen()


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
        self.ids.newAccountType.text = "Select Account"
        self.ids.startingBalance.text = ""
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
    pass

    # def __init__(self, **kwargs):
    #     super(RV, self).__init__(**kwargs)
    #     # if loggedin == True:
    #     #     self.get_info()


















class CurrentCustomer:
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

class CurrentTellerCustomer:
    def __init__(self):
        ssn = ""

class TellerScreen(Screen):
    chosenAccount1 = ""
    chosenAccount2 = ""
    activeCustomer = False
    def SetCurrentCustomer(self):
        if self.check_is_integer(self.ids.lookup_ti.text) == 0 or self.check_account_length(self.ids.lookup_ti.text) == 0:
            self.UpdateStatusBar("Enter valid SSN", 'Error')
            self.activeCustomer = False
            return
        self.activeCustomer = True
        self.UpdateStatusBar("User account found!", 'Valid')
        App.get_running_app().tellerCustomer = CurrentTellerCustomer()
        App.get_running_app().tellerCustomer.ssn = self.ids.lookup_ti.text

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
        elif instance.text == 'Payments':
            self.ids.screen_manager.current = 'payments_screen'

    def parse_account_info_teller(self, acct_number):
        token = App.get_running_app().token
        sess = App.get_running_app().sess
        aDict = {  # must use dictionary, is requirement of the request library
            "acct_number": acct_number

        }
        hDict = {
            "Authorization": "Token " + token
        }
        r = sess.post('https://localhost/view_customerAcct/', data=aDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        test = json.loads(r.text)

        y = json.loads(r.text)

        fetched_acct_teller_details = str(y['acct_infoToBePrinted']['acct_number']) + " - " + y['acct_infoToBePrinted']['acct_type'] + " $" + str(y['acct_infoToBePrinted']['acct_balance'])
        return fetched_acct_teller_details

        #print('Account Type:', y['acct_infoToBePrinted']['acct_type'])

    def Transfer(self):
        token = App.get_running_app().token
        sess = App.get_running_app().sess
        chosenAccount1 = self.ids.transferFromSpinner.text.split(' ')[0]
        chosenAccount2 = self.ids.transferToSpinner.text.split(' ')[0]
        print('account from: ' + chosenAccount1)
        print('account to: ' + chosenAccount2)
        amount = self.ids.transferAmount.text

        tDict = {  # must use dictionary, is requirement of the request library
					"to_acct_number": int(chosenAccount2),
					"from_acct_number": int(chosenAccount1),
					"transfer_amount": amount,

				}
        hDict = {
					"Authorization": "Token " + token
				}
        r = sess.post('https://localhost/transfer_customerAcct/', data=tDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        self.resetPages()
        self.SearchCustomer()

    def Deposit(self):
        token = App.get_running_app().token
        sess = App.get_running_app().sess


        chosenAccount1 = self.ids.depositSpinner.text.split(' ')[0]
        amount = self.ids.depositAmount.text
        aDict = {  # must use dictionary, is requirement of the request library
					"acct_number": int(chosenAccount1),
					"deposit_amount": amount,

        }
        hDict = {
					"Authorization": "Token " + token
				}
        r = sess.post('https://localhost/deposit_customerAcct/', data=aDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        self.resetPages()
        self.SearchCustomer()

    def Withdrawal(self):
        token = App.get_running_app().token
        sess = App.get_running_app().sess
        chosenAccount1 = self.ids.withdrawalSpinner.text.split(' ')[0]
        amount = self.ids.withdrawalAmount.text
        aDict = {  # must use dictionary, is requirement of the request library
					"acct_number": int(chosenAccount1),
					"withdrawl_amount": amount,

        }
        hDict = {
					"Authorization": "Token " + token
				}
        r = sess.post('https://localhost/withdrawl_customerAcct/', data=aDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        self.resetPages()
        self.SearchCustomer()

    def Payments(self):
        pass

    def resetPages(self):
        self.ids.lookup_ti.text = ""

        self.ids.transferFromSpinner.text = "Select Account"
        self.ids.transferToSpinner.text = "Select Account"
        self.ids.transferAmount.text = ""

        self.ids.depositSpinner.text = "Select Account"
        self.ids.depositAmount.text = ""

        self.ids.withdrawalSpinner.text = "Select Account"
        self.ids.withdrawalAmount.text = ""

    def check_is_integer(self, number_to_check):
        try:
            val = int(number_to_check)
            return 1
        except ValueError:
            return 0

    def check_account_length(self, num):
        length_count = len(num)
        if length_count == 9:
            return 1
        else:
            return 0

    def SearchCustomer(self):
        if self.activeCustomer == False:
            return
        else:
            token = App.get_running_app().token
            sess = App.get_running_app().sess

            ssnDict = {  # must use dictionary, is requirement of the request library
                        "ss_number": App.get_running_app().tellerCustomer.ssn

                    }
            hDict = {
                        "Authorization": "Token " + token
                    }
            r = sess.post('https://localhost/find_customerAcct/', data=ssnDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

            test = json.loads(r.text)
            print(test['acct_numbers'])
            #print(test['acct_infoToBePrinted'])
            # after this you'll have a list of the account numbers associated with the SSN you used
            # to search. now run the for loop below to loop through and give you the details you need
            # for the teller menu dropdowns
            accounts = []
            for acct_number in test['acct_numbers']:
                accounts.append(self.parse_account_info_teller(acct_number))
            self.ids.transferFromSpinner.values = accounts
            self.ids.transferToSpinner.values = accounts
            self.ids.depositSpinner.values = accounts
            self.ids.withdrawalSpinner.values = accounts

    def UpdateStatusBar(self, status, check):
        self.ids.status.text = status
        if check == "Error":
            self.ids.status.background_color = 1,0,0,1

    def logout(self):

        app = App.get_running_app()
        app.root.transition = NoTransition()
        app.root.current = 'login_screen'
        self.resetPages()


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
        adminCustomer = CurrentCustomer()
        tellerCustomer = CurrentTellerCustomer()
        token = ""
        sess = ""

    data_items = ListProperty([])
    def get_info(self):
        token = App.get_running_app().token
        sess = App.get_running_app().sess
        ssnDict = {  # must use dictionary, is requirement of the request library
                    "ss_number": App.get_running_app().adminCustomer.ssn
                }
        hDict = {
                    "Authorization": "Token " + token
                }
        r = sess.post('https://localhost/find_customerAcct/', data=ssnDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        test = json.loads(r.text)

        print(test['acct_numbers'])

        b = []

        for acct_number in test['acct_numbers']:
            #parse_account_info(acct_number)
            b.append([self.get_list_info(acct_number)])

        # b = []
        # b.append(['one'])
        # b.append(['two'])
        # b.append(['three'])



        for row in b:
            for col in row:
                self.data_items.append(col)
        #self.data = [{'text': str(x)} for x in range(100)]
        return

    #loggedin = False

    def get_list_info(self, acct_number):

        token = App.get_running_app().token
        sess = App.get_running_app().sess

        aDict = {  # must use dictionary, is requirement of the request library
            "acct_number": acct_number

        }
        hDict = {
            "Authorization": "Token " + token
        }
        r = sess.post('https://localhost/view_customerAcct/', data=aDict, headers=hDict, verify="C:/Users/Adam PC/Desktop/Apache24/certs/Ursus.crt")

        test = json.loads(r.text)
        print(test['acct_infoToBePrinted'])
        #input()

        y = json.loads(r.text)

        #print('Customer Name:', y['acct_infoToBePrinted']['first_name'], y['acct_infoToBePrinted']['last_name'])
        # print('Last Name:', y['acct_infoToBePrinted']['last_name'])
        #print('Account Number:', y['acct_infoToBePrinted']['acct_number'])
        #print('Account Type:', y['acct_infoToBePrinted']['acct_type'])
        # acct_balance_to_view= locale.format("%d", y['acct_infoToBePrinted']['acct_balance'], grouping=True)
        #acct_balance_to_view = "{:,}".format(y['acct_infoToBePrinted']['acct_balance'])
        # print('Account Balance:$', y['acct_infoToBePrinted']['acct_balance'])
        #print('Account Balance:$', acct_balance_to_view)
        f = '{0} {1:>30} {2:>30}'
        liststring = f.format(str(y['acct_infoToBePrinted']['acct_number']), y['acct_infoToBePrinted']['acct_type'], '$' +str(y['acct_infoToBePrinted']['acct_balance']))
        #liststring = str(y['acct_infoToBePrinted']['acct_number']) + "        " + y['acct_infoToBePrinted']['acct_type'] + '        $' + str(y['acct_infoToBePrinted']['acct_balance'])
        return liststring

if __name__ == '__main__':
    BankApp().run()


#####################################
# print("\tPlease enter SSN or Username to remove")
# 				ss_number = input() <----- this is for the SSN field in your search in teller menu
                # after the ssn is input, when you hit the search button or whatever the fuck
                # you'll then use the below to send that information off to the view, and it will return
                # the account number(s) associated with that SSN

# 				dDict = {  # must use dictionary, is requirement of the request library
# 					"ss_number": ss_number,
# 				}
# 				hDict = {
# 					"Authorization": "Token " + token
# 				}
# 				r = sess.post('https://localhost/delete_User/', data=dDict, headers=hDict,verify="C:/Users/Justin/Desktop/Apache24/Apache24/certs/Ursus.crt")

# 				test = json.loads(r.text)
# 				print(test['acct_infoToBePrinted'])
                # after this you'll have a list of the account numbers associated with the SSN you used
                # to search. now run the for loop below to loop through and give you the details you need
                # for the teller menu dropdowns
                #for acct_number in test['acct_numbers']:
				#	parse_account_info_teller(acct_number)