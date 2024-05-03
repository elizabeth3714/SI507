Search Your Dream Home

1. Data and source:

The data was scraped from Realtor.com. The scraper was HomeHarvest developed by some users in the online community. 
File name: homeharvest_scraper.ipynb
Source: https://github.com/Bunsly/HomeHarvest

HomeHarvest:
By using this scraper/API, the user can select the city, time period of online record, type of the listing (for sale, for rent, 
sold, etc.).
In this final project, I selected the city of Philadelphia, rental listings in the past 365 days.
Data is saved as a CSV file in the current directory.
CSV file name: HomeHarvest_20240425_184034_philly_forrent365days.csv

Data:
There are a total of 3489 records for the rental units in Philadelphia in the past year.
The data was read from the saved CSV file, and further cleaned.
Data cleaning and pre-processing:
File name: DataStructure.py
- Missing values were filled in proportionally based on the existing non-Na values.
- Two variables about price and square footage have been converted to ordinal value, for easy selection.
- 12 variables were kept for this project:
	'mls_id': the property's unique ID
	'zip_code': zip code 
	'beds': number of bedrooms 
	'price_range': price range 
	'style': housing type 
	'sqft': square footage
	'neighborhoods': neighborhood
	'street': address
	'latitude': latitude 
	'longitude': longitude 
	'primary_photo': the primary photo from Realtor.com 
	'property_url': link to Realtor.com listing


2. Data Structure - Graph/Network
File name: DataStructure.py
How Graph/Network works:
Each property unit is taken as a node, and the sharing features are the secondary nodes. The co-occurrences of secondary nodes
represent the shared features of two property units.
Greedy method:
Both greedy method and graph structure has been experimented. The greedy method attempts to find a property with the most available
shared features based on the input criteria. It is achieved through the function "Recommendation()".
Graph method with single co-occurrence:
The graph structure is built in the function generateAdjList(), where two units are connected by their (single) shared feature.
Calculation of similarity score:
The algorithm further did a calculation of the common features between two units. This is realized by the function query_co_occurrence().
A similarity score is listed at the bottom of the recommendation page.