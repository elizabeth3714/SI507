from flask import Flask, render_template, url_for, jsonify, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps, Map, icons
# from markupsafe import Markup
from datetime import datetime, UTC
import datetime
from DataStructure import *
import pandas as pd
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
CORS(app)
app.app_context().push()

class Todo(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __repr__(self):
        return '<Task %r>' % self.id

# with app.app_context():
#     db.create_all()

property_input_list = {
    'mls_id': None,  # or empty string "" if you expect a string later
    'zip_code': None,
    'beds': 0,  # assuming a numerical value, start with 0 or None if it's unknown yet
    'price_range': None,
    'style': None,
    'sqft': 0,  # assuming a numerical value, start with 0 or None if it's unknown yet
    'neighborhoods': None,
    'street': None,
    'latitude': 0.0,  # assuming a float, start with 0.0 or None if it's unknown yet
    'longitude': 0.0,  # assuming a float, start with 0.0 or None if it's unknown yet
    'primary_photo': None,  # URL or path to the photo, None or empty string ""
    'property_url': None  # URL to the property listing, None or empty string ""
}



@app.route('/') #url
def index():
    # homes = HomeSearch.recommendation()
    # mls_id = homes[0]


    neighborhoods = ['',
        'South Philadelphia, West Passyunk',
        'West Philadelphia, Cobbs Creek', 'Center City, Graduate Hospital',
        'Center City, Society Hill', 'North Central, Lower North',
        'Richmond, River Wards', 'Elmwood, Southwest Philadelphia',
        'Brewerytown, Lower North',
        'Center City, Avenue of the Arts South',
        'Lower North, Brewerytown', 'Center City, Rittenhouse',
        'Center City, Logan Square', 'Center City, Washington Square West',
        'Whitman, South Philadelphia', 'Center City, Old City',
        'Center City, Northern Liberties', 'Rittenhouse, Center City',
        'Fishtown, River Wards', 'Tioga, Upper North Philadelphia',
        'Lower Moyamensing, South Philadelphia',
        'Lower North, Olde Kensington', 'West Philadelphia, Spruce Hill',
        'Center City, Franklin Bridge North Neighbors, Old City',
        'Center City, Spring Garden', 'West Philadelphia, Walnut Hill',
        'Center City, Center City East, Market East',
        'Upper Roxborough, Lower Northwest', 'Hartranft, Lower North',
        'Wissinoming, North Delaware', 'Upper Kensington, Kensington',
        'Center City, Queen Village',
        'Near Northeast Philadelphia, Lawndale',
        'West Philadelphia, Mantua', 'South Philadelphia, Passyunk Square',
        'Center City, Chinatown',
        'West Central Germantown, Upper Northwest',
        'Harrowgate, Kensington', 'Upper North District, West Oak Lane',
        'Lower North, North Central', 'Upper North District, Olney',
        'Upper North Philadelphia, Franklinville',
        'Center City, West Poplar', 'South Philadelphia, Point Breeze',
        'East Mount Airy, Upper Northwest',
        'Avenue of the Arts South, Center City',
        'West Mount Airy, Upper Northwest',
        'Germantown - Morton, Upper Northwest',
        'Center City, Fitler Square', 'Holmesburg, North Delaware',
        'Wissahickon, Lower Northwest', 'West Philadelphia, East Parkside',
        'Lower North, West Kensington',
        'South Philadelphia, Lower Moyamensing',
        'East Kensington, River Wards', 'East Falls, Upper Northwest',
        'Cedarbrook, Upper North District',
        'West Philadelphia, University City',
        'Upper North Philadelphia, Allegheny West',
        'Bella Vista, Italian Market, Center City',
        'Carroll Park, West Philadelphia', 'Center City, Francisville',
        'Stanton, Lower North', 'Center City, Bella Vista',
        'West Kensington, Lower North',
        'West Philadelphia, Saunders Park, West Powelton',
        'Upper North District, Ogontz',
        'Upper North Philadelphia, McGuire',
        'Center City, Avenue of the Arts North',
        'South Philadelphia, Grays Ferry',
        'Strawberry Mansion, Lower North', 'Center City, East Poplar',
        "Center City, Penn's Landing", 'South Philadelphia, East Passyunk',
        'River Wards, East Kensington',
        'Oxford Circle, Near Northeast Philadelphia, Made Amos',
        'Kensington, Frankford', 'Far Northeast Philadelphia, Parkwood',
        'Center City, Fairmount', 'Upper North Philadelphia, Hunting Park',
        'Lower Northwest, Roxborough', 'River Wards, Richmond',
        'West Philadelphia, Overbrook',
        'West Philadelphia, Cedar Park, Southwest Cedar Park',
        'Center City, Center City West, Rittenhouse',
        'West Philadelphia, Cedar Park',
        'Summerdale, Near Northeast Philadelphia',
        'Lower Northwest, Wissahickon',
        'Rittenhouse, Center City, Center City West',
        'Upper North Philadelphia, Tioga', 'Frankford, Kensington',
        'Northwood, Kensington', 'West Philadelphia, Cathedral Park',
        'Lower North, Sharswood', 'Society Hill, Center City',
        'Center City, Market East, Old City',
        'West Philadelphia, Garden Court', 'Lower North, Ludlow',
        'Center City, Hawthorne', 'West Philadelphia, West Parkside',
        'Manayunk, Lower Northwest, Main Street Manayunk',
        'Center City, Graduate Hospital, Christian Street Historic District',
        'Wister, Upper Northwest', 'Upper North District, Logan',
        'Germantown - Westside, Upper Northwest',
        'Grays Ferry, South Philadelphia',
        'Germantown - Penn Knox, Upper Northwest',
        'Near Northeast Philadelphia, Fox Chase',
        'Southwest Philadelphia, Elmwood', 'Upper Northwest, East Falls',
        'Garden Court, West Philadelphia',
        'Lower North, Avenue of the Arts North',
        'Center City, Bella Vista, Italian Market',
        'River Wards, Fishtown', 'West Philadelphia, Belmont',
        'Southwest Philadelphia, Kingsessing',
        'West Philadelphia, Woodland Terrace',
        'Castor Highlands, Near Northeast Philadelphia, Rhawnhurst',
        'West Philadelphia, Parkside Historic District, East Parkside',
        'Roxborough Park, Lower Northwest',
        'Kingsessing, Southwest Philadelphia, Angora',
        'Center City, Little Saigon, Bella Vista',
        'West Philadelphia, Mill Creek',
        'Allegheny West, Upper North Philadelphia',
        'Kingsessing, Southwest Philadelphia',
        'Southwest Philadelphia, Bartram Village',
        'Hunting Park, Upper North Philadelphia', 'Lower North, Yorktown',
        'South Philadelphia, Greenwich', 'Wynnefield, West Philadelphia',
        'South Philadelphia, Newbold', 'West Philadelphia, West Powelton',
        'Lower Northwest, Manayunk',
        'Southwest Schuylkill, Southwest Philadelphia',
        'Morrell Park, Far Northeast Philadelphia',
        'Manayunk, Lower Northwest',
        'Southwest Germantown, Upper Northwest',
        'Chestnut Hill, Upper Northwest',
        'Near Northeast Philadelphia, Oxford Circle, Made Amos',
        'West Marconi Plaza, South Philadelphia, Girard Estates',
        'West Philadelphia, Powelton', 'Ogontz, Upper North District',
        'Lower North, Stanton, Diamond Street',
        'East Passyunk, South Philadelphia',
        'Lower North, North Central, Diamond Street',
        'West Philadelphia, Haverford North',
        'Southwest Philadelphia, Southwest Schuylkill',
        'Near Northeast Philadelphia, Rhawnhurst',
        'Point Breeze, South Philadelphia',
        'Upper North District, Fern Rock',
        'Upper North District, East Oak Lane',
        'Logan, Upper North District',
        'Oxford Circle, Made Amos, Near Northeast Philadelphia',
        'West Philadelphia, Dunlap', 'Lower North, Stanton',
        'South Philadelphia, Packer Park', 'Tacony, North Delaware',
        'Passyunk Square, South Philadelphia',
        'East Germantown, Upper Northwest', 'Ludlow, Lower North',
        'South Philadelphia, Girard Estates',
        'Italian Market, South Philadelphia, Passyunk Square',
        'North Delaware, Tacony',
        'Center City, Italian Market, Bella Vista',
        'Packer Park, South Philadelphia', 'West Philadelphia, Haddington',
        'Lower Northwest, Germany Hill',
        'Bustleton, Far Northeast Philadelphia',
        'Haddington, West Philadelphia', 'Newbold, South Philadelphia',
        'South Philadelphia',
        'Lower Northwest, Manayunk, Main Street Manayunk',
        'North Delaware, Wissinoming', 'Center City, Callowhill',
        'Girard Estates, South Philadelphia',
        'North Central, Lower North, Diamond Street',
        'Dickinson Square West, South Philadelphia',
        'Hawthorne, Center City', 'North Delaware, Mayfair',
        'Lower Northwest, Roxborough Park',
        'Southwest Philadelphia, Kingsessing, Mount Moriah',
        'Upper Northwest, East Germantown',
        'West Philadelphia, Wynnefield',
        'Far Northeast Philadelphia, Walton Park, Parkwood',
        'Rittenhouse, Center City West, Center City',
        'Eastwick, Southwest Philadelphia', 'North Delaware, Holmesburg',
        'Olde Kensington, Lower North', 'Sharswood, Lower North',
        'Somerton, Far Northeast Philadelphia',
        'South Philadelphia, Pennsport',
        'Paschall, Southwest Philadelphia', 'Roxborough, Lower Northwest',
        'Upper North Philadelphia, Feltonville',
        'Upper North Philadelphia, Nicetown',
        'Germantown, Upper Northwest',
        'Southwest Philadelphia, Kingsessing, Angora',
        'Aston - Woodbridge, Far Northeast Philadelphia',
        'Yorktown, Lower North', 'Near Northeast Philadelphia, Summerdale',
        'Little Saigon, South Philadelphia, Passyunk Square',
        'South Philadelphia, Whitman', 'River Wards, Bridesburg',
        'West Philadelphia, Carroll Park',
        'Near Northeast Philadelphia, Lexington Park',
        'Kingsessing, Southwest Philadelphia, Mount Moriah',
        'Far Northeast Philadelphia, Aston - Woodbridge',
        'Bridesburg, River Wards',
        'South Philadelphia, Dickinson Square West',
        'Torresdale, North Delaware',
        'Near Northeast Philadelphia, Oxford Circle',
        'Dunlap, West Philadelphia',
        'Feltonville, Upper North Philadelphia',
        'Juniata Park, Kensington', 'Lower North, Hartranft',
        'West Philadelphia, Wynnefield Heights',
        'Overbrook Farms Historic District, West Philadelphia, Overbrook',
        'Main Street Manayunk, Lower Northwest, Manayunk',
        'Kensington, Juniata Park', 'Upper Darby, Stonehurst Hills',
        'Mayfair, North Delaware',
        'Center City, Devils Pocket, Graduate Hospital',
        'Center City, Bella Vista, Little Saigon',
        'Center City, Center City East', 'Logan Square, Center City',
        'Mount Moriah, Kingsessing, Southwest Philadelphia',
        'Greenwich, South Philadelphia',
        'Lexington Park, Near Northeast Philadelphia',
        'Penrose, Southwest Philadelphia',
        'West Passyunk, South Philadelphia',
        'Paschall, Southwest Philadelphia, Mount Moriah',
        'South Philadelphia, Stadium District, East Marconi Plaza',
        'Far Northeast Philadelphia, Morrell Park',
        'Wynnefield Heights, West Philadelphia',
        'North Delaware, Torresdale',
        'Far Northeast Philadelphia, North Torresdale',
        'West Oak Lane, Upper North District',
        'Pennypack, Far Northeast Philadelphia',
        'Girard Estates, South Philadelphia, West Marconi Plaza',
        'Upper North Philadelphia, Glenwood',
        'West Philadelphia, Southwest Cedar Park, Cedar Park',
        'Bala Cynwyd, Main Line', 'Bella Vista, Center City',
        'Melrose Park Garden, Upper North District',
        'Far Northeast Philadelphia, Academy Gardens',
        'Southwest Philadelphia, Eastwick',
        'Upper Northwest, East Mount Airy',
        'Lower Northwest, Dearnley Park',
        'Bella Vista, Center City, Little Saigon',
        'West Philadelphia, Overbrook, Overbrook Farms Historic District',
        'Bartram Village, Southwest Philadelphia',
        'Upper North District, Cedarbrook',
        'Dearnley Park, Lower Northwest', 'Germany Hill, Lower Northwest',
        'Walnut Hill, West Philadelphia', 'Mill Creek, West Philadelphia',
        'Fern Rock, Upper North District',
        'Washington Square West, Center City'
        ]
    # Generate the options for the dropdown menu
    options_html = '\n'.join(f'<option value="{n}">{n}</option>' for n in neighborhoods)

    # Define the HTML structure with a placeholder for the options
    html_template = '''
    <div class="content">
        <h3>Neighborhood:</h3>
        <select name="Select">
            {{ options|safe }}
        </select>
    </div>
    '''

    # Render the final HTML
    return render_template('index.html', options=options_html)
    # return render_template('index.html')


def process_input(city, zip_code, bed, price_range, style, sqft):
    # Process the input values
    return city, zip_code, bed, price_range, style, sqft



file_path = 'HomeHarvest_20240425_184034_philly_forrent365days.csv'
homesearch = HomeSearch(file_path)

@app.route('/submit2', methods=['GET', 'POST']) #get_recommendation
def get_recommendation():
    file_path = 'HomeHarvest_20240425_184034_philly_forrent365days.csv'
    homesearch = HomeSearch(file_path)
    global recommd_property
    recommd_property = {}  # Default empty dictionary
    score = 0              # Default score
    property_input_list = {
        'mls_id': request.form.get('mls_id', None),
        'zip_code': request.form.get('zip_code', None),
        'beds': request.form.get('beds', 0),
        'price_range': request.form.get('price_range', None),
        'style': request.form.get('style', None),
        'sqft': request.form.get('sqft', 0),
        'neighborhoods': request.form.get('neighborhoods', None),
        'street': request.form.get('street', None),
        'latitude': float(request.form.get('latitude', 0)),
        'longitude': float(request.form.get('longitude', 0)),
        'primary_photo': request.form.get('primary_photo', None),
        'property_url': request.form.get('property_url', None)
        }
    # Converting each scalar value to a list
    property_input_list = {key: [value] for key, value in property_input_list.items()}
    if request.method == 'POST':  
        # properties = homesearch.load_properties()
        curr_property = pd.DataFrame(property_input_list)  # use the input from the form
        recommd_property, score = homesearch.recommendation(curr_property)
        
        return render_template('find_prop.html', recommd_property=recommd_property, score=score), recommd_property

    else:
        return render_template('find_prop.html', recommd_property={}, score=0)


@app.route('/submit3', methods=['GET','POST']) #get_recommendation
def get_recommendation2():
    file_path = 'HomeHarvest_20240425_184034_philly_forrent365days.csv'
    homesearch = HomeSearch(file_path)
    score = 0              # Default score
    property_input_list = {
        'mls_id': request.form.get('mls_id', None),
        'zip_code': request.form.get('zip_code', None),
        'beds': request.form.get('beds', 0),
        'price_range': request.form.get('price_range', None),
        'style': request.form.get('style', None),
        'sqft': request.form.get('sqft', 0),
        'neighborhoods': request.form.get('neighborhoods', None),
        'street': request.form.get('street', None),
        'latitude': float(request.form.get('latitude', 0)),
        'longitude': float(request.form.get('longitude', 0)),
        'primary_photo': request.form.get('primary_photo', None),
        'property_url': request.form.get('property_url', None)
        }

    property_input_list = recommd_property
    curr_property = pd.DataFrame(property_input_list)  # use the input from the form
    recommd_property2, score0 = homesearch.recommendation(curr_property)
    key_order = ['mls_id', 'zip_code', 'beds', 'price_range', 'style', 'sqft', 'neighborhoods',
                    'street', 'latitude', 'longitude', 'primary_photo', 'property_url']    
    recommd_property2 = {k: recommd_property2[k] for k in key_order}
    adjList, n_cooccurrence = homesearch.generateAdjList()
    ID1 = curr_property['mls_id'][0]
    ID2 = list(adjList.keys())[0]
    score = homesearch.query_co_occurrence(n_cooccurrence, ID1, ID2)

    print(recommd_property2, score)
    print(ID1, ID2)

    return render_template('rec_prop.html', recommd_property2=recommd_property2, score=score)




if __name__ == '__main__':
    app.run(debug=True)