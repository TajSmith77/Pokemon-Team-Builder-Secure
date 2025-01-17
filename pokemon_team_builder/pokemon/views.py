from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from .models import *
from .forms import *
import csv
import json

def pokemon(request):
    mypokemon = Pokemon.objects.all().prefetch_related('types', 'moves', 'abilities')
    all_types = Type.objects.all()
    all_abilities = Ability.objects.all()
    all_moves = Move.objects.all()

    #Filtering
    filter_visible = request.GET.get('filter_visible', False)
    pokedex_number_query = request.GET.get('pokedex_number')
    if pokedex_number_query:
        mypokemon = mypokemon.filter(id=pokedex_number_query)

    name_query = request.GET.get('poke_name')
    if name_query:
        name_query = name_query.strip().lower()
        mypokemon = mypokemon.filter(name__istartswith=name_query)

    type_query = request.GET.get('type')
    if type_query:
        mypokemon = mypokemon.filter(types__id=type_query)

    ability_query = request.GET.get('ability')
    if ability_query:
        mypokemon = mypokemon.filter(abilities__id=ability_query)

    move_query = request.GET.get('move')
    if move_query:
        mypokemon = mypokemon.filter(moves__id=move_query)

    hp_query = request.GET.get('min_hp')
    if hp_query:
        mypokemon = mypokemon.filter(hp__gte=hp_query)

    attack_query = request.GET.get('min_attack')
    if attack_query:
        mypokemon = mypokemon.filter(attack__gte=attack_query)

    defense_query = request.GET.get('min_defense')
    if defense_query:
        mypokemon = mypokemon.filter(defense__gte=defense_query)

    special_attack_query = request.GET.get('min_special_attack')
    if special_attack_query:
        mypokemon = mypokemon.filter(special_attack__gte=special_attack_query)

    special_defense_query = request.GET.get('min_special_defense')
    if special_defense_query:
        mypokemon = mypokemon.filter(special_defense__gte=special_defense_query)

    speed_query = request.GET.get('min_speed')
    if speed_query:
        mypokemon = mypokemon.filter(speed__gte=speed_query)

    #Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by:
        sort_by = sort_by.strip()
        if sort_by == 'name':
            mypokemon = mypokemon.order_by('name')
        if sort_by == 'id':
            mypokemon = mypokemon.order_by('id')

    #Pagination
    per_page = int(request.GET.get('per_page', 50))
    paginator = Paginator(mypokemon, per_page)
    page_number = request.GET.get('page')
    poke_page = paginator.get_page(page_number)
    template = loader.get_template('all_pokemon.html')
    context = {
        'mypokemon': mypokemon,
        'poke_page': poke_page,
        'per_page': per_page,
        'name_query': name_query,
        'pokedex_number_query': pokedex_number_query,
        'type_query': type_query,
        'ability_query': ability_query,
        'move_query': move_query,
        'hp_query': hp_query,
        'attack_query': attack_query,
        'defense_query': defense_query,
        'special_attack_query': special_attack_query,
        'special_defense_query': special_defense_query,
        'speed_query': speed_query,
        'sort_by': sort_by,
        'all_types': all_types,
        'all_abilities': all_abilities,
        'all_moves': all_moves,
        'filter_visible': filter_visible
    }
    return HttpResponse(template.render(context, request))

def poke_details(request, id):
    mypokemon = Pokemon.objects.get(id=id)
    template = loader.get_template('poke_details.html')
    context = {
        'mypokemon': mypokemon,

    }
    return HttpResponse(template.render(context, request))

def moves(request):
    mymove = Move.objects.all()
    form = MoveFilterForm()
    name_query = request.GET.get('move_name')
    if name_query:
        print(name_query)
        name_query = name_query.strip().lower()
        mymove = mymove.filter(id=name_query)
    type_query = request.GET.get('move_type')
    if type_query:
        mymove = mymove.filter(type=type_query)
    min_damage_query = request.GET.get('min_damage')
    if min_damage_query:
        mymove = mymove.filter(power__gte=min_damage_query)
    per_page = int(request.GET.get('per_page', 50))
    paginator = Paginator(mymove, per_page)
    page_number = request.GET.get('page')
    move_page = paginator.get_page(page_number)
    template = loader.get_template('moves.html')
    context = {
        'mymove': mymove,
        'move_page': move_page,
        'per_page': per_page,
        'name_query': name_query,
        'type_query': type_query,
        'min_damage_query': min_damage_query,
        'form': form
    }
    return HttpResponse(template.render(context, request))
def move_details(request, id):
    mymove = Move.objects.get(id=id)
    template = loader.get_template('move_details.html')
    context = {
        'mymove': mymove
    }
    return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  context = {
      
  }
  return HttpResponse(template.render(context, request))

def main_redirect(request):
  return redirect('/home/')

 
# login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        # Authenticate the user with the provided username and password
        user = authenticate(request=request, username=username, password=password)
         
        if user is None:
            # Display an error message if authentication fails
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/')
     
    # Render the login page template (GET request)
    return render(request, 'login.html')

def login_redirect(request):
    return redirect('/login/')
 
# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
         
        # Check if a user with the provided username already exists 
        if User.objects.filter(username=username).exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
         
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            # Display an information message if the email is taken
            messages.info(request, "Email already taken!")
            return redirect('/register/')
        
        #Password validation
        try:
            validate_password(password)
        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
            return redirect('/register/')
         
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
         
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
         
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
     
    # Render the registration page template (GET request)
    return render(request, 'register.html')


@login_required
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('/login/') # Redirect to the login page upon pass

@login_required
def profile(request):
  template = loader.get_template('profile.html')
  context = {
      
  }
  return HttpResponse(template.render(context, request))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile edited successfully!")
            return redirect('/profile/')
    else:
        form = UserEditForm(instance=request.user)
    template = loader.get_template('edit_profile.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

@login_required
def delete_profile(request):
    if request.method == "POST":
        form = UserDeleteForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/profile/delete_profile/')
         
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
         
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/profile/delete_profile/')
        else:
            # Delete the user
            if user.username == request.user.username:
                user.delete()
                messages.info(request, "Profile deleted successfully!")
                return redirect('/login/')
            else:
                messages.error(request, "You can only delete your own profile!")
    return render(request, 'delete_profile.html')



@login_required
def teams(request):
  myteams = Team.objects.filter(owner=request.user)
  template = loader.get_template('teams.html')
  context = {
      'myteams': myteams
  }
  return HttpResponse(template.render(context, request))

def teams_details(request, id):
  myteam = Team.objects.get(id=id)
  template = loader.get_template('teams_details.html')
  context = {
      'myteam': myteam
  }
  return HttpResponse(template.render(context, request))

def community(request):
  myteams = Team.objects.all().filter(is_public=True)
  template = loader.get_template('community.html')
  context = {
      'myteams': myteams
  }
  return HttpResponse(template.render(context, request))

def create_team(request):
  all_pokemon = Pokemon.objects.all().prefetch_related('abilities', 'moves')
  all_abilities = Ability.objects.all().prefetch_related('pokemon')
  all_moves = Move.objects.all().prefetch_related('pokemon')

  if request.method == 'POST':
      form = TeamForm(request.POST)
      if form.is_valid():
          team = form.save(commit=False)
          team.owner = request.user
          team.save()
          
          return redirect(f'/teams/details/{team.id}')
  else:
      form = TeamForm()
      context = {
          'form': form,
          'all_pokemon': all_pokemon,
          'all_abilities': all_abilities,
          'all_moves': all_moves

      }
  template = loader.get_template('create_team.html')

 
  return HttpResponse(template.render(context, request))

def update_team(request, id):
  myteam = get_object_or_404(Team, id=id, owner=request.user)
  all_pokemon = Pokemon.objects.all().prefetch_related('abilities', 'moves')
  all_abilities = Ability.objects.all().prefetch_related('pokemon')
  all_moves = Move.objects.all().prefetch_related('pokemon')
  if request.method == 'POST':
      form = TeamForm(request.POST, instance=myteam)
      if form.is_valid():
          form.save()
          return redirect(f'/teams/details/{id}')
  else:
      form = TeamForm(instance=myteam)
      context = {
          'form': form,
          'all_pokemon': all_pokemon,
          'all_abilities': all_abilities,
          'all_moves': all_moves
        }
  template = loader.get_template('update_team.html')
 
  return HttpResponse(template.render(context, request))

def delete_team(request, id):
  myteam = get_object_or_404(Team, id=id, owner=request.user)
  if request.method == 'POST':
    myteam.delete()
    return redirect('teams')
  return redirect('teams')

def get_pokemon_data(request, pokemon_id):
  try:  
    pokemon = Pokemon.objects.get(id=pokemon_id)
    abilities = Ability.objects.filter(pokemon=pokemon).values('id','name')
    moves = Move.objects.filter(pokemon=pokemon).values('id','name')
    pokemon_data = {
        'name': pokemon.name,
        'abilities': list(abilities),
        'moves': list(moves)
        }
    return JsonResponse({'pokemon_data': pokemon_data})
  
  except Pokemon.DoesNotExist:
    return JsonResponse({'error': 'Pokemon not found'}, status=404)
  
def export_team_json(request, id):
  myteam = get_object_or_404(Team, id=id, owner=request.user)
  team_data = {
      'team_name': myteam.name,
      'pokemon1': {
          'name': myteam.pokemon1.name,
      },
      'ability1': {
          'name': myteam.ability1.name
      },
      'move1_1': {
          'name': myteam.move1_1.name,
          'type': {
              'name': myteam.move1_1.type.name
          },
          'power': myteam.move1_1.power,
          'accuracy': myteam.move1_1.accuracy,
          'pp': myteam.move1_1.pp
      },
      'move1_2': {
          'name': myteam.move1_2.name,
          'type': {
              'name': myteam.move1_2.type.name
          },
          'power': myteam.move1_2.power,
          'accuracy': myteam.move1_2.accuracy,
          'pp': myteam.move1_2.pp
      },
      'move1_3': {
          'name': myteam.move1_3.name,
          'type': {
              'name': myteam.move1_3.type.name
          },
          'power': myteam.move1_3.power,
          'accuracy': myteam.move1_3.accuracy,
          'pp': myteam.move1_3.pp
      },
      'move1_4': {
          'name': myteam.move1_4.name,
          'type': {
              'name': myteam.move1_4.type.name
          },
          'power': myteam.move1_4.power,
          'accuracy': myteam.move1_4.accuracy,
          'pp': myteam.move1_4.pp
      },
      'pokemon2': {
          'name': myteam.pokemon2.name,
      },
      'ability2':{
          'name': myteam.ability2.name
      },
      'move2_1': {
          'name': myteam.move2_1.name,
          'type': {
              'name': myteam.move2_1.type.name
          },
          'power': myteam.move2_1.power,
          'accuracy': myteam.move2_1.accuracy,
          'pp': myteam.move2_1.pp
      },
      'move2_2': {
          'name': myteam.move2_2.name,
          'type': {
              'name': myteam.move2_2.type.name
          },
          'power': myteam.move2_2.power,
          'accuracy': myteam.move2_2.accuracy,
          'pp': myteam.move2_2.pp
      },
      'move2_3': {
          'name': myteam.move2_3.name,
          'type': {
              'name': myteam.move2_3.type.name
          },
          'power': myteam.move2_3.power,
          'accuracy': myteam.move2_3.accuracy,
          'pp': myteam.move2_3.pp
      },
      'move2_4': {
          'name': myteam.move2_4.name,
          'type': {
              'name': myteam.move2_4.type.name
          },
          'power': myteam.move2_4.power,
          'accuracy': myteam.move2_4.accuracy,
          'pp': myteam.move2_4.pp
      },
      'pokemon3': {
          'name': myteam.pokemon3.name, 
      },
      'ability3': {
          'name': myteam.ability3.name
      },
      'move3_1': {
          'name': myteam.move3_1.name,
          'type': {
              'name': myteam.move3_1.type.name
          },
          'power': myteam.move3_1.power,
          'accuracy': myteam.move3_1.accuracy,
          'pp': myteam.move3_1.pp
      },
      'move3_2': {
          'name': myteam.move3_2.name,
          'type': {
              'name': myteam.move3_2.type.name
          },
          'power': myteam.move3_2.power,
          'accuracy': myteam.move3_2.accuracy,
          'pp': myteam.move3_2.pp
      },
      'move3_3': {
          'name': myteam.move3_3.name,
          'type': {
              'name': myteam.move3_3.type.name
          },
          'power': myteam.move3_3.power,
          'accuracy': myteam.move3_3.accuracy,
          'pp': myteam.move3_3.pp
      },
      'move3_4': {
          'name': myteam.move3_4.name,
          'type': {
              'name': myteam.move3_4.type.name
          },
          'power': myteam.move3_4.power,
          'accuracy': myteam.move3_4.accuracy,
          'pp': myteam.move3_4.pp
      },
      'pokemon4': {
          'name': myteam.pokemon4.name,
      },
      'ability4': {
          'name': myteam.ability4.name
      },
      'move4_1': {
          'name': myteam.move4_1.name,
          'type': {
              'name': myteam.move4_1.type.name
          },
          'power': myteam.move4_1.power,
          'accuracy': myteam.move4_1.accuracy,
          'pp': myteam.move4_1.pp
      },
      'move4_2': {
          'name': myteam.move4_2.name,
          'type': {
              'name': myteam.move4_2.type.name
          },
          'power': myteam.move4_2.power,
          'accuracy': myteam.move4_2.accuracy,
          'pp': myteam.move4_2.pp
      },
      'move4_3': {
          'name': myteam.move4_3.name,
          'type': {
              'name': myteam.move4_3.type.name
          },
          'power': myteam.move4_3.power,
          'accuracy': myteam.move4_3.accuracy,
          'pp': myteam.move4_3.pp
      },
      'move4_4': {
          'name': myteam.move4_4.name,
          'type': {
              'name': myteam.move4_4.type.name
          },
          'power': myteam.move4_4.power,
          'accuracy': myteam.move4_4.accuracy,
          'pp': myteam.move4_4.pp
      },
      'pokemon5': {
          'name': myteam.pokemon5.name,
      },
      'ability5': {
          'name': myteam.ability5.name
      },
      'move5_1': {
          'name': myteam.move5_1.name,
          'type': {
              'name': myteam.move5_1.type.name
          },
          'power': myteam.move5_1.power,
          'accuracy': myteam.move5_1.accuracy,
          'pp': myteam.move5_1.pp
      },
      'move5_2': {
          'name': myteam.move5_2.name,
          'type': {
              'name': myteam.move5_2.type.name
          },
          'power': myteam.move5_2.power,
          'accuracy': myteam.move5_2.accuracy,
          'pp': myteam.move5_2.pp
      },
      'move5_3': {
          'name': myteam.move5_3.name,
          'type': {
              'name': myteam.move5_3.type.name
          },
          'power': myteam.move5_3.power,
          'accuracy': myteam.move5_3.accuracy,
          'pp': myteam.move5_3.pp
      },
      'move5_4': {
          'name': myteam.move5_4.name,
          'type': {
              'name': myteam.move5_4.type.name
          },
          'power': myteam.move5_4.power,
          'accuracy': myteam.move5_4.accuracy,
          'pp': myteam.move5_4.pp
      },
      'pokemon6': {
          'name': myteam.pokemon6.name,
      },
      'ability6': {
          'name': myteam.ability6.name
      },
      'move6_1': {
          'name': myteam.move6_1.name,
          'type': {
              'name': myteam.move6_1.type.name
          },
          'power': myteam.move6_1.power,
          'accuracy': myteam.move6_1.accuracy,
          'pp': myteam.move6_1.pp
      },
      'move6_2': {
          'name': myteam.move6_2.name,
          'type': {
              'name': myteam.move6_2.type.name
          },
          'power': myteam.move6_2.power,
          'accuracy': myteam.move6_2.accuracy,
          'pp': myteam.move6_2.pp
      },
      'move6_3': {
          'name': myteam.move6_3.name,
          'type': {
              'name': myteam.move6_3.type.name
          },
          'power': myteam.move6_3.power,
          'accuracy': myteam.move6_3.accuracy,
          'pp': myteam.move6_3.pp
      },
      'move6_4': {
          'name': myteam.move6_4.name,
          'type': {
              'name': myteam.move6_4.type.name
          },
          'power': myteam.move6_4.power,
          'accuracy': myteam.move6_4.accuracy,
          'pp': myteam.move6_4.pp
      }
  }


  team_json = json.dumps(team_data)

  return HttpResponse(team_json, content_type='application/json')

def export_team_csv(request, id):
  myteam = get_object_or_404(Team, id=id, owner=request.user)
  team_data = {
      'name': myteam.name,
      'pokemon1': myteam.pokemon1,
      'ability1': myteam.ability1,
      'move1_1': myteam.move1_1,
      'move1_2': myteam.move1_2,
      'move1_3': myteam.move1_3,
      'move1_4': myteam.move1_4,
      'pokemon2': myteam.pokemon2,
      'ability2': myteam.ability2,
      'move2_1': myteam.move2_1,
      'move2_2': myteam.move2_2,
      'move2_3': myteam.move2_3,
      'move2_4': myteam.move2_4,
      'pokemon3': myteam.pokemon3,
      'ability3': myteam.ability3,
      'move3_1': myteam.move3_1,
      'move3_2': myteam.move3_2,
      'move3_3': myteam.move3_3,
      'move3_4': myteam.move3_4,
      'pokemon4': myteam.pokemon4,
      'ability4': myteam.ability4,
      'move4_1': myteam.move4_1,
      'move4_2': myteam.move4_2,
      'move4_3': myteam.move4_3,
      'move4_4': myteam.move4_4,
      'pokemon5': myteam.pokemon5,
      'ability5': myteam.ability5,
      'move5_1': myteam.move5_1,
      'move5_2': myteam.move5_2,
      'move5_3': myteam.move5_3,
      'move5_4': myteam.move5_4,
      'pokemon6': myteam.pokemon6,
      'ability6': myteam.ability6,
      'move6_1': myteam.move6_1,
      'move6_2': myteam.move6_2,
      'move6_3': myteam.move6_3,
      'move6_4': myteam.move6_4,
    }
  filename = f'{myteam.name}_team.csv'  
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = f'attachment; filename="{filename}"'
  writer = csv.writer(response)
  writer.writerow(team_data.keys())
  writer.writerow(team_data.values())
  return response

def export_team_pokemon_showdown(request, id):
    myteam = get_object_or_404(Team, id=id, owner=request.user)
    showdown_team = ""
    for i in range(1, 7):
        pokemon = myteam.__getattribute__(f'pokemon{i}')
        if pokemon:
            showdown_team += f'{pokemon.name}\n'

            ability = myteam.__getattribute__(f'ability{i}')
            if ability:
                    showdown_team += f'Ability: {ability.name}\n'

            for j in range(1, 5):
                move = myteam.__getattribute__(f'move{i}_{j}')
                if move:
                    showdown_team += f'- {move.name}\n'

            showdown_team += '\n'
    print(showdown_team)
    response = HttpResponse(showdown_team, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{myteam.name}_team.txt"'
    return response
        
  

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))