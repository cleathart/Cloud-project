import config
import storage
import logging
import hashlib
from flask import Flask, render_template, request, session
from flask.json import jsonify
from google.cloud.storage import Blob

from search_api import SearchAPI

app = Flask(__name__)
app.config.from_object(config)

# store of recipes
recipes = SearchAPI()

# uploads images to bucket
def upload_image_file(file):
    if not file:
        return None
    
    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    return public_url

@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.html',
        title = "Empty My Fridge!")

# @app.route('/clear_database')
# def clear_data():
#     recipes.delete_all()
#     return 'database cleared'

@app.route('/submitted_fridge', methods=['GET', 'POST'])
def submitted_fridge():
    if request.method == 'POST':

        all_results = []
        search_result_1 = recipes.search('ingredients: ' + request.form['Ingredient1'])
        search_result_2 = recipes.search('ingredients: ' + request.form['Ingredient2'])
        search_result_3 = recipes.search('ingredients: ' + request.form['Ingredient3'])
        all_results = search_result_1 + search_result_2 + search_result_3

        seen = set()
        search_result = []
        for res in all_results:
            t = tuple(res.items())
            if t not in seen:
                seen.add(t)
                res['url'] = hashlib.md5(res['recipe_name']).hexdigest()
                search_result.append(res)

    return render_template(
         'search.html',
         recipes = search_result)

@app.route('/new_recipe', methods=['GET'])
def new_recipe():
    return render_template(
        'new_recipe.html',
        title = "Give a recipe"
    )

@app.route('/submitted_recipe', methods=['POST'])
def submitted_recipe():
    if request.method == 'POST':
        image_url = upload_image_file(request.files.get('image'))
        recipes.insert(request.form, image_url)
    
    return render_template(
        'new_recipe_submitted.html',
        title = 'Thanks for the recipe!',
    )

@app.route('/recipe/<recipe_hash>', methods=['GET'])
def show_recipe(recipe_hash):
    recipe_result = recipes.get_key(recipe_hash)

    if bool(recipe_result):
        ingredients = recipe_result['ingredients'].split(' - ')
        method = recipe_result['method'].split(' - ')

        return render_template(
            'recipe.html',
            recipe_name = recipe_result['recipe_name'],
            ingredients = ingredients,
            method = method,
            img_url = recipe_result['image_url']
        )
    else:
        return '404 no recipe at this address'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__=='__main__':
    app.run(debug=True)