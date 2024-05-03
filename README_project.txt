Search Your Dream Home

1. Packages in Python (in app.py):

# from flask import Flask, render_template, url_for, jsonify, request, redirect, abort
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, UTC
# import datetime
# from DataStructure import *
# import pandas as pd
# from flask_cors import CORS

2. Initiate the page (in app.py):
Click "Run" button and the terminal returns the link of the website. By default it is Localhost:5000.

3. Main Page:
On the main page, input the home features you are looking for, for example, zip code, unit size, price range, etc.
It doesn't require input of all criteria, but more information serves for better recommendation results.
Click "Find Home" to the recommendation page.

4. Recommendation Page 1:
The program attempts to find the best match based on the input criteria. A similarity score is calculated based on
the shared similarity. 
Home information is displayed including zip code, neighborhood, unit size, price range, square footage, and housing type.
An interactive map from Open Street Map is embedded on this page, so the user can zoom in and out to check the location and surroundings.
A primary photo is inserted on this page for some visual reference.
A hyperlink of the listing can direct the user to Realtor.com for more information.
Users can click "More Recommendation" to find more similar properties.
Users can click "Back to Search" to return to the main page.

5. Recommendation Page 2:
By clicking "More Recommendation", it directs to a new web page of a similar property. The information structure is similar
to Recommendation Page 1. Similarly, users can click "Back to Search" to return to the main page.

6. How Graph/Network works (in DataStructure.py):
Each property unit is taken as a node, and the sharing features are the secondary nodes. The co-occurrences of secondary nodes
represent the shared features of two property units.
Both greedy method and graph structure has been experimented. The greedy method attempts to find a property with the most available
shared features based on the input criteria. It is achieved through the function "Recommendation()".
The graph structure is built in the function generateAdjList(), where two units are connected by their (single) shared feature.
The algorithm further did a calculation of the common features between two units. This is realized by the function query_co_occurrence().

