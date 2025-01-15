from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    
    path('', views.main_redirect, name='main_redirect'), #main_redirect
    path('home/', views.main, name='main'), #home page
    path('pokemon/', views.pokemon, name='pokemon'), #pokemon page
    path('pokemon/details/<int:id>/', views.poke_details, name='poke_details'), #pokemon details
    path('moves/', views.moves, name='moves'),  #moves
    path('moves/<int:id>/', views.move_details, name='move_details'), #move details
    path('community/', views.community, name='community'), #community
    path('teams/', views.teams, name='teams'), #teams
    path('teams/details/<int:id>/', views.teams_details, name='teams_details'), #team details
    path('teams/create_team/', views.create_team, name='create_team'), #create team
    path('teams/details/<int:id>/delete_team/', views.delete_team, name='delete_team'), #delete team
    path('teams/details/<int:id>/update_team/', views.update_team, name='update_team'), #update team
    path('teams/details/<int:id>/export_team_json/', views.export_team_json, name='export_team_json'), #export team json
    path('teams/details/<int:id>/export_team_csv/', views.export_team_csv, name='export_team_csv'), #export team csv
    path('teams/details/<int:id>/export_team_pokemon_showdown/', views.export_team_pokemon_showdown, name='export_team_pokemon_showdown'), #export team pokemon showdown
    path('get_pokemon_data/<int:pokemon_id>/', views.get_pokemon_data, name='get_pokemon_data'), #get pokemon data
    path('testing/', views.testing, name='testing'), #testing
    path('accounts/login/', views.login_redirect, name='login_redirect'), #login
    path('profile/', views.profile, name='profile'), #profile
    path('profile/delete_profile/', views.delete_profile, name='delete_profile'), #delete profile
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'), #edit profile
    path('login/', views.login_page, name='login'), #login
    path('register/',views.register_page, name='register'), #register
    path('logout/', views.logout_page, name='logout'), #logout

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',   
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

         path('admin/', admin.site.urls), #admin
]