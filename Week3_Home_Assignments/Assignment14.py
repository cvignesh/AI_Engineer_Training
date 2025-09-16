class CreditCardPayment:
    def process_payment(self, amount):
        print(f"Processing credit card payment of ${amount}")

class PayPalPayment:
    def process_payment(self, amount):
        print(f"Processing PayPal payment of ${amount}")
    
class BankTransferPayment:
    def process_payment(self, amount):
        print(f"Processing bank transfer payment of ${amount}")

def make_payment(payment_method, amount):
    payment_method.process_payment(amount)

# Example usage
credit_card = CreditCardPayment()
paypal = PayPalPayment()            
bank_transfer = BankTransferPayment()

if __name__ == "__main__":
    payment_methods = [credit_card, paypal, bank_transfer]
    amount = 100
    for method in payment_methods:
        make_payment(method, amount)    
