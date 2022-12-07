#User Authentication project
import re
import random
import smtplib,ssl
import time
import keyboard
from verify_email import verify_email, verify_email_async

class Initial:

    def welcome():
        return """
        
        !!! Welcome to Amkart !!! """


    def user_choice():
        user_choice_input = input("""
Do you want to SIGN IN / SIGN UP / PASSWORD RESET
Press (1) for SIGNING IN 
Press (2) for SIGNING UP 
Press (3) for PASSWORD RESET
Press (4) for QUIT 

Enter you choice : """)

        while(True):

            if user_choice_input == '1':
                return signIn_performer()

            elif user_choice_input == '2':
                return signUp_performer()

            elif user_choice_input == '3':
                return password_resetter()

            elif user_choice_input == '4':
                return "Exiting Amakart !!!"

def project_execution():
    
    print(Initial.welcome())
    print(Initial.user_choice())


def signUp_performer():

    user_name_input = ""
    first_name_input = ""
    last_name_input = ""

    first_name_input = input("Enter your first name : ")
    last_name_input = input("Enter your last name : ")
    user_created = SignUp(first_name_input,last_name_input)

    while(True):
        user_name_input = input("Enter your user name : ")

        if user_created.if_id_already_exists(user_name_input)==True:
            print("User ID already exists \nPlease try a different user name")
            continue
        else:
            break
        
    email_address_input = ""

    while(True):
        email_address_input = input("Enter your email ID : ")

        if SignUp.if_mail_already_exists(email_address_input)==True:
            print("Email ID already exists \nPlease try a different Email ID")
            continue
        else:
            break

    while(True):

        if SignUp.email_validation(email_address_input)=="Enter a valid EMAIL - ID":
            print(SignUp.email_validation(email_address_input))
            continue
        else:
            break

    while(True):
        code = SignUp.email_code_generation()
        print(SignUp.email_code_sender(code,email_address_input))
        SignIn.countdown_creater()
        if SignIn.countdown_creater()==True:
            code_input = input("Enter the verififcation PIN : ")
            if SignUp.email_code_validator(code_input,code)==True:
                break
            else:
                print(SignUp.email_code_validator(code_input,code))
                continue
        else:
            print(SignIn.countdown_creater())
            loop_input = input("Do you want to continue with new code? Yes/No : ")
            if loop_input.lower()=='yes':
                continue
            elif loop_input.lower()=='no':
                print("Exiting...")
                exit()
            
    password_input = input("Please enter your password : ")
    password_created = PasswordReset(first_name_input,last_name_input,password_input)

    while(True):

        if password_created.if_mix_of_char()==True:
            Db.first_names_db_update(first_name_input)
            Db.last_names_db_update(last_name_input)
            Db.user_names_db_update(user_name_input)
            Db.email_ids_db_update(email_address_input)
            Db.passwords_db_update(password_input)
            # print(Db.user_names_db,Db.email_ids_db,Db.passwords_db)
            return 'User created'
        else:
            print(password_created.if_mix_of_char())
            password_input = input("Enter your password : ")
            password_created.update_temp_pwd(password_input)
            continue

def signIn_performer():
    #user id validation , password validation
    user_name_input = ""
    email_address_input = ""

    while(True):

        login_choice = input("""

Do you want to login using Email ID or User ID
Press (1) to login with User ID
Press (2) to login with Email ID
Press (3) to quit()
Your choice :  """)

        if login_choice == '1' or login_choice == '2' or login_choice == '3':
            break
        else:
            print("Enter values between 1-3")
            continue
            

    if login_choice == '1':
        while(True):
            user_name_input = input("Enter your user name : ")
            if SignIn.if_user_id_already_exists(user_name_input)==True:
                break
            else:
                print("User ID doesn't exist . Please enter the correct username")
                continue

    elif login_choice == '2':
        while(True):
            email_address_input = input("Enter your Email ID : ")
            if SignUp.if_mail_already_exists(email_address_input)==True:
                break
            else:
                print("Email ID doesn't exist . Please enter the correct mail ID")
                continue
    
    elif login_choice == '3':
        exit()

    no_of_attempts = 3
    while(no_of_attempts>0):
        password_input = ""

        while(True):
            if no_of_attempts>0:
                while(True):
                    password_input = input("Please enter your password : ")
                    if PasswordReset.password_validate(username=user_name_input,email_address=email_address_input,password=password_input,login_choice=login_choice)==True:
                        return "Account Logged In"
                    else:
                        print(PasswordReset.password_validate(username=user_name_input,email_address=email_address_input,password=password_input,login_choice=login_choice))
                        no_of_attempts = no_of_attempts - 1
                        print(f"Attempts remaining : {no_of_attempts} ")
                        if no_of_attempts==0:
                            PasswordReset.password_lock(username=user_name_input,email_address=email_address_input,password=password_input,login_choice=login_choice)
                            print("Your password is locked")
                            break
                        if no_of_attempts>0: continue
                        
            if no_of_attempts<=0:
                while(True):
                    password_reset_choice = input("Do you want to reset the password ? Yes/No : ")
                    if password_reset_choice.lower() == 'yes':
                        return password_resetter()
                    elif password_reset_choice.lower() == 'no':
                        exit()
                    else:
                        print("Enter input as yes or no")
                        continue

def password_resetter():
    
    email_address_input = ""
    while(True):
            email_address_input = input("Enter your Email ID : ")
            if SignUp.if_mail_already_exists(email_address_input)==True:
                break
            else:
                print("Email ID doesn't exist . Please enter the correct username")
                continue

    password_input = input("Please enter your new password : ")
    first_name_input = Db.first_names_db[Db.email_ids_db.index(email_address_input)]
    last_name_input = Db.last_names_db[Db.email_ids_db.index(email_address_input)]
    password_created = PasswordReset(first_name_input,last_name_input,password_input)
    
    while(True):

        if password_created.if_mix_of_char()==True:
            code = ""
            while(True):
                code = SignUp.email_code_generation()
                print(SignUp.email_code_sender(code,email_address_input))
                SignIn.countdown_creater()
                if SignIn.countdown_creater()==True:
                    no_of_attempts = 3
                    while(no_of_attempts>0):
                        code_input = input("Enter the verififcation PIN : ")
                        if SignUp.email_code_validator(code_input,code)==True:
                            break
                        else:
                            print(SignUp.email_code_validator(code_input,code))
                            print(f"Attempts remaining : {no_of_attempts}")
                            no_of_attempts = no_of_attempts-1
                            continue
                    else:
                        print("You have entered 3 incorrect code\nPlease try signing up after sometime.")
                else:
                    print(SignIn.countdown_creater())
                    loop_input = input("Do you want to continue with new code? Yes/No : ")
                    if loop_input.lower()=='yes':
                        continue
                    elif loop_input.lower()=='no':
                        print("Exiting...")
                        exit()
                break
        else:
            print(password_created.if_mix_of_char())
            password_input = input("Enter your password : ")
            password_created.update_temp_pwd(password_input)
            continue

        PasswordReset.password_reset_mail(email_address_input,password_input)

        while(True):
            user_sign_in_choice = input("Do you want to sign in to your account ? Yes/No : ")
            if user_sign_in_choice.lower() == 'yes':
                return signIn_performer
            elif user_sign_in_choice.lower() == 'no':
                return 'Password changed'
            else:
                print("Enter input as yes or no")
                continue

    

class Db:
    first_names_db = ["Mahendiran"]
    last_names_db = ["Sumithra"]
    user_names_db = ["Mahe@sumi",]
    email_ids_db = ["akns27022000@gmail.com",]
    passwords_db = ["P@wer951753Q2"]

    @classmethod
    def first_names_db_update(cls,first_name):
        Db.first_names_db.append(first_name)

    @classmethod
    def last_names_db_update(cls,last_name):
        Db.last_names_db.append(last_name)

    @classmethod
    def user_names_db_update(cls,username):
        Db.user_names_db.append(username)

    @classmethod
    def email_ids_db_update(cls,email_address):
        Db.email_ids_db.append(email_address)

    @classmethod
    def passwords_db_update(cls,password):
        Db.passwords_db.append(password)

class SignIn(Db):
    
    @classmethod
    def if_user_id_already_exists(cls,username):
        if username in Db.user_names_db:
            return True
        return False

    @staticmethod
    def countdown_creater():
        print("Verification code expires in 30 seconds")
        print("Enter Ctrl+c to enter the verification code")
        count = 30
        try:
            for i in range(count,0,-1):
                print(f"Countdown : 00:{i}",end = "\r",flush=True)
                time.sleep(1)
                if count == 0:
                    return "Code Expired"
        except KeyboardInterrupt:
            return True

class SignUp(Db):
    
    def __init__(self,first_name,last_name):
        self.first_name = first_name
        self.last_name = last_name

    def if_id_already_exists(self,username):
        if username in Db.user_names_db:
            return True
        return False

    @classmethod
    def if_mail_already_exists(self,email_address):
        if email_address in Db.email_ids_db:
            return True
        return False

    @staticmethod
    def email_validation(code):
        pass

    @staticmethod
    def email_code_generation():
        return random.randint(10001,99999)

    @staticmethod
    def email_code_sender(code,email_address):
        port = 465
        pwd = 'rukpwlqyhskdaelw'
        smtp_server = "smtp.gmail.com"
        sender_email = "tmptstng@gmail.com"  # Enter your address
        receiver_email = email_address  # Enter receiver address
        message = f'Your verification code is {code}'
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
            server.login(sender_email,pwd)
            server.sendmail(sender_email,receiver_email,message)

        return "Verification code sent to your EMAIL - ID"

    @staticmethod
    def email_code_validator(email_code_input,email_code_output):
        if email_code_output == int(email_code_input):
            return True
        return "PIN is incorrect"

class PasswordReset(SignUp,Db):

    def __init__(self, first_name, last_name,password):
        super().__init__(first_name, last_name)
        self.password = password
    
    # @staticmethod
    # def password_len_check(password):
    #     if len(password)>12:
    #         return True
    #     return False

    def if_mix_of_char(self):
        if self.password.lower().find(self.first_name.lower())==-1:
            if self.password.lower().find(self.last_name.lower())==-1:
                if len(self.password)>12:
                    if re.search("[a-z]",self.password):
                        if re.search("[A-Z]",self.password):
                            if re.search("[0-9]",self.password):
                                if re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(self.password):
                                    return True
                                else: return "Please add special characters in password"
                            else: return "Please add numbers in password"
                        else: return "Please add capital alphabets"
                    else: return "Please add small alphabets"
                else: return "Please type password more than 12 characters"
            else: return "Please don't use weak passwords , avoid using your name in passwords"
        else: return "Please don't use weak passwords , avoid using your name in passwords"

    def update_temp_pwd(self,password):
        self.password = password

    @classmethod
    def password_validate(cls,username=None,email_address=None,password=None,login_choice=None):

        if login_choice=='1':
            if password == Db.passwords_db[int(Db.user_names_db.index(username))]:
                return True
            else:
                return "Password is incorrect"
        
        if login_choice=='2':
            if password == Db.passwords_db[int(Db.email_ids_db.index(email_address))]:
                return True
            else:
                return "Password is incorrect"

    @classmethod
    def password_reset_mail(cls,email_address,password):
        
        Db.passwords_db[int(Db.email_ids_db.index(email_address))] = password

    @classmethod
    def password_lock(cls,username=None,email_address=None,password=None,login_choice=None):

        if login_choice=='1':
            Db.passwords_db[int(Db.user_names_db.index(username))] = "***"
        
        if login_choice=='2':
            Db.passwords_db[int(Db.email_ids_db.index(email_address))] = "***"


project_execution()








