import tkinter as tk
from tkinter import messagebox, simpledialog
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, account_num, pin, balance):
        self.account_num = account_num
        self.pin = pin
        self.balance = balance

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

class SavingsAccount(Account):
    def __init__(self, account_num, pin, balance, min_deposit=1000, max_withdraw=50000):
        super().__init__(account_num, pin, balance)
        self.min_deposit = min_deposit
        self.max_withdraw = max_withdraw

    def deposit(self, amount):
        if amount < self.min_deposit:
            return f"Minimum deposit amount is ${self.min_deposit}"
        self.balance += amount
        self.update_balance_in_file()
        return f"Deposit successful. Your new balance is ${self.balance}"

    def withdraw(self, amount):
        if amount > self.max_withdraw:
            return f"Maximum withdrawal limit is ${self.max_withdraw}"
        elif amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.update_balance_in_file()
        return f"Withdrawal successful. Your new balance is ${self.balance}"

    def update_balance_in_file(self):
        with open('C:\\Users\\GILBERT VENIDA\\OneDrive\\Documents\\savings.txt', 'r+') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                acc_info = line.strip().split(',')
                if acc_info[0] == str(self.account_num):
                    lines[i] = f"{self.account_num},{self.pin},{self.balance:.2f}\n"

            file.seek(0)
            file.writelines(lines)
            file.truncate()

class CheckingAccount(Account):
    def __init__(self, account_num, pin, balance):
        super().__init__(account_num, pin, balance)

    def deposit(self, amount):
        self.balance += amount
        self.update_balance_in_file()
        return f"Deposit successful. Your new balance is ${self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.update_balance_in_file()
        return f"Withdrawal successful. Your new balance is ${self.balance}"

    def update_balance_in_file(self):
        with open('C:\\Users\\GILBERT VENIDA\\OneDrive\\Documents\\checking.txt', 'r+') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                acc_info = line.strip().split(',')
                if acc_info[0] == str(self.account_num):
                    lines[i] = f"{self.account_num},{self.pin},{self.balance:.2f}\n"

            file.seek(0)
            file.writelines(lines)
            file.truncate()

class ATM:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account_num, pin, account_type, balance):
        if self.get_account(account_num) is not None:
            return
        if self.get_account_by_pin(pin) is not None:
            return
        if account_type == "Savings":
            self.accounts[account_num] = SavingsAccount(account_num, pin, balance)
        elif account_type == "Checking":
            self.accounts[account_num] = CheckingAccount(account_num, pin, balance)

    def get_account(self, account_num):
        return self.accounts.get(account_num)

    def get_account_by_pin(self, pin):
        for account in self.accounts.values():
            if account.pin == pin:
                return account
        return None

class PINHandler:
    def __init__(self, savings_file, checking_file):
        self.savings_file = savings_file
        self.checking_file = checking_file

    def validate_credentials(self, account_num, pin):
        
        with open(self.savings_file, 'r') as file:
            for line in file:
                acc_num, acc_pin, _ = line.strip().split(',')
                if acc_num == account_num and acc_pin == pin:
                    return "Savings"

        
        with open(self.checking_file, 'r') as file:
            for line in file:
                acc_num, acc_pin, _ = line.strip().split(',')
                if acc_num == account_num and acc_pin == pin:
                    return "Checking"

        
        return None


class ATMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BANKO DE GILBERT")
        self.root.configure(bg="#03045e")

        self.savings_file = "C:\\Users\\GILBERT VENIDA\\OneDrive\\Documents\\savings.txt"
        self.checking_file = "C:\\Users\\GILBERT VENIDA\\OneDrive\\Documents\\checking.txt"

        self.pin_handler = PINHandler(self.savings_file, self.checking_file)

        self.center_window()
        self.header_frame = tk.Frame(root, bg="#03045e")
        self.header_frame.pack(pady=20)

        self.atm_label = tk.Label(self.header_frame, text="BANKO DE GILBERT", font=("Helvetica", 24, "bold"), bg="#03045e", fg="white")
        self.atm_label.pack(pady=20)

        self.account_type_label = tk.Label(self.header_frame, text="Select Account Type:", font=("Helvetica", 14), bg="#03045e", fg="white")
        self.account_type_label.pack()

        self.savings_button = tk.Button(self.header_frame, text="Savings", font=("Helvetica", 12), bg="#ffd100", fg="#03045e", command=lambda: self.set_account_type("Savings"))
        self.savings_button.pack(anchor=tk.CENTER, pady=5)

        self.checking_button = tk.Button(self.header_frame, text="Checking", font=("Helvetica", 12), bg="#ffd100", fg="#03045e", command=lambda: self.set_account_type("Checking"))
        self.checking_button.pack(anchor=tk.CENTER, pady=5)

        self.atm = ATM()

    def center_window(self):
        width = 400
        height = 350
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_account_type(self, account_type):
        self.account_type = account_type
        self.show_login()

    def show_login(self):
        self.header_frame.pack_forget()

        self.login_frame = tk.Frame(self.root, bg="#03045e")
        self.login_frame.pack()

        self.account_num_label = tk.Label(self.login_frame, text="Enter your account number:", font=("Helvetica", 14), bg="#03045e", fg="white")
        self.account_num_label.pack()

        self.account_num_entry = tk.Entry(self.login_frame, font=("Helvetica", 14))
        self.account_num_entry.pack(pady=10, padx=20)

        self.pin_label = tk.Label(self.login_frame, text="Enter your 4-digit PIN:", font=("Helvetica", 14), bg="#03045e", fg="white")
        self.pin_label.pack()

        self.pin_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 14))
        self.pin_entry.pack(pady=10, padx=20)

        self.login_button = tk.Button(self.login_frame, text="Login", font=("Helvetica", 15, "bold"), bg="#ffd100",fg="#03045e", command=self.validate_login)
        self.login_button.pack(pady=10, padx=20)

    def validate_login(self):
        account_num = self.account_num_entry.get()
        entered_pin = self.pin_entry.get()
        account_type = self.pin_handler.validate_credentials(account_num, entered_pin)
        if account_type == self.account_type:
            balance = self.get_balance(account_num, entered_pin)
            if balance is not None:
                self.atm.add_account(account_num, entered_pin, self.account_type, balance)
                self.show_menu()
            else:
                messagebox.showerror("Error", "Failed to retrieve account balance. Please try again.")
        else:
            messagebox.showerror("Error", "Invalid account number or PIN. Please try again.")
            self.account_num_entry.delete(0, tk.END)
            self.pin_entry.delete(0, tk.END)

    def get_balance(self, account_num, pin):
        if self.account_type == "Savings":
            file_path = self.savings_file
        elif self.account_type == "Checking":
            file_path = self.checking_file

        with open(file_path, 'r') as file:
            for line in file:
                acc_info = line.strip().split(',')
                if len(acc_info) == 3:
                    acc_num, acc_pin, balance = acc_info
                    if acc_num == account_num and acc_pin == pin:
                        return float(balance)
        return None

    def show_menu(self):
        self.login_frame.pack_forget()

        self.menu_frame = tk.Frame(self.root, bg="#03045e")
        self.menu_frame.pack()

        self.menu_label = tk.Label(self.menu_frame, text="Choose an option:", font=("Helvetica", 18, "bold"), bg="#03045e", fg="white")
        self.menu_label.pack()

        self.balance_button = tk.Button(self.menu_frame, text="Check Balance", font=("Helvetica", 12, "bold"), bg="#ffd100", fg="#03045e", command=self.check_balance)
        self.balance_button.pack(anchor=tk.CENTER, pady=10)

        self.deposit_button = tk.Button(self.menu_frame, text="Deposit", font=("Helvetica", 12, "bold"), bg="#ffd100", fg="#03045e", command=self.deposit_menu)
        self.deposit_button.pack(anchor=tk.CENTER, pady=10)

        self.withdraw_button = tk.Button(self.menu_frame, text="Withdraw", font=("Helvetica", 12, "bold"), bg="#ffd100", fg="#03045e", command=self.withdraw_menu)
        self.withdraw_button.pack(anchor=tk.CENTER, pady=10)

        self.logout_button = tk.Button(self.menu_frame, text="Logout", font=("Helvetica", 12, "bold"), bg="#ffd100", fg="#03045e", command=self.logout)
        self.logout_button.pack(anchor=tk.CENTER, pady=10)

    def check_balance(self):
        account = self.atm.get_account(self.account_num_entry.get())
        if account:
            balance = account.balance 
            messagebox.showinfo("Balance", f"Your balance is: ${balance}")
        else:
            messagebox.showerror("Error", "Failed to retrieve account balance.")

    def deposit_menu(self):
        account = self.atm.get_account(self.account_num_entry.get())
        if account:
            amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
            if amount is not None:
                message = account.deposit(amount)
                messagebox.showinfo("Deposit", message)
        else:
            messagebox.showerror("Error", "Account not found.")

    def withdraw_menu(self):
        account = self.atm.get_account(self.account_num_entry.get())
        if account:
            amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
            if amount is not None:
                message = account.withdraw(amount)
                messagebox.showinfo("Withdraw", message)
        else:
            messagebox.showerror("Error", "Account not found.")

    def logout(self):
        self.menu_frame.pack_forget()
        self.account_num_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.header_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMGUI(root)
    root.mainloop()
