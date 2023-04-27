import mysql.connector




mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alpha028!",
    database="BankingInfo"
)


def create_account():
    # account creation Inputs (infinitely repeats till inputs are correct. )
    while True:
        email = input("Please enter an Email address: ")
        if "@" in email and "." in email:
            pass
        else:
            print("[ERROR] Invalid Email address. Please enter a valid Email. \n")
            continue


        password = input("Please enter your password. (This is an experimental program. Do not enter serious passwords)")
        password2 = input("Please repeat your password. ")
        if password == password2:
            if len(password) > 5:
                pass
            else:
                print("[ERROR] The password needs to have a minimum of 6 characters. ")
                continue
        else:
            print("[ERROR] Passwords don't match. Please try again. \n")
            continue
        cursor = mydb.cursor()
        query = 'SELECT email FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        if cursor.fetchone():
            print("[ERROR] This email is already in use!")
            cursor.close()
            continue
        cursor.fetchall()
        cursor.close()
        break
    cursor = mydb.cursor()
    query = 'INSERT INTO users(email, password) VALUES(%s, %s)'
    cursor.execute(query, (email, password))
    cursor.close()
    mydb.commit()

    cursor = mydb.cursor()
    query = 'SELECT id FROM users WHERE email = %s'
    cursor.execute(query, (email,))
    client_id = cursor.fetchone()[0]
    cursor.close()

    print(client_id)
    cursor = mydb.cursor()
    query = 'INSERT INTO accounts(user_id, account_type, balance) VALUES(%s, "default", 0)'
    cursor.execute(query, (client_id,))
    cursor.close()
    mydb.commit()

    return client_id


def login():
    print("Please enter your account credentials! ")
    while True:
        email = input("Please enter an Email address: ")
        password = input("Please enter your password: ")

        cursor = mydb.cursor()
        query = "SELECT id FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        tmp = None
        try:
            tmp = cursor.fetchone()[0]
        except:
            pass
        if tmp:
            client_id = tmp
            cursor.close()
            break
        else:
            print("[ERROR] Wrong password or email. Please try again. ")
        cursor.close()
    return client_id


def get_balance(user_id):
    cursor = mydb.cursor()
    query = "SELECT balance FROM accounts WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    tmp = cursor.fetchone()[0]
    cursor.close()
    return float(tmp)


def set_balance(user_id, balance):

    cursor = mydb.cursor()
    query = 'UPDATE accounts SET balance = %s WHERE user_id = %s;'
    cursor.execute(query, (balance, user_id))
    mydb.commit()
    cursor.close()


def logged_in(user_id):
    # This section is only reachable if the user is logged in. You can choose the all options here.
    print(f"Welcome! Please select one of the options below. ")
    while True:
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Check Balance")
        print("4. Logout")
        print("5. Close Account")
        print("6. Modify Account")
        choice = input("Enter choice: ")

        # Withdrawing money
        if choice == "1":
            balance = get_balance(user_id)
            print(f"You currently have {balance}$ on your bank account \n")
            amount = float(input("How much money would you like to withdraw? "))
            if amount <= 0:
                print("[ERROR] You cannot withdraw $0. ")
                continue
            if amount <= balance:
                new_bal = balance - amount
                set_balance(user_id, new_bal)
                print("You successfully updated your balance. You now have a balance of ${:.2f} \n".format(
                    get_balance(user_id)))
            else:
                print("You do not have enough money to withdraw the money.")
                continue

        # depositing money
        elif choice == "2":
            amount = float(input("How much money would you like to deposit? "))
            print(amount + get_balance(user_id))
            set_balance(user_id, amount + get_balance(user_id))
            print("You successfully updated your balance. You now have a balance of ${:.2f}".format(get_balance(user_id)))




        # checking balance
        elif choice == "3":
            print("You currently have a balance of ${:.2f}".format(get_balance(user_id)))




        # going back to the main menu.
        elif choice == "4":
            print("Logging out...")
            break
        # deleting / closing account.
        elif choice == "5":
            #show prompt to confirm
            confirm_choice = input("Are you sure you want to close your account? Please remember this action is irreversable: ")
            if(confirm_choice.lower() == "yes"):
                # deletes account
                cursor = mydb.cursor()
                print(f"Your user ID: {user_id}")
                # Delete the account from the database
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                mydb.commit()
                cursor.close()
                break
            if (confirm_choice.lower() == "no"):
                print("You have chosen to not delete your account.")
                break
            else:
                print("[ERROR] Invalid choice, returning to account.")
                break
        elif choice == "6":
            cursor = mydb.cursor()
            new_email = input("Enter your new email: ")
            if "@" in new_email and "." in new_email:
                # Update the email in the database
                cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
                mydb.commit()
                print("Email updated successfully.")
            else:
                print("Invalid email format.")
                continue
            password = input("Please enter your new password. (This is an experimental program. Do not enter serious passwords)")
            password2 = input("Please repeat your new password. ")
            if password == password2:
                if len(password) > 5:
                    pass
                else:
                    print("[ERROR] The new password needs to have a minimum of 6 characters. ")
                    continue
            # Update the email in the database
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (password2, user_id))
            mydb.commit()
            print("Password updated successfully.")
            cursor.close()
            break
        else:
            print("[ERROR] Invalid choice")


def main():
    # Main function (gets executed when the program starts)
    print("Hello, Welcome to the Caleb's Banking System")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit program")
    choice = input("Enter choice: ")


    # Initial Selection (infinitely continues unless 1 or 2 is entered.)
    if choice == "1":
        user_id = create_account()
        logged_in(user_id)


    elif choice == "2":
        user_id = login()
        logged_in(user_id)

    elif choice == "3":
        exit()

    else:
        print("[ERROR] Invalid option. ")



if __name__ == "__main__":
    while True:
        main()



