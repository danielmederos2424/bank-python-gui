from classes import *

# Initialization of owners
owner1 = Person("123456789", "John", "Smith")
owner2 = Person("987654321", "Anna", "Johnson")
owner3 = Person("456789123", "Louis", "Martinez")
owner4 = Person("789123456", "Mary", "Brown")

# Initialization of ordinary savings accounts
savings_account1 = OrdinarySavingsAccount("0001234567", "USD", 1000, "01/01/24", owner1, card=Card("1234567812345678"), beneficiary=owner2)
savings_account2 = OrdinarySavingsAccount("0007654321", "EUR", 2000, "01/02/24", owner2, card=Card("8765432187654321"), beneficiary=owner1)

# Initialization of fixed-term accounts
fixed_term_account1 = FixedTermAccount("0009876543", "USD", 5000, "01/03/24", owner3, 6)
fixed_term_account2 = FixedTermAccount("0006543219", "EUR", 10000, "01/04/24", owner4, 12)

# Initialization of fund formation accounts
fund_account1 = FundFormationAccount("0001112223", "USD", 1500, "01/05/24", owner1, 100)
fund_account2 = FundFormationAccount("0003334445", "EUR", 3000, "01/06/24", owner3, 200)

# Initialization of the bank
bank = Bank()
bank.add_account(savings_account1)
bank.add_account(savings_account2)
bank.add_account(fixed_term_account1)
bank.add_account(fixed_term_account2)
bank.add_account(fund_account1)
bank.add_account(fund_account2)

# Account transactions
bank.make_deposit("0001234567", 200, "15/01/24")
bank.make_withdrawal("0009876543", 100, "15/01/24")
bank.make_deposit("0001112223", 100, "01/06/24")
bank.make_withdrawal("0007654321", 500, "01/06/24")
bank.make_deposit("0006543219", 500, "15/04/24")
bank.make_withdrawal("0003334445", 100, "01/07/24")
