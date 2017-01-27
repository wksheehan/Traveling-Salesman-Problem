# Traveling-Salesman-Problem
We attempted to solve the travelling salesman problem by creating a circle with a center located at the mean longitude and latitude of the cities the user enters (this report will use longitude and latitude in place of x and y coordinates). We gathered the longitude and latitude of each city using a Google Maps API that returns the longitude and latitude of whatever city is inputted. We then create a radius for the circle, mentioned earlier, that extends to the starting point of the cities the user wants to visit, although the radius of the circle does not affect the rest of the method. Once creating the circle, we create lines that extend from each city/point that the user inputted to the center of the circle. We then go around the circle and visit each city in the order that their corresponding line intersects with the circle. For example, the starting point is the first city that is visited, and then the city whose line’s intersection point is next in a clockwise order around the circle and so on until returning to the original starting city on the circle. This order is then returned to the user to visit the cities in that order for the shortest route possible. This method works for many cases. However, it often is false as well, with the most obvious way to describe this being two inscribed circles, with the points on the inner circle being spaced between the points on the outer circle. We are unsure of how to proceed and would like assistance on a way to overcome this problem in our method.