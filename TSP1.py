import requests
import pprint
import math

citynames = []
x_coordinates = []
y_coordinates = []

# Get number of cities
number_of_cities = raw_input('How many cities would you like to visit? Please press enter after each response. ')
if number_of_cities.isdigit() == True:
    Number_of_Cities = int(number_of_cities)
elif number_of_cities.isdigit() == False:
    print "Please enter an integer and try again."
    quit()
NOC_test = int(number_of_cities)
if NOC_test <= 1:
    print "You must enter more than 1 city. Please rerun the program and try again."
    quit()

# Get the cities
for i in range(Number_of_Cities):
    citynames.append(raw_input('Enter a city: ').lower())
CityNames = []
for i in citynames:
    CityNames.append(i.title())
    
print
print "These are the cities you entered:", CityNames

# API call to get longitude and latitude
for i in citynames:
    r = requests.get('''https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyBXreCjf8x8_L7-7CW7ymdsV7jLaxuXeRg'''.format(i))
    data = r.json()
    if data['results']:
        x_coordinates.append(data['results'][0]['geometry']['location']['lng'])
        y_coordinates.append(data['results'][0]['geometry']['location']['lat'])
    else:
        print "You have entered a nonexistent city. Please look back at the cities you entered to check for any typos and try again."
        quit()

# Choose aribtrary starting city
starting_pt = (x_coordinates[0],y_coordinates[0])
x_coordinates.remove(x_coordinates[0])
y_coordinates.remove(y_coordinates[0])

lst = []
n = 0
# Convert circle center and radius
for i in range(Number_of_Cities-1):
    lst += [(x_coordinates[n], y_coordinates[n])]
    n += 1
sum_long = sum(x_coordinates) + starting_pt[0]
sum_lat = sum(y_coordinates) + starting_pt[1]
mean_long = sum_long/float(NOC_test)
mean_lat = sum_lat/float(NOC_test)
radius_yvalue = mean_lat - starting_pt[1]
radius_xvalue = mean_long - starting_pt[0]
radius_length = math.sqrt((radius_yvalue)**2 + (radius_xvalue)**2)

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

sol=[]
line_equations = []
x_int_pts = []

# Calculate order of x locations
for i in lst:
    zero_div_test = i[0] - mean_long
    if zero_div_test == 0:
        x_int0 = i[0]
        solution_base1.append(x_int0)
    else:
        m = ((i[1])- mean_lat)/((i[0])-mean_long)
        a = (m**2) + 1
        b = -2*((m**2)*mean_long)-(2*mean_long)
        c = (-(radius_length**2) + (mean_long**2) + (m*mean_long)**2)
        discriminant = (b**2)-(4*a*c)
        if discriminant >= 0:
            sqrt_discrim = math.sqrt(float(discriminant))
            x_int1 = float(-b + sqrt_discrim)/float(2*a)
            x_int2 = float(-b - sqrt_discrim)/float(2*a)
            if i[0] > mean_long and x_int1 > x_int2:
                x_int_pts.append(x_int1)
            if i[0] > mean_long and x_int1 < x_int2:
                x_int_pts.append(x_int2)
            if i[0] < mean_long and x_int1 > x_int2:
                x_int_pts.append(x_int2)
            if i[0] < mean_long and x_int1 < x_int2:
                x_int_pts.append(x_int1)
upper_half = []
lower_half = []
int_pts = []
y_int_pts = []
k=0

# Find order of y locations and condense to int_pts
for i in x_int_pts:
    circle_solver = radius_length**2 - ((i-mean_long)**2)
    y_int_pt1 = math.sqrt(circle_solver) + mean_lat
    y_int_pt2 = -math.sqrt(circle_solver) + mean_lat
    if lst[k][1] > mean_lat and y_int_pt1 > y_int_pt2:
            y_int_pts.append(y_int_pt1)
    if lst[k][1] > mean_lat and y_int_pt1 < y_int_pt2:
            y_int_pts.append(y_int_pt2)
    if lst[k][1] < mean_lat and y_int_pt1 < y_int_pt2:
            y_int_pts.append(y_int_pt1)
    if lst[k][1] < mean_lat and y_int_pt1 > y_int_pt2:
            y_int_pts.append(y_int_pt2)
    int_pts += [(i, y_int_pts[k])]
    k += 1

int_pts.append((starting_pt))

for i in int_pts:
    if i[1] > mean_lat:
        upper_half.append(i)
    if i[1] < mean_lat:
        lower_half.append(i)

orig_upper_half = []
orig_lower_half = []

for i in lst:
    if i[1] > mean_lat:
        orig_upper_half.append(i)
    if i[1] < mean_lat:
        orig_lower_half.append(i)

if starting_pt[1] > mean_lat:
    orig_upper_half.append(starting_pt)
if starting_pt[1] <= mean_lat:
    orig_lower_half.append(starting_pt)

zipped_upper = zip(upper_half, orig_upper_half)
zipped_lower = zip(lower_half, orig_lower_half)
zipped_upper.sort()
zipped_lower.sort()
zipped_lower.reverse()
zipped_lower_len = len(zipped_lower)
zipped_upper_len = len(zipped_upper)
sorted_unzip_upper = zip (*zipped_upper)
sorted_unzip_upper[1]
sorted_unzip_lower = zip (*zipped_lower)
sorted_unzip_lower[1]

final_list = sorted_unzip_upper[1] + sorted_unzip_lower[1]

ordered_cities = []
Ordered_Cities = []

for i in final_list:
    bang = i[0]
    bung = i[1]
    t = requests.get('''https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyBXreCjf8x8_L7-7CW7ymdsV7jLaxuXeRg''' % (bung, bang))
    data2 = t.json()
    str0 = data2['results'][0]['formatted_address'].lower()
    str1 = data2['results'][1]['formatted_address'].lower()
    str2 = data2['results'][2]['formatted_address'].lower()
    str3 = data2['results'][3]['formatted_address'].lower()
    str4 = data2['results'][4]['formatted_address'].lower()
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
            ordered_cities.append(k)

for i in ordered_cities:
    Ordered_Cities.append(i.title())

if len(ordered_cities) != len(citynames):
    print "You have entered a nonexistent city. Please look back at the cities you entered to check for any typos and try again."
    quit()

time_list = []
for i in Ordered_Cities:
    time_list.append(i)
time_list.append(Ordered_Cities[0])
times = []

print "For the fastest route, visit the cities in this order:", Ordered_Cities
print "(Note: You can start at any city you like, and move right or left through the list and return back to the city you started at.)"

America = raw_input('Would you like the driving time between the cities, if possible? Y/N    ')
if America == 'Y':
    for i in range(NOC_test):
        origin = time_list[i]
        destination = time_list[i+1]
        q = requests.get('''https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s&key=AIzaSyBXreCjf8x8_L7-7CW7ymdsV7jLaxuXeRg''' % (origin, destination))
        data3 = q.json()
        test = data3['rows'][0]['elements'][0]
        if 'duration' in test.keys():
            pass
        else:
            print "Sorry, it is not possible to drive to all the destinations you entered"
            quit()
        time = data3['rows'][0]['elements'][0]['duration']['value']
        times.append(time)
    round_trip_sec = sum(times)
    round_trip_hours = round_trip_sec/360
    round_trip_days = round_trip_hours/24
    print "If you are driving, it will take you approximately %s hours, or %s days, to complete your journey." % (round_trip_hours, round_trip_days)
else:
    print "Okay, fine. Have it your way."
                     
#in order to make compatible with new python servers that don't sort zipped objects. zip them. sort the int pts one only. Then use the find function to line them all up
