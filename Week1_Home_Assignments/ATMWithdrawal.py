input_withdrawal_amt = int(input("Enter the amount to withdraw:"))
if(input_withdrawal_amt % 100 == 0):
    print(f"Dispensing {input_withdrawal_amt}")
else:
    print("Invalid Amount")