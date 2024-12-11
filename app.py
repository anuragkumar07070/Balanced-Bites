from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load your CSV data
data = pd.read_csv('data.csv')
data.columns = data.columns.str.strip()  # Remove any leading/trailing whitespace

@app.route('/')
def index():
    # Pass the food items to the index template using the correct column name
    food_items = data['name'].tolist()
    return render_template('index.html', food_items=food_items)

@app.route('/search_food')
def search_food():
    # Get the search query
    query = request.args.get('query', '').lower()

    # Find the food in the dataset
    food_item = data[data['name'].str.lower() == query]

    if not food_item.empty:
        # Pass the first match to the food.html template
        food = food_item.iloc[0].to_dict()
        # Redirect to the food detail page
        return redirect(url_for('food', food_name=food['name']))
    else:
        return "Food not found", 404


@app.route('/food/<food_name>')
def food(food_name):
    # Get the nutritional information for the selected food item
    food_info = data[data['name'].str.lower() == food_name.lower()].squeeze()

    # Check if the food exists
    if food_info.empty:
        return "Food not found", 404

    return render_template('food.html', food=food_info)


if __name__ == '__main__':
    app.run(debug=True)
