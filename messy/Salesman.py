from math import sin, cos, sqrt, radians

a = 6378.137
b = 6356.752
e2 = 1 - (b ** 2 / a ** 2)

def latlon_to_xyz(lat, lon, h=0):
    lat_rad = radians(lat)
    lon_rad = radians(lon)

    N = a / sqrt(1 - e2 * sin(lat_rad) ** 2)

    x = (N + h) * cos(lat_rad) * cos(lon_rad)
    y = (N + h) * cos(lat_rad) * sin(lon_rad)
    z = (b ** 2 / a ** 2 * N + h) * sin(lat_rad)

    return x, y, z

def euclidean_distance(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2

    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance

def nearest_neighbor(cities, distances, start_index):
    n = len(cities)
    visited = [False] * n
    route = []
    total_distance = 0

    current_city = start_index
    route.append(current_city)
    visited[current_city] = True

    while len(route) < n:
        nearest_city = None
        nearest_distance = float('inf')

        for i in range(n):
            if not visited[i]:
                distance = distances[current_city][i]
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_city = i

        if nearest_city is None:
            break

        route.append(nearest_city)
        visited[nearest_city] = True
        total_distance += nearest_distance
        current_city = nearest_city

    total_distance += distances[route[-1]][start_index]
    route.append(start_index)

    return route, total_distance

def parse_coordinate(coord_str):
    coord_str = coord_str.replace('°', '.').replace("'", '')
    direction = coord_str[-1]
    value = float(coord_str[:-1])

    if direction in ['S', 'W']:
        value = -value

    return value

cities = []
with open('citiesTest.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()

        lon_str = parts[-2]
        lat_str = parts[-1]

        name = ' '.join(parts[:-2])

        try:
            lon = parse_coordinate(lon_str)
            lat = parse_coordinate(lat_str)
            cities.append((name, lat, lon))
        except ValueError as e:
            print(f"Skipping line due to parsing error: {line.strip()}")
            print(f"Error: {e}")

city_coords = [latlon_to_xyz(lat, lon) for name, lat, lon in cities]

n = len(city_coords)
distances = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        distances[i][j]= euclidean_distance(city_coords[i], city_coords[j])

city_a = input("Enter the starting city (City A): ")

city_a_index = None

for i, (name, _, _) in enumerate(cities):
    if name == city_a:
        city_a_index = i

if city_a_index is None:
    print(f"Error: City '{city_a}' not found in the list.")
else:
    route, total_distance = nearest_neighbor(cities, distances, city_a_index)
    print(route)
    print("Route:")
    for i in route:
        print(cities[i][0])
    print(f"Total distance: {total_distance:.2f} kilometers")