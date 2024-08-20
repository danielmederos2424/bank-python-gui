from datetime import datetime, timedelta


class Person:
    def __init__(self, id_number, first_name, last_name):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id_number})"


class Card:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return f"Card {self.number}"


class Account:
    def __init__(self, number, currency, initial_balance, opening_date, owner):
        self.number = number
        self.currency = currency
        self.balance = initial_balance
        self.opening_date = datetime.strptime(opening_date, "%d/%m/%y")
        self.owner = owner
        self.transactions = []

    def deposit(self, amount, date):
        self.balance += amount
        self.transactions.append({"date": date, "type": "Deposit", "amount": amount})

    def withdraw(self, amount, date):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transactions.append({"date": date, "type": "Withdrawal", "amount": amount})

    def calculate_interest(self):
        return self.balance * 0.02

    def __str__(self):
        return f"Account {self.number} - {self.currency} - Balance: {self.balance:.2f}"


class FundFormationAccount(Account):
    def __init__(self, number, currency, initial_balance, opening_date, owner, monthly_payment):
        super().__init__(number, currency, initial_balance, opening_date, owner)
        self.monthly_payment = monthly_payment

    def deposit_monthly_payment(self, date):
        self.deposit(self.monthly_payment, date)


class FixedTermAccount(Account):
    def __init__(self, number, currency, initial_balance, opening_date, owner, term_months):
        super().__init__(number, currency, initial_balance, opening_date, owner)
        self.term_months = term_months
        self.maturity_date = self.opening_date + timedelta(days=term_months * 30)
        self.movements = False

    def deposit(self, amount, date):
        if datetime.strptime(date, "%d/%m/%y") < self.maturity_date:
            self.movements = True
        super().deposit(amount, date)

    def withdraw(self, amount, date):
        if datetime.strptime(date, "%d/%m/%y") < self.maturity_date:
            self.movements = True
        super().withdraw(amount, date)

    def calculate_interest(self):
        if datetime.today() < self.maturity_date:
            if self.movements:
                return self.balance * 0.02
            if self.term_months == 3:
                return self.balance * 0.03
            elif self.term_months == 6:
                return self.balance * 0.04
            elif self.term_months == 12:
                return self.balance * 0.05
        else:
            return self.balance * 0.02


class OrdinarySavingsAccount(Account):
    def __init__(self, number, currency, initial_balance, opening_date, owner, card=None, beneficiary=None):
        super().__init__(number, currency, initial_balance, opening_date, owner)
        self.card = card
        self.beneficiary = beneficiary

    def __str__(self):
        return f"Account {self.number} - {self.currency} - Balance: {self.balance:.2f} - Card: {self.card} - Beneficiary: {self.beneficiary}"


class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def find_account(self, account_number):
        for account in self.accounts:
            if account.number == account_number:
                return account
        return None

    def make_deposit(self, account_number, amount, date):
        account = self.find_account(account_number)
        if account:
            account.deposit(amount, date)

    def make_withdrawal(self, account_number, amount, date):
        account = self.find_account(account_number)
        if account:
            account.withdraw(amount, date)

    def total_balance(self):
        return sum(account.balance for account in self.accounts)

    def interests_to_increase(self):
        return {account.number: account.calculate_interest() for account in self.accounts}

    def fixed_term_accounts_without_interest(self):
        accounts_without_interest = []
        for account in self.accounts:
            if isinstance(account, FixedTermAccount) and account.movements:
                accounts_without_interest.append(account)
        return accounts_without_interest

    def transactions_by_month(self, month, year):
        total_inflow = 0
        total_outflow = 0
        for account in self.accounts:
            for transaction in account.transactions:
                transaction_date = datetime.strptime(transaction["date"], "%d/%m/%y")
                if transaction_date.month == month and transaction_date.year == year:
                    if transaction["type"] == "Deposit":
                        total_inflow += transaction["amount"]
                    elif transaction["type"] == "Withdrawal":
                        total_outflow -= transaction["amount"]
        return total_inflow, total_outflow

    def accounts_by_client(self, id_number):
        client_accounts = [account for account in self.accounts if account.owner.id_number == id_number]
        return client_accounts

    def list_by_type(self, account_type):
        type_class = None
        if account_type == "Fund formation accounts":
            type_class = FundFormationAccount
        elif account_type == "Fixed term accounts":
            type_class = FixedTermAccount
        elif account_type == "Ordinary savings accounts":
            type_class = OrdinarySavingsAccount

        if type_class:
            accounts_of_type = [account for account in self.accounts if isinstance(account, type_class)]
            return sorted(accounts_of_type, key=lambda x: x.balance, reverse=True)
        else:
            return []
