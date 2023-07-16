from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import PokemonSearch, LoginForm, SignUpForm
from .models import User, db, Pokedex, PokedexPokemon, Pool, PoolPokemon, Pokemon
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
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
    res = r.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if res.ok:
        data = res.json()
        pokemon_data = dict()
        pokemon_data['pokemon #'] = data['id']
        pokemon_data['name'] = data['forms'][0]['name'].title()
        pokemon_data['abilities'] = dict()
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

@app.route('/pokemon', methods=['GET','POST'])
def pokemonSearch():
    global global_pokemon_data
    poke_data = dict()
    form = PokemonSearch()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokename.data
            poke_data = get_pokemon_info(pokemon.lower())
            print(poke_data)
            global_pokemon_data = poke_data
            if Pokemon.query.filter_by(pokemon_id=poke_data['pokemon #']).first():
                pass
            elif len(poke_data['abilities']) > 1:
                addPokemon = Pokemon(poke_data['pokemon #'],poke_data['name'],poke_data['img'],poke_data['abilities']['Ability 1'],poke_data['abilities']['Ability 2'],poke_data['base experience'],poke_data['hp base stat'],poke_data['attack base stat'],poke_data['defense base stat'])
                db.session.add(addPokemon)
                db.session.commit()
            else:
                addPokemon = Pokemon(poke_data['pokemon #'],poke_data['name'],poke_data['img'],poke_data['abilities']['Ability 1'],None,poke_data['base experience'],poke_data['hp base stat'],poke_data['attack base stat'],poke_data['defense base stat'])
                db.session.add(addPokemon)
                db.session.commit()

            if not poke_data:
                flash('That is not a valid pokemon name. Please see a list of valid pokemon names ','warning')
    
    return render_template('pokemonsearch.html', form=form, pokemon_data=poke_data)

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
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Successfuly logged in.', 'success')
                    return redirect(url_for('homePage'))
                else:
                    flash('Incorrect password.', 'danger')
            else:
                flash('The username does not exist.', 'danger')
        else:
            flash('An error has ocurred. PLease submit a valid form.', 'danger')

    return render_template('login.html', form=form, message=message)

def username_in_db(username):
    return User.query.filter_by(username=username).first()

def email_in_db(email):
    return User.query.filter_by(email=email).first()

@app.route('/signup', methods=['GET','POST'])
def signUpPage():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if username_in_db(username):
                flash('The username already exists. Please enter another username.', 'danger')
                return redirect(url_for('signUpPage'))

            elif email_in_db(email):
                flash('The email is already in use. Please enter another email.', 'danger')
                return redirect(url_for('signUpPage'))
            
            else:
                # add user to database
                user = User(username,email,password)

                db.session.add(user)
                db.session.commit()

                user = User.query.filter_by(username=username).first()
                user_id = user.user_id
                pokedex = Pokedex(user_id)

                db.session.add(pokedex)
                db.session.commit()

                pool = Pool(user_id)

                db.session.add(pool)
                db.session.commit()

                flash('Successfully created an account.', 'success')

                return redirect(url_for('loginPage'))

        else:
            flash('Passwords do not match. Please try again.', 'danger')
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('loginPage'))

@app.route('/catch', methods=['GET','POST'])
@login_required
def catchPokemon():
    current_pool = Pool.query.filter_by(user_id=current_user.user_id).first().pool_id
    pokemon_id = global_pokemon_data['pokemon #']
    pool_pokemon = PoolPokemon(current_pool,pokemon_id)
    db.session.add(pool_pokemon)
    db.session.commit()
    flash('Pokemon successfully added to your collection.', 'success')

    current_pokedex = Pokedex.query.filter_by(user_id=current_user.user_id).first().pokedex_id
    dexPokes = PokedexPokemon.query.filter_by(pokedex_id=current_pokedex).all()
    pokedexPokemon = dict()
    for poke in dexPokes:
        pokedexPokemon[poke.pokemon_id] = pokemon_id
    if not PokedexPokemon.query.filter_by(pokedex_id=current_pokedex).all():
        addPokedexPokemon = PokedexPokemon(current_pokedex, pokemon_id)
        db.session.add(addPokedexPokemon)
        db.session.commit()
    elif pokemon_id in pokedexPokemon:
        pass
    else:
        addPokedexPokemon = PokedexPokemon(current_pokedex, pokemon_id)
        db.session.add(addPokedexPokemon)
        db.session.commit()
        flash('Pokemon successfully added to your Pokedex.', 'success')
    
    return redirect(url_for('pokemonSearch'))

@app.route('/pokedex')
@login_required
def pokedex():
    current_pokedex = Pokedex.query.filter_by(user_id=current_user.user_id).first().pokedex_id
    pokemon_list = PokedexPokemon.query.filter_by(pokedex_id=current_pokedex).all()
    pokemon_id_list = []
    for pokemon in pokemon_list:
        pokemon_id_list.append(pokemon.pokemon_id)
    pokemon_id_list.sort()
    all_pokemon = []
    for poke_id in pokemon_id_list:
        all_pokemon.append(Pokemon.query.filter_by(pokemon_id=poke_id).first())

    return render_template('pokedex.html', all_pokemon=all_pokemon)

@app.route('/mypokemon')
@login_required
def myPokemon():
    current_pool = Pool.query.filter_by(user_id=current_user.user_id).first().pool_id
    pokemon_list = PoolPokemon.query.filter_by(pool_id=current_pool).all()
    all_pokemon = dict()
    for pokemon in pokemon_list:
        all_pokemon[pokemon.pool_pokemon_id] = Pokemon.query.filter_by(pokemon_id=pokemon.pokemon_id).first()
    # pokemon_id_list.sort()
    # all_pokemon = dict()
    # for poke_id in pokemon_id_list:
    #     all_pokemon[] = Pokemon.query.filter_by(pokemon_id=poke_id).first()
    return render_template('mypokemon.html', all_pokemon=all_pokemon)

@app.route('/mypokemon/<pool_pokemon_id>')
@login_required
def singlePokemonPage(pool_pokemon_id):
    pokemon = PoolPokemon.query.get(pool_pokemon_id)
    if pokemon:
        poke = Pokemon.query.get(pokemon.pokemon_id)
        return render_template('singlepokemon.html', poke=poke, pokemon=pokemon)
    else:
        return redirect(url_for('myPokemon'))

@app.route('/mypokemon/release/<pool_pokemon_id>')
@login_required
def releasePokemon(pool_pokemon_id):
    pokemon = PoolPokemon.query.get(pool_pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    flash('Pokemon successfully released.', 'success')
    return redirect(url_for('myPokemon'))