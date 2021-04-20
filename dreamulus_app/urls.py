from django.urls import path
from .import views

urlpatterns = [
    # localhost:8000 --main splash page 
    path('', views.index),
    # localhost:8000 -- create a user
    path('users/create', views.create_user),
    # localhost:8000 -- login
    path('users/login', views.login),
    # localhost:8000/dreams -- dreams
    path('dreams', views.dreams),
    # localhost:8000 -- create a dream
    path('dreams/create', views.create_dream),
    # localhost:8000 -- show one dream
    path('users/dreams/<int:dream_id>', views.one_dream),
    # localhost:8000/users/dreams/edit/<int:dream_id> --- edit a dream
    path('users/dreams/edit/<int:dream_id>', views.edit_dream),
    # localhost:8000/users/dreams/update/<int:dream_id> --- update a dream
    path('users/dreams/update/<int:dream_id>', views.update_dream),
    # localhost:8000 -- delete one dream
    path('dreams/delete/<int:dream_id>', views.delete_dream),
    # localhost:8000/dreams/like
    path('dreams/like/<int:dream_id>', views.like_dream),
    # localhost:8000/dreams/unlike
    path('dreams/unlike/<int:dream_id>', views.unlike_dream),
    # localhost:8000/journal
    path('users/journal', views.journal),
    # localhost:8000/users/account
    path('users/account/<int:user_id>', views.account),
    # localhost:8000/users/update
    path('users/update/<int:user_id>', views.update_account),
    # localhost:8000/logout -- logout
    path('logout', views.logout),
]