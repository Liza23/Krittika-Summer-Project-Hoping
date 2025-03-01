import math
import pandas as pd

class Point():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
def distance(a,b):
  x_term = int(a.x) - int(b.x)
  y_term = int(a.y) - int(b.y)
  return math.sqrt((x_term * x_term) + (y_term * y_term))

# this function will return the value of the nearest 
# star to the clicks from the selected stars.

def min_distance(click, star_catalogue):
  star_name = None

  stars_point = []
  # star_point is list of Point objects with ra as 
  # the x and dec as the y values of the star.
  for i in range(len(star_catalogue)):
    x = star_catalogue['ra'][i]
    y = star_catalogue['dec'][i]
    p = Point(x,y)
    stars_point.append(p)
  
  try:
    min_val = distance(click, stars_point[0])
    min_star = stars_point[0]
  
    count = 0
  # to keep a track of stars which are at a same value from our click
  
    for i in range(len(stars_point)):
      if min_val >= distance(click, stars_point[i]):
        min_val = distance(click, stars_point[i])
        min_star = stars_point[i]
        star_name = star_catalogue['star'][i]
        count += 1
    
    assert(count == 1)

    return min_star, star_name
  
  except AssertionError:
    print("Two or more stars found nearby! Try again")
    temp = Point(None, None)
    return temp, None
    
  except IndexError:
    print("No star found in the region you click! Try again")
    temp = Point(None, None)
    return temp, None
    
# this value is used to avoid returning of hops even 
# when there is no nearby star (e.g. editor clicking
# somewhere near the borders).
limit_range = 50

# max_stars is the limit put to remove unnessecory 
# faint stars from our star list
max_stars = 50

# limiting_brightness is the minimum brightness below 
# which we consider a star to be faint
limiting_brightness = 0.1

# this function returns a list of stars that lie 
# within the sqaure formed with the click as center

def list_stars(click, data):

  stars_catalogue = pd.DataFrame(columns = ['star','ra','dec','brightness'])

  l_x_limit = int(click.x) - limit_range
  r_x_limit = int(click.x) + limit_range
  l_y_limit = int(click.y) - limit_range
  r_y_limit = int(click.y) + limit_range
  
  for i in range(len(data)):    
    if (data['ra'][i] > l_x_limit and data['ra'][i] < r_x_limit) and (data['dec'][i] > l_y_limit and data['dec'][i] < r_y_limit):
      stars_catalogue = stars_catalogue.append({'star': data['star'][i], 'ra': data['ra'][i], 'dec': data['dec'][i], 'brightness': data['brightness'][i]}, ignore_index=True)

  if len(stars_catalogue) >= max_stars:
     stars_catalogue = stars_catalogue[stars_catalogue['brightness'] > limiting_brightness]

  return stars_catalogue

# Driver code with temp data
data = {'star': ['a', 'b', 'c', 'd'], 'ra': [100, 200, 300, 400], 'dec': [10, 20, 30, 40], 'brightness': [0.1, 0.2, 0.3, 0.4]}
df = pd.DataFrame (data, columns = ['star','ra','dec','brightness'])


global hops

# this function stores the series of hops
# hops is a list of stars as Point object
def save_hops(click, star_catalogue, hops):
  star_point, star_name = min_distance(click, star_catalogue)
  hops = {'star': star_name, 'ra': star_point.x, 'dec': star_point.y}
  return hops
  
  
def main():
  hops = pd.DataFrame(columns = ['star','ra','dec'])
  flag = True
  while(flag):
    x = input()
    y = input()
    flag = input()
    click = Point(x, y)

    stars_catalogue = list_stars(click, df)
    hopped_star = save_hops(click, stars_catalogue, hops)
    hops = hops.append(hopped_star, ignore_index = True)

  return hops
  
print(main())
