def FizzBuzz(n):
    for i in range(1,n+1):
        if(i%3 == 0 and i%5 == 0):
            print("FizzBuzz")
        elif(i%3 == 0):
            print("Fizz")
        elif(i%5 == 0):
            print("Buzz")
        else:
            print(str(i))
            
input_value = input("Enter a number: ")
if input_value.isdigit() and int(input_value) > 0:
    FizzBuzz(int(input_value))
else:
    print("Please enter a positive integer")