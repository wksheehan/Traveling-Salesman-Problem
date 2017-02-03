import requests
import pprint
import math

citynames = []
x_coordinates = []
y_coordinates = []

number_of_cities = raw_input('How many cities would you like to visit? Please press enter after each response. ') #Gets number of cities the user wants to enter
if number_of_cities.isdigit() == True: #tests to see if user inputted a number
    Number_of_Cities = int(number_of_cities)
elif number_of_cities.isdigit() == False:
    print "Please enter an integer and try again."
    quit() #quits program if user did not enter a number
NOC_test = int(number_of_cities)  #changes from string to integer
if NOC_test <= 1:
    print "You must enter more than 1 city. Please rerun the program and try again."
    quit() #quits program if the user does not input a list of cities

for i in range(Number_of_Cities):
    citynames.append(raw_input('Enter a city: ').lower()) #user inputs their list of cities and cities are appended to a list
CityNames = []
for i in citynames:
    CityNames.append(i.title()) #unifies the format of the cities to be compatible with Google Maps APIs
    
print
print "These are the cities you entered:", CityNames #returns the unordered list of cities

for i in citynames:
    r = requests.get('''https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyBXreCjf8x8_L7-7CW7ymdsV7jLaxuXeRg'''.format(i)) #gets city data from Google Map API
    data = r.json()
    if data['results']:
        x_coordinates.append(data['results'][0]['geometry']['location']['lng'])
        y_coordinates.append(data['results'][0]['geometry']['location']['lat']) #retrieves the latitude and longitude from the data gathered by the Google Map API
    else:
        print "You have entered a nonexistent city. Please look back at the cities you entered to check for any typos and try again."
        quit() #quits program if user enters a nonexistent city

starting_pt = (x_coordinates[0],y_coordinates[0]) #defines starting point as the first city entered
x_coordinates.remove(x_coordinates[0])
y_coordinates.remove(y_coordinates[0]) #removes starting point from list that will be ordered

lst = []
n = 0
for i in range(Number_of_Cities-1):
    lst += [(x_coordinates[n], y_coordinates[n])]
    n += 1 #gathers the coordinates of both cities into a longitude and latitude, similar to an x and y coordinate
sum_long = sum(x_coordinates) + starting_pt[0]
sum_lat = sum(y_coordinates) + starting_pt[1]
mean_long = sum_long/float(NOC_test)
mean_lat = sum_lat/float(NOC_test) #finds the mean longitude and latitude where the center of the circle will be
radius_yvalue = mean_lat - starting_pt[1]
radius_xvalue = mean_long - starting_pt[0]
radius_length = math.sqrt((radius_yvalue)**2 + (radius_xvalue)**2) #creates a radius for the circle

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2) #a function to find the distance between any two points

sol=[]
line_equations = []
x_int_pts = []

for i in lst:
    zero_div_test = i[0] - mean_long
    if zero_div_test == 0: #tests to ensure that the slope of our line to find the intersection is not undefined
        x_int0 = i[0] 
        solution_base1.append(x_int0) #adds the longitude of the point as the x-value integer if the point is located right above or below the origin of the circle
    else:
        m = ((i[1])- mean_lat)/((i[0])-mean_long)
        a = (m**2) + 1
        b = -2*((m**2)*mean_long)-(2*mean_long)
        c = (-(radius_length**2) + (mean_long**2) + (m*mean_long)**2)
        discriminant = (b**2)-(4*a*c)
        if discriminant >= 0:
            sqrt_discrim = math.sqrt(float(discriminant))
            x_int1 = float(-b + sqrt_discrim)/float(2*a)
            x_int2 = float(-b - sqrt_discrim)/float(2*a) #determines the longitude value of the two intersections between the line and the circle using the quadratic formula
            if i[0] > mean_long and x_int1 > x_int2:
                x_int_pts.append(x_int1)
            if i[0] > mean_long and x_int1 < x_int2:
                x_int_pts.append(x_int2)
            if i[0] < mean_long and x_int1 > x_int2:
                x_int_pts.append(x_int2)
            if i[0] < mean_long and x_int1 < x_int2:
                x_int_pts.append(x_int1) #appends the intersection between the line segment we created between the origin and the city and the circle. This works by taking the larger longitudinal value of the intersection if the city is to the right of the origin of the circle and the smaller longitudinal value if the city is to the left of the origin of the circle.
upper_half = []
lower_half = []
int_pts = []
y_int_pts = []
k=0

for i in x_int_pts:
    circle_solver = radius_length**2 - ((i-mean_long)**2)
    y_int_pt1 = math.sqrt(circle_solver) + mean_lat
    y_int_pt2 = -math.sqrt(circle_solver) + mean_lat #determines the latitude of the intersection points between the circle and the lines
    if lst[k][1] > mean_lat and y_int_pt1 > y_int_pt2:
            y_int_pts.append(y_int_pt1)
    if lst[k][1] > mean_lat and y_int_pt1 < y_int_pt2:
            y_int_pts.append(y_int_pt2)
    if lst[k][1] < mean_lat and y_int_pt1 < y_int_pt2:
            y_int_pts.append(y_int_pt1)
    if lst[k][1] < mean_lat and y_int_pt1 > y_int_pt2:
            y_int_pts.append(y_int_pt2) #If the latitude of the city is greater than the latitude of the origin of the circle, it takes the greater latitude of the intersection points and appends it to the list of latitudes of the intersection. If the latitude of the city is less than the latitude of the origin of the circle, it takes the lesser latitude of the intersection points and appends it to the list of latitudes of the intersections.
    int_pts += [(i, y_int_pts[k])]
    k += 1

int_pts.append((starting_pt)) #adds the starting point back to the intersection points before ordering them, since it is already on the radius of the circle.

for i in int_pts:
    if i[1] > mean_lat:
        upper_half.append(i)
    if i[1] < mean_lat:
        lower_half.append(i) #splits the circle into an upper half and lower half, so it can order the two halves separately, then combine them

orig_upper_half = []
orig_lower_half = []

for i in lst:
    if i[1] > mean_lat:
        orig_upper_half.append(i)
    if i[1] < mean_lat:
        orig_lower_half.append(i) #splits the original circle into an upper and lower half, to zip the original points and the intersection points together

if starting_pt[1] > mean_lat:
    orig_upper_half.append(starting_pt)
if starting_pt[1] <= mean_lat:
    orig_lower_half.append(starting_pt) #adds the starting point to the list of points for the half of the circle that it lies on

zipped_upper = zip(upper_half, orig_upper_half)
zipped_lower = zip(lower_half, orig_lower_half) #zips the original points and the intersection points together
zipped_upper.sort()
zipped_lower.sort() #sorts the two zipped lists individually by the x value of the intersection points
zipped_lower.reverse() #reverses the order of the bottom half so the points would follow a circle
sorted_unzip_upper = zip (*zipped_upper)
sorted_unzip_upper[1]
sorted_unzip_lower = zip (*zipped_lower)
sorted_unzip_lower[1] #unzips lists so that we can extract the longitude and latitude of the actual cities that we want to reverse geocode. The list[1] returns the longitude and latitudes of the actual cities

final_list = sorted_unzip_upper[1] + sorted_unzip_lower[1] #final list of longitudes and latitudes of the actual cities that has been sorted

ordered_cities = []
Ordered_Cities = []

for i in final_list:
    bang = i[0] #longitude of the individual city
    bung = i[1] #latitude of the individual city
    t = requests.get('''https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyBXreCjf8x8_L7-7CW7ymdsV7jLaxuXeRg''' % (bung, bang)) #gathers information about the latitude and longitude of the city
    data2 = t.json()
    str0 = data2['results'][0]['formatted_address'].lower()
    str1 = data2['results'][1]['formatted_address'].lower()
    str2 = data2['results'][2]['formatted_address'].lower()
    str3 = data2['results'][3]['formatted_address'].lower()
    str4 = data2['results'][4]['formatted_address'].lower() #combs through the data to extract possible locations for the name of the city
    for k in citynames:
        if str0.find(k)!=-1:
            ordered_cities.append(k)
        elif str1.find(k)!=-1:
            ordered_cities.append(k)
        elif str2.find(k)!=-1:
            ordered_cities.append(k)
        elif str3.find(k)!=-1:
            ordered_cities.append(k)
        elif str4.find(k)!=-1:
            ordered_cities.append(k) #finds the name of the original city the user entered listed within the data returned from the reverse geocode and adds it to the list of ordered return cities.

for i in ordered_cities:
    Ordered_Cities.append(i.title()) #unifies the format of the returned cities

if len(ordered_cities) != len(citynames):
    print "You have entered a nonexistent city. Please look back at the cities you entered to check for any typos and try again."
    quit() #quits the program if a user made a typo while entering cities, but the Google Maps API still locates a longitude and latitude to accompany the mistyped city

print "For the fastest route, visit the cities in this order:", Ordered_Cities
print "Note: You can start at any city you like, and move clockwise or counter-clockwise through the list and return back to the city you started at." #returns the list of ordered cities