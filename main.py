import requests
import json

def intro():
	print("\t\t\t\t**********************")
	print("\t\t\t\tTeam CHOT's")
	print("\t\t\t\tBANK MANAGEMENT SYSTEM")
	print("\t\t\t\t**********************")
	print("\t\t\t\tBrought To You By:")
	print("\t\t\t\t   Justin")
	print("\t\t\t\t   Adam")
	print("\t\t\t\t   Tristan")
	print("\t\t\t\t   Jonathan")

	



userChoice = ''
menuChoice = ''
userID = ''
password = ''
num = 0
intro()
endFlag = ''

while endFlag != -1:
	print("What is your username?")
	userID = input()
	print("What is your password?")
	password = input()

	sess = requests.Session()
	#resp = sess.get('http://localhost:8000/login/')
	#csrf_token = resp.cookies['csrftoken']
	r = sess.post('http://localhost:8000/token_login/',data={'username': userID, 'password': password})
	print(r)
	json_response = json.loads(r.text)
	#print(json_response)
	#second request, checking isadmin/ and isteller/


	if json_response['usertype'] == 2:
		menuChoice = ''
		while menuChoice != 4:
			print("\tUser Type: Teller")
			print("\tMAIN MENU")
			print("\t1. DEPOSIT AMOUNT")
			print("\t2. TRANSFER AMOUNT")
			print("\t3. WITHDRAW AMOUNT")
			print("\t4. EXIT")
			menuChoice = input()

			if menuChoice == '1':
				# writeAccount()
				print("\tYou picked DEPOSIT")
			elif menuChoice == '2':
				# num = int(input("\tEnter The account No. : "))
				# depositAndWithdraw(num, 1)
				print("\tYou picked TRANSFER")
			elif menuChoice == '3':
				# num = int(input("\tEnter The account No. : "))
				# depositAndWithdraw(num, 2)
				print("\tYou picked WITHDRAW")
			elif menuChoice == '4':
				# num = int(input("\tEnter The account No. : "))
				# displaySp(num)
				print("\tYou picked EXIT")
				break
			else:
				print("Invalid menu choice")

	elif json_response['usertype'] == 1:
		menuChoice = ''
		while menuChoice != 3:
			print("\tUser Type: Administrator")
			print("\tMAIN MENU")
			print("\t1. CREATE NEW ACCOUNT")
			print("\t2. REMOVE AN ACCOUNT")
			print("\t3. EXIT")
			menuChoice = input()

			if menuChoice == '1':
				# writeAccount()
				print("\tYou picked CREATE NEW ACCOUNT")
			elif menuChoice == '2':
				# num = int(input("\tEnter The account No. : "))
				# depositAndWithdraw(num, 1)
				print("\tYou picked REMOVE AN ACCOUNT")
			elif menuChoice == '3':
				# num = int(input("\tEnter The account No. : "))
				# depositAndWithdraw(num, 2)
				print("\tYou picked EXIT!")
				break
			else:
				print("Invalid menu choice")


	elif json_response['usertype'] == 0:
		print("There was an error, get fuckt")

	#elif userChoice == 'exit':
		#print("You have chosen to exit the application. Thank you for choosing TeamCHOT")
		#print("Please press any key to continue...")
		#input()
		#break

	#else:
		#print("Error: Please enter either 'admin' or 'teller'")


