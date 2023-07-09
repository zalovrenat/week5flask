from flask import render_template, request, redirect, url_for
from app import app
from .forms import PokemonSearch, LoginForm, SignUpForm
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user
import requests as r

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/favorite5')
def favorite5Page():

    favorite_pokemons = [{
        'name': 'Arceus',
        # 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/493.gif'
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/493.png'
    },{
        'name': 'Charizard',
        # 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif'
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png'
    },{
        'name': 'Mew Two',
        # 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/150.gif'
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png'
    },{
        'name': 'Rayquaza',
        # 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/384.gif'
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/384.png'
    },{
        'name': 'Snorlax',
        # 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/143.gif'
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png'
    }]

    return render_template('favorite5.html', favorite_pokemons = favorite_pokemons)

def get_pokemon_info(pokemon_name):
    message = None
    res = r.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if res.ok:
        data = res.json()
        pokemon_data = dict()
        pokemon_data['abilities'] = dict()
        pokemon_data['name'] = data['forms'][0]['name'].title()
        i = 1
        for ability in data['abilities']:
            pokemon_data['abilities']['Ability ' + str(i)] = ability['ability']['name']
            i += 1
        i = 1
        pokemon_data['base experience'] = data['base_experience']
        pokemon_data['img'] = data['sprites']['other']['official-artwork']['front_default']
        pokemon_data['attack base stat'] = data['stats'][1]['base_stat']
        pokemon_data['hp base stat'] = data['stats'][0]['base_stat']
        pokemon_data['defense base stat'] = data['stats'][2]['base_stat']
        return pokemon_data
    else:
        print('That is not a valid pokemon name. Please see a list of pokemon names here:\nhttps://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number')

@app.route('/pokemon', methods=['GET','POST'])
def pokemonSearch():
    poke_data = dict()
    form = PokemonSearch()
    message = None
    message_link = None
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokename.data
            poke_data = get_pokemon_info(pokemon.lower())

            if not poke_data:
                message = 'That is not a valid pokemon name. Please see a list of pokemon names here:'
                message_link = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
    
    return render_template('pokemon.html', form=form, pokemon_data=poke_data, message=message, message_link=message_link)

@app.route('/login', methods=['GET','POST'])
def loginPage():
    form = LoginForm()
    message = None
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            # check if user is in database
            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    message = 'Incorrect password.'
                    print('Incorrect password.')
            else:
                message = 'The username does not exist'
                print('The username does not exist')

    return render_template('login.html', form=form, message=message)

@app.route('/signup', methods=['GET','POST'])
def signUpPage():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            # add user to database
            user = User(username,email,password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('loginPage'))
    
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('loginPage'))