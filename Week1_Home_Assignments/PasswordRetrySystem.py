Str_Correct_Password = "openAI123"
for i in range(1,4,1):
    Str_User_Password = input("Enter your password: ")
    if(Str_Correct_Password == Str_User_Password):
        print("Login Successfull")
        break