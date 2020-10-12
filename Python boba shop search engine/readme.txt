Amber, Yong, Shania
Final Project
CIS 41B

SUMMARY:
In this final project, we decided to create an application where we filter out boba shops in the surrounding area of De Anza College, which includes Cupertino, San Jose, Mountain View, Palo Alto, Santa Clara, Sunnyvale, Saratoga. We chose to use Yelp to get all the information such as the shop name, price, ratings, address, distance and a brief description of what the shop sells. Then the following information is stored in a database to provide easier access for the GUI. Also, Yelp limits their API to 5,000 calls per day. When the user opens the application, the user will be greeted by 3 buttons, one for searching boba shops by distance, by city, and lastly the user could see a graph corresponding to the most 4-5 starred boba shops in the city.

WEB SCRAPING DESCRIPTION:
In this part, we are fetching all the data from the chosen API, which is Yelp. Since Yelp's database isn't open to public, therefore
we need to apply for the access code. Here, we are looking to fetch the data for the shop name, description, rating, address, price and distance
from De Anza College. After extracting the all the needed information, the data is then saved to a JSON file. 

DATABASE DESCRIPTION:
In this part, we store the data from the JSON file into a database. The database is split into 4 tables, 1 main table for the 
boba shop and the specifications, 1 subtable for the name of the city, 1 subtable for the price, and 1 subtable for the ranking
of the shop.

GUI DESCRIPTION:
In this part, the program pops up a window with three buttons. For the first button, it shows buttons of distance categories and let the user choose, and then pop up a list of boba shop sorted by distance in the list box. For the second choice, it pops up a window with two buttons, for the user to search by city and dollar sign. For the third choice, it shows in a graph the number of 4-5 starred boba shops over each city. After clicking at the boba shop in the list box, there will be a message pop up showing the information about the selected boba shop.
