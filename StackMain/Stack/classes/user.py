import uuid
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import re
import uuid

# import capstoneMain.ToolOwnershipTracker.models
from Stack.models import user


class userClass:
    # if role does not work, change 'U' to UserType.User
    def createUser(
        self,
        firstName,
        lastName,
        email,
        password,
        confirmPassword
    ):
        if userClass.verifyInformationRequirements(self, firstName, lastName, email):
            if userClass.verifyPasswordRequirements(self, password, confirmPassword):
                hashPass = userClass.hashPass(password)
                newUser = user(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=hashPass,
                    forget_password_token=hashPass,
                )
                newUser.save()

    def verifyInformationRequirements(self, firstName, lastName, email):
        if firstName is None:
            raise Exception("First name may not be left blank!")
        if lastName is None:
            raise Exception("Last name may not be left blank!")
        if email is None:
            raise Exception("Email may not be left blank!")
        test = list(map(str, user.objects.filter(email=email)))
        if len(test) != 0:
            raise Exception("User already exists!")
        else:
            return True

    def verifyPasswordRequirements(self, password, confirmPassword):
        if len(password) < 12:
            raise Exception("Password must be at least 12 characters!")
        if not re.search("!|@|#|$|%|^|&|\\*|\\(|\\)|_|\\+|-|=", password):
            raise Exception("Password must contain a symbol!")
        tempUpper = False
        tempLower = False
        tempDigit = False
        for letter in password:
            if letter.isupper():
                tempUpper = True
            if letter.islower():
                tempLower = True
            if letter.isdigit():
                tempDigit = True
        if not tempUpper:
            raise Exception("Password must contain an uppercase letter!")
        if not tempLower:
            raise Exception("Password must contain a lowercase letter!")
        if not tempDigit:
            raise Exception("Password must contain a number!")
        if password != confirmPassword:
            raise Exception("Passwords do not match!")
        return True
    
    def hashPass(password):
        return hashlib.md5(password.encode("utf-8")).hexdigest()
    
    def processPasswordResetRequest(email):
        try:
            test = list(map(str, user.objects.filter(email=email)))
        except Exception as e:
            print(e)
            raise Exception("Email is not valid!")

        token = str(uuid.uuid4())
        tempUser = user.objects.get(email=email)
        tempUser.forget_password_token = token
        tempUser.save()

        userClass.sendForgotPasswordMail(email, token)
        return True
    
    def sendForgotPasswordMail(email, token):
        subject = "Your password reset link"
        message = f"Hello, click the following link to be redirected to form to reset your password: https://{token}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return True
    
    def verifyPasswordResetToken(self, email, token):
        try:
            user = user.objects.get(email=email)
            return user.forget_password_token == token
        except user.DoesNotExist:
            return False
        
    def changePassword(self, email, password, confirmPassword):
        try:
            test = list(map(str, user.objects.filter(email=email)))
        except:
            raise Exception("Email is not valid!")

        tempUser = user.objects.get(email=email)
        if userClass.verifyPasswordRequirements(tempUser, password, confirmPassword):
            self.password = userClass.hashPass(password)
            tempUser.forget_password_token = ""
            tempUser.save()
            return True
