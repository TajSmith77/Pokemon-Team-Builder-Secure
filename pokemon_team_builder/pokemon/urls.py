from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.main_redirect, name='main_redirect'),
    path('home/', views.main, name='main'),
    path('pokemon/', views.pokemon, name='pokemon'),
    path('pokemon/details/<int:id>/', views.poke_details, name='poke_details'),
    path('moves/', views.moves, name='moves'),  
    path('moves/<int:id>/', views.move_details, name='move_details'),
    path('community/', views.community, name='community'),
    path('teams/', views.teams, name='teams'),
    path('teams/details/<int:id>/', views.teams_details, name='teams_details'),
    path('teams/create_team/', views.create_team, name='create_team'),
    path('teams/details/<int:id>/delete_team/', views.delete_team, name='delete_team'),
    path('teams/details/<int:id>/update_team/', views.update_team, name='update_team'),
    path('teams/details/<int:id>/export_team_json/', views.export_team_json, name='export_team_json'),
    path('teams/details/<int:id>/export_team_csv/', views.export_team_csv, name='export_team_csv'),
    path('teams/details/<int:id>/export_team_pokemon_showdown/', views.export_team_pokemon_showdown, name='export_team_pokemon_showdown'),
    path('get_pokemon_data/<int:pokemon_id>/', views.get_pokemon_data, name='get_pokemon_data'),
    path('testing/', views.testing, name='testing'),
    path('accounts/login/', views.login_redirect, name='login_redirect'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete_profile/', views.delete_profile, name='delete_profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.login_page, name='login'),
    path('register/',views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('admin/', admin.site.urls),
]