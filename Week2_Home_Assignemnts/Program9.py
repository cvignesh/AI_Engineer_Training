class Bank_Account:
    def __init__(self, account_holder, balance, account_type):
        self.account_holder = account_holder
        self.balance = balance
        self.account_type = account_type

    def deposit(self, amount):
        if isinstance(amount, float):
            self.balance = self.balance +  amount
        else:
            raise TypeError("Amount should be in Float")
    
    def withdraw(self, amount):
        if isinstance(amount, float):
            if amount <= 0:
                raise ValueError("Enter amt great than 0")
            if self.balance - amount <= 0:
                raise ValueError("No enough balance")
            self.balance = self.balance - amount
        else:
            raise ValueError("Amount should be in Float")
    
    def display_bal(self):
        print(f" Account No:{self.account_holder}, Account_type: {self.account_type}, Balance: {self.balance} ")
        print("-----------------")
            
if(__name__ == "__main__"):
    account1 = Bank_Account("Person1", 100, 'Savings')
    account2 = Bank_Account("Person2", 1000, 'Salary')
    account1.display_bal()
    print("Depositing 500 to Person1")
    account1.deposit(500.0)
    account1.display_bal()
    print("Withdrawing 200 from Person1")  
    account1.withdraw(200.0)
    account1.display_bal() 
