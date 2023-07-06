from flask import render_template, request, redirect, url_for
from app import app
from .forms import PokemonSearch
import requests as r
# from .models import User, db

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/favorite5')
def favorite5Page():

    favorite_pokemons = [{
        'name': 'Arceus',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/493.png'
    },{
        'name': 'Charizard',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png'
    },{
        'name': 'Mew Two',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png'
    },{
        'name': 'Rayquaza',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/384.png'
    },{
        'name': 'Snorlax',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png'
    }]

    return render_template('favorite5.html', favorite_pokemons = favorite_pokemons)

def get_pokemon_info(pokemon_name):
    res = r.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if res.ok:
        data = res.json()
        pokemon_data = dict()
        pokemon_data['name'] = data['forms'][0]['name'].title()
        i = 1
        for ability in data['abilities']:
            pokemon_data['ability ' + str(i)] = ability['ability']['name']
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
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokename.data
            poke_data = get_pokemon_info(pokemon.lower())
            
            # # add user to database
            # user = User(username,email,password)

            # db.session.add(user)
            # db.session.commit()
    
    return render_template('pokemon.html', form=form, pokemon_data = poke_data)