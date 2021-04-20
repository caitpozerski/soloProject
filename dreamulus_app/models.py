from django.db import models
import re


#-----USER-----
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"        
        if len(reqPOST['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"        
        if len(reqPOST['email']) < 6: 
            errors['email'] = "Email must be at least 8 characters"
        if len(reqPOST['email']) == 0:
            errors['email'] = "You must enter an email"        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email is not in correct format"
        # No Duplicate Emails: 
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email has been used, please use another"        
        if len(reqPOST['password']) < 8: 
            errors['password'] = "Password must be at least 8 characters long"        
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['match'] = "Password and password confirmation do not match"        
        return errors

    def edit_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"        
        if len(reqPOST['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"        
        if len(reqPOST['email']) < 6: 
            errors['email'] = "Email must be at least 8 characters"
        if len(reqPOST['email']) == 0:
            errors['email'] = "You must enter an email"        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email is not in correct format"
        if len(reqPOST['password']) < 8: 
            errors['password'] = "Password must be at least 8 characters long"        
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['match'] = "Password and password confirmation do not match"        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.TextField()
    password = models.TextField()
    # profile_pic = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 


#------DREAM------
class DreamManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) <= 1:
            errors['title'] = "Title name is required" 
        if len(reqPOST['description']) == 0:
            errors['description'] = "Description is required"
        if len(reqPOST['description']) < 10:
            errors['description'] = "Description should be more than 10 characters"
        # dream_with_title = Dream.objects.filter(org_name=reqPOST['org_name'])
        # if len(dream_with_title) >= 1:
        #     errors['dup'] = "Title has been taken, please use another"  
        return errors 


class Dream(models.Model):
    title = models.TextField()
    description = models.TextField()
    owner = models.ForeignKey(User, related_name="dreams_owned", on_delete=models.CASCADE)
    users_that_liked = models.ManyToManyField(User, related_name="dream_user_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DreamManager()


