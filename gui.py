import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from data import bank
from classes import *


class Application(tk.Tk):
    def __init__(self, bank):
        super().__init__()
        self.bank = bank
        self.title("Bank")
        self.style = Style(theme="darkly")
        self.geometry("1200x600")
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def center_popup_window(self, window, width, height):
        x_window = (window.winfo_screenwidth() // 2) - (width // 2)
        y_window = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x_window, y_window))

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_accounts_tab()
        self.create_operation_buttons()

    def create_accounts_tab(self):
        self.accounts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.accounts_tab, text="Accounts")

        self.treeview = ttk.Treeview(self.accounts_tab, columns=("Number", "Currency", "Balance", "Owner", "Opening Date"), show="headings")
        self.treeview.heading("Number", text="NUMBER", anchor="center")
        self.treeview.heading("Currency", text="CURRENCY", anchor="center")
        self.treeview.heading("Balance", text="BALANCE", anchor="center")
        self.treeview.heading("Owner", text="OWNER", anchor="center")
        self.treeview.heading("Opening Date", text="OPENING DATE", anchor="center")

        self.treeview.column("Number", width=100, anchor="center")
        self.treeview.column("Currency", width=100, anchor="center")
        self.treeview.column("Balance", width=100, anchor="center")
        self.treeview.column("Owner", width=200, anchor="center")
        self.treeview.column("Opening Date", width=120, anchor="center")

        self.treeview.pack(expand=True, fill="both", padx=10, pady=10)
        self.populate_treeview()

    def populate_treeview(self):
        for child in self.treeview.get_children():
            self.treeview.delete(child)

        for account in self.bank.accounts:
            self.treeview.insert("", "end", values=(account.number, account.currency, account.balance, str(account.owner), account.opening_date.strftime("%d/%m/%y")))

    def create_operation_buttons(self):
        self.operations_frame = ttk.Frame(self)
        self.operations_frame.pack(side="bottom", fill="x", pady=10)

        button_configurations = [
            ("Current Balance", self.current_balance),
            ("Interests to Increase", self.interests_to_increase),
            ("Fixed-Term Accounts without Interest", self.fixed_term_accounts_without_interest),
            ("Transactions by Month/Year", self.transactions_by_month),
            ("Accounts by Client", self.accounts_by_client),
            ("Account Transactions", self.account_transactions),
            ("List by Type", self.list_by_type)
        ]

        for text, command in button_configurations:
            ttk.Button(self.operations_frame, text=text, command=command, style='primary.TButton').pack(side="left", padx=5, pady=5)

    def current_balance(self):
        total_balance = self.bank.total_balance()
        self.show_info_window("Total Balance", f"The current balance of all accounts is: {total_balance:.2f}", 300, 120)

    def interests_to_increase(self):
        interests = self.bank.interests_to_increase()
        details = "\n".join([f"Account {number}: {interest:.2f}" for number, interest in interests.items()])
        self.show_info_window("Interests to Increase", details, 400, 200)

    def fixed_term_accounts_without_interest(self):
        accounts_without_interest = self.bank.fixed_term_accounts_without_interest()
        details = "\n".join([f"Account {account.number} - Owner: {account.owner}" for account in accounts_without_interest])
        self.show_info_window("Fixed-Term Accounts without Interest", details, 400, 200)

    def transactions_by_month(self):
        window = tk.Toplevel(self)
        window.title("Transactions by Month/Year")
        width = 320
        height = 180
        window.geometry(f"{width}x{height}")
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="Enter the month (1-12):").pack(pady=5)
        month_entry = ttk.Entry(window)
        month_entry.pack()

        ttk.Label(window, text="Enter the year (yyyy):").pack(pady=5)
        year_entry = ttk.Entry(window)
        year_entry.pack()

        buttons_frame = ttk.Frame(window)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Accept", command=lambda: self.verify_transactions_by_month(window, month_entry.get(), year_entry.get())).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=window.destroy).pack(side="left", padx=5)

        self.center_popup_window(window, width, height)

    def verify_transactions_by_month(self, window, month, year):
        try:
            month = int(month)
            year = int(year)
            if 1 <= month <= 12 and 1900 <= year <= 2100:
                total_inflow, total_outflow = self.bank.transactions_by_month(month, year)
                self.show_info_window("Transactions by Month/Year", f"Total Inflow: {total_inflow:.2f}\nTotal Outflow: {total_outflow:.2f}", 300, 150)
                window.destroy()
            else:
                messagebox.showerror("Error", "Invalid month or year. Please try again.")
        except ValueError:
            messagebox.showerror("Error", "Month and year must be integers.")

    def accounts_by_client(self):
        window = tk.Toplevel(self)
        window.title("Accounts by Client")
        width = 300
        height = 120
        window.geometry(f"{width}x{height}")
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="Enter the ID number:").pack(pady=5)
        id_entry = ttk.Entry(window)
        id_entry.pack()

        buttons_frame = ttk.Frame(window)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Accept", command=lambda: self.show_accounts_by_client(window, id_entry.get())).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=window.destroy).pack(side="left", padx=5)

        self.center_popup_window(window, width, height)

    def show_accounts_by_client(self, window, id):
        window.destroy()

        client_accounts = self.bank.accounts_by_client(id)
        if client_accounts:
            details = "\n".join(
                [f"Account {account.number} - Type: {type(account).__name__} - Balance: {account.balance:.2f}" for account in client_accounts])
            self.show_info_window("Accounts by Client", details, 400, 150)
        else:
            messagebox.showerror("Error", f"No accounts found for the client with ID {id}.")

    def account_transactions(self):
        window = tk.Toplevel(self)
        window.title("Account Transactions")
        width = 350
        height = 250
        window.geometry(f"{width}x{height}")
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="Enter the account number:").pack(pady=5)
        account_number_entry = ttk.Entry(window)
        account_number_entry.pack()

        ttk.Label(window, text="Transaction amount:").pack(pady=5)
        amount_entry = ttk.Entry(window)
        amount_entry.pack()

        ttk.Label(window, text="Select the transaction type:").pack(pady=5)
        transaction_type = tk.StringVar()
        transaction_type.set("Deposit")
        transaction_type_menu = ttk.OptionMenu(window, transaction_type, "Deposit", "Deposit", "Withdrawal")
        transaction_type_menu.pack()

        buttons_frame = ttk.Frame(window)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Accept", command=lambda: self.verify_account_transactions(window, account_number_entry.get(), amount_entry.get(), transaction_type.get())).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=window.destroy).pack(side="left", padx=5)

        self.center_popup_window(window, width, height)

    def verify_account_transactions(self, window, account_number, amount, transaction_type):
        try:
            amount = float(amount)
            account = self.bank.find_account(account_number)
            if account:
                if transaction_type == "Deposit":
                    account.deposit(amount, datetime.now().strftime("%d/%m/%y"))
                elif transaction_type == "Withdrawal":
                    account.withdraw(amount, datetime.now().strftime("%d/%m/%y"))
                self.populate_treeview()
                self.show_info_window("Account Transaction", f"{transaction_type} transaction completed successfully.", 300, 120)
                window.destroy()
            else:
                messagebox.showerror("Error", f"Account with number {account_number} not found.")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")

    def list_by_type(self):
        window = tk.Toplevel(self)
        window.title("List by Type")
        width = 300
        height = 150
        window.geometry(f"{width}x{height}")
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="Select the account type:").pack(pady=10)
        account_type = tk.StringVar()
        types = ["Fund formation accounts", "Fixed-term accounts", "Ordinary savings accounts"]
        account_type_menu = ttk.OptionMenu(window, account_type, types[0], *types)
        account_type_menu.pack()

        buttons_frame = ttk.Frame(window)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Accept", command=lambda: self.show_list_by_type(window, account_type.get())).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=window.destroy).pack(side="left", padx=5)

        self.center_popup_window(window, width, height)

    def show_list_by_type(self, window, account_type):
        window.destroy()
        accounts = self.bank.list_by_type(account_type)
        if accounts:
            details = "\n".join([f"Number: {account.number} - Balance: {account.balance:.2f} - Owner: {account.owner}" for account in accounts])
            self.show_info_window(f"List of {account_type}", details, 400, 150)
        else:
            messagebox.showerror("Error", f"No accounts found of type {account_type}.")

    def show_info_window(self, title, message, width, height):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.transient(self)
        window.grab_set()

        message_label = ttk.Label(window, text=message, wraplength=width-20, justify="left")
        message_label.pack(padx=10, pady=10)

        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)

        self.center_popup_window(window, width, height)
