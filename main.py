import datetime
import os
import json
import re

class ATMManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.current_user = None
        self.current_acct = None
        
        if not os.path.exists('data'):
            os.makedirs('data')
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

    def save_users(self, users_data):
        with open(self.users_file, "w") as f:
            json.dump(users_data, f, indent=4)

    def register(self):
        print("\n" + "="*40)
        print("      NEW ACCOUNT REGISTRATION")
        print("="*40)
        
        # 1. Account Number Validation (Exactly 12 Integers)
        while True:
            acct_num = input("Enter 12-digit Account Number: ")
            if acct_num.isdigit() and len(acct_num) == 12:
                break
            print("Error: Account number must be exactly 12 integers (e.g., 123456789012).")

        with open(self.users_file, "r") as f:
            users = json.load(f)
        if acct_num in users:
            print("Error: This account number is already registered!")
            return

        # 2. Name Validation (Only Alphabets and Spaces)
        while True:
            name = input("Enter Account Holder Name: ")
            if all(x.isalpha() or x.isspace() for x in name) and len(name.strip()) >= 3:
                name = name.strip().title()
                break
            print("Error: Name must contain only alphabets and be at least 3 characters long.")

        # 3. Bank Name Validation (Only Alphabets)
        while True:
            bank = input("Enter Bank Name: ")
            if all(x.isalpha() or x.isspace() for x in bank) and len(bank.strip()) >= 2:
                bank = bank.strip().upper()
                break
            print("Error: Bank name must contain only alphabets.")

        # 4. Date of Birth Validation (DD-MM-YYYY format)
        while True:
            dob = input("Enter DOB (DD-MM-YYYY): ")
            if re.match(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$", dob):
                break
            print("Error: Invalid format. Use DD-MM-YYYY (e.g., 15-08-2000).")
        
        # 5. PIN Validation (4 Digits)
        while True:
            pin = input("Set a 4-digit Secret PIN: ")
            if pin.isdigit() and len(pin) == 4:
                break
            print("Error: PIN must be exactly 4 digits.")

        # Save data to JSON
        users[acct_num] = {
            "name": name,
            "bank": bank,
            "dob": dob,
            "pin": pin,
            "balance": 1000.0
        }
        self.save_users(users)
        print(f"\nSUCCESS: Account created for {name} in {bank}!")

    def login(self):
        print("\n" + "="*40)
        print("           ATM LOGIN")
        print("="*40)
        acct_num = input("Account Number: ")
        pin = input("Enter PIN: ")

        with open(self.users_file, "r") as f:
            users = json.load(f)

        if acct_num in users and users[acct_num]["pin"] == pin:
            self.current_user = users[acct_num]
            self.current_acct = acct_num
            print(f"\nWelcome, {self.current_user['name']}!")
            return True
        else:
            print("Login Failed: Incorrect Account Number or PIN.")
            return False

    def log_transaction(self, description):
        """Requirement 5 & 7: Date and time description in one line"""
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_file = f"data/trans_{self.current_acct}.txt"
        
        with open(log_file, "a") as f:
            f.write(f"{now} | {description}\n")

    def show_mini_statement(self):
        """Requirement 6: Last 3 transactions"""
        log_file = f"data/trans_{self.current_acct}.txt"
        print("\n--- MINI STATEMENT (Last 3) ---")
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
                history = lines[-3:] if len(lines) > 0 else ["No transactions found."]
                for entry in history:
                    print(entry.strip())
        else:
            print("No history file found.")

    def update_balance_in_file(self):
        with open(self.users_file, "r") as f:
            users = json.load(f)
        users[self.current_acct]["balance"] = self.current_user["balance"]
        self.save_users(users)

# --- EXECUTION ---
def main():
    atm = ATMManager()
    
    while True:
        if not atm.current_user:
            print("\n1. Register | 2. Login | 3. Exit")
            choice = input("Choice: ")
            if choice == '1': atm.register()
            elif choice == '2': atm.login()
            elif choice == '3': break
        else:
            print(f"\n[{atm.current_user['bank']} ATM MENU]")
            print("1. Account Details\n2. Deposit\n3. Withdraw\n4. Mini Statement\n5. Logout")
            choice = input("\nOption: ")

            if choice == '1':
                print(f"\n--- Details ---")
                print(f"Holder: {atm.current_user['name']}\nA/C: {atm.current_acct}\nBank: {atm.current_user['bank']}\nBalance: ${atm.current_user['balance']:.2f}")

            elif choice == '2':
                try:
                    amt = float(input("Deposit Amount: "))
                    if amt > 0:
                        atm.current_user['balance'] += amt
                        atm.update_balance_in_file()
                        atm.log_transaction(f"CR: +${amt:.2f} | Bal: ${atm.current_user['balance']:.2f}")
                        print("Deposit Successful.")
                    else: print("Invalid amount.")
                except ValueError: print("Enter numeric value.")

            elif choice == '3':
                try:
                    amt = float(input("Withdraw Amount: "))
                    if 0 < amt <= atm.current_user['balance']:
                        atm.current_user['balance'] -= amt
                        atm.update_balance_in_file()
                        atm.log_transaction(f"DR: -${amt:.2f} | Bal: ${atm.current_user['balance']:.2f}")
                        print("Cash Dispatched.")
                    else: print("Invalid amount or Low Balance.")
                except ValueError: print("Enter numeric value.")

            elif choice == '4':
                atm.show_mini_statement()

            elif choice == '5':
                atm.current_user = None
                atm.current_acct = None
                print("Logged out safely.")

if __name__ == "__main__":
    main()