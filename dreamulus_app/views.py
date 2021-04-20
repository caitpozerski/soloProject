from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Dream




#------LOGIN/REG MAIN PAGE-----
def index(request):
    return render(request, "main.html")


#-----CREATE USER/REGISTER-----
def create_user(request):
    if request.method =="POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            # add in profile picture???
            request.session['user_id'] = user.id # matches variable on line 25
            return redirect('/') # or return redirect('/dreams')
    return redirect('/')


#-----LOGIN-----
def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id 
                return redirect('/dreams') 
        messages.error(request, "Email or password are incorrect")
    return redirect('/')

#-----DREAM DASH-----
def dreams(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_dreams': Dream.objects.all(),
    }
    return render(request, "dashboard.html", context)


#-----CREATE A DREAM-----
def create_dream(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Dream.objects.create_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dreams')
        else:
            dream = Dream.objects.create(title=request.POST['title'], description=request.POST['description'], owner = User.objects.get(id=request.session['user_id']))
            request.session['dream_id'] = dream.id
            messages.success(request, "Dream created")
            return redirect('/dreams')
    return redirect('/dreams')


#-----SHOW ONE DREAM-----
def one_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =="GET":
        context = {
            'one_dream': Dream.objects.get(id=dream_id)
        }
    return render(request, "one_dream.html", context)



#-----EDIT ONE DREAM-----
def edit_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =="GET":
        context = {
            'one_dream': Dream.objects.get(id=dream_id)
        }
        return render(request, "edit_dream.html", context)


#-----UPDATE DREAM-----
def update_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =="POST":
        dream_to_update = Dream.objects.get(id=dream_id)
        dream_to_update.title = request.POST['title']
        dream_to_update.description = request.POST['description']
        dream_to_update.save()
    # return redirect(f"users/dreams/edit/{dream_id}")
    return redirect('/dreams')



#-----DELETE ONE DREAM------
def delete_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        dream_to_delete = Dream.objects.get(id=dream_id)
        if dream_to_delete.owner.id == request.session['user_id']:
            dream_to_delete.delete()
    return redirect('/dreams')



#-----MY JOURNAL------
def journal(request):
    if 'user_id' not in request.session:
        return redirect('/')
    # can we reference this context object in another method??
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_dreams': Dream.objects.all(), 
        # 'my_dreams': User.objects.all() - re watch giraffes course
    }
    return render(request, "journal.html", context)


#-----LIKE DREAM------
def like_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        one_like = Dream.objects.get(id=dream_id)
        current_user = User.objects.get(id=request.session['user_id'])
        one_like.users_that_liked.add(current_user)
    return redirect('/dreams')


#-----UNLIKE DREAM-----
def unlike_dream(request, dream_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        one_like = Dream.objects.get(id=dream_id)
        current_user = User.objects.get(id=request.session['user_id'])
        one_like.users_that_liked.remove(current_user)
    return redirect('/dreams')


#-----ACCOUNT INFO-----
def account(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # return render(request, "account.html")
    # if request.method =="GET":
    context = {
        'one_user': User.objects.get(id=user_id)
    }
    return render(request, "account.html", context)


#-----UPDATE ACCOUNT INFO------
def update_account(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =="POST":
        print('how about here?')
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/users/account/{user_id}')
            print('how about here?')
        else:
            user_to_update = User.objects.get(id=user_id)
            user_to_update.first_name = request.POST['first_name']
            user_to_update.last_name = request.POST['last_name']
            user_to_update.email = request.POST['email']
            user_to_update.password = request.POST['password']
            user_to_update.save()
            messages.success(request, "Account has been updated")
        # return redirect('/users/account/<int:user_id>')
        return redirect(f'/users/account/{user_id}')
    return redirect('/dreams')




    #         password = request.POST['password']
    #         pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    #         user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
    #         # add in profile picture???
    #         request.session['user_id'] = user.id # matches variable on line 25
    #         return redirect('/') # or return redirect('/dreams')
    # return redirect('/')
    
    
    # olddddddd
    # if request.method =="POST":
    #     errors = User.objects.create_validator(request.POST)
    #     if len(errors) > 0:
    #         for key, value in errors.items():
    #             messages.error(request, value)
    #         # return redirect('/users/account/<int:user_id>')
    #         return redirect('/users/account/{f'{'user_id'}')
    #     else: 
    #         user_to_update = User.objects.get(id=user_id)
    #         user_to_update.first_name = request.POST['first_name']
    #         user_to_update.last_name = request.POST['last_name']
    #         user_to_update.email = request.POST['email']
    #         user_to_update.password = request.POST['password']
    #         user_to_update.save()
    #         messages.success(request, "Account has been updated")
    #     # return redirect('/users/account/<int:user_id>')
    #     return redirect('/users/account/{f'{'user_id'}')
    # return redirect('/dreams')






#-----LOGOUT------
def logout(request):
    request.session.flush()
    return redirect('/')