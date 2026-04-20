
# 🏦 ATM Management System (Python)

This project is a simple ATM system developed using Python. It is a command-line based program that allows users to create an account, log in, and perform basic banking operations like deposit, withdrawal, and checking transaction history.

---

## 📌 Features

* New user registration with proper input validation
* Login using account number and PIN
* Deposit money into account
* Withdraw money with balance checking
* Mini statement showing last 3 transactions
* Transaction history stored with date and time
* User data stored using JSON file

---

## 🛠️ Technologies Used

* Python
* JSON (for storing user data)
* File Handling
* Regular Expressions

---

## 📂 Project Structure

ATM-Management-System/

├── data/

│   ├── users.json (stores user details)

│   ├── trans_<account>.txt (stores transaction history)


├── atm.py (main program)

└── README.md

---

## ▶️ How to Run

1. Make sure Python is installed
2. Download or clone the project
3. Open terminal / command prompt
4. Run the file using:

python atm.py

---

## 🧾 Working of the Project

* First, the user can register by entering details like account number, name, bank, DOB, and PIN.
* After registration, the user can log in using account number and PIN.
* Once logged in, the user gets options to check details, deposit, withdraw, view mini statement, or logout.
* All transactions are saved with date and time in a separate file for each account.

---

## ⚠️ Validations

* Account number must be exactly 12 digits
* Name should contain only alphabets
* DOB format must be DD-MM-YYYY
* PIN must be 4 digits
* Duplicate accounts are not allowed

---

## 🚀 Future Scope

* Add GUI for better user interface
* Improve security by encrypting PIN
* Add OTP verification
* Connect with a database

---

## 👩‍💻 Author

Diksha Gade

