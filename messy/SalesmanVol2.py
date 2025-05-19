from math import sin, cos, sqrt, radians, exp
import random
import copy

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

    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return distance


def calculate_total_distance(route, distances):
    """Oblicza całkowitą długość trasy"""
    total_distance = 0
    n = len(route)
    for i in range(n - 1):
        total_distance += distances[route[i]][route[i + 1]]
    total_distance += distances[route[-1]][route[0]]  # Powrót do miasta startowego
    return total_distance


def generate_initial_solution(n, start_index):
    """Generuje losowe rozwiązanie początkowe"""
    solution = list(range(n))
    solution.remove(start_index)
    random.shuffle(solution)
    solution.insert(0, start_index)
    solution.append(start_index)  # Powrót do miasta startowego
    return solution


def get_neighbor_solution(current_solution):
    """Generuje sąsiednie rozwiązanie poprzez zamianę dwóch losowych miast (oprócz startowego)"""
    neighbor = current_solution.copy()

    # Wybierz dwa różne indeksy do zamiany (pomijając pierwszy i ostatni element - miasto startowe)
    idx1, idx2 = random.sample(range(1, len(neighbor) - 1), 2
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

    return neighbor


def simulated_annealing(distances, start_index, initial_temp=10000, cooling_rate=0.99, min_temp=0.1,
                        max_iterations=1000):
    """Implementacja algorytmu symulowanego wyżarzania dla TSP"""
    n = len(distances)
    current_solution = generate_initial_solution(n, start_index)
    current_distance = calculate_total_distance(current_solution, distances)

    best_solution = current_solution.copy()
    best_distance = current_distance

    temp = initial_temp
    iteration = 0

    while temp > min_temp and iteration < max_iterations:
        # Generuj sąsiednie rozwiązanie
        neighbor_solution = get_neighbor_solution(current_solution)
        neighbor_distance = calculate_total_distance(neighbor_solution, distances)

        # Oblicz różnicę w długości trasy
        delta = neighbor_distance - current_distance

        # Jeśli nowe rozwiązanie jest lepsze, zaakceptuj je
        if delta < 0:
            current_solution = neighbor_solution
            current_distance = neighbor_distance

            # Sprawdź czy to nowe najlepsze rozwiązanie
            if current_distance < best_distance:
                best_solution = current_solution.copy()
                best_distance = current_distance
        else:
            # Jeśli gorsze, zaakceptuj z pewnym prawdopodobieństwem
            probability = exp(-delta / temp)
            if random.random() < probability:
                current_solution = neighbor_solution
                current_distance = neighbor_distance

        # Schładzanie
        temp *= cooling_rate
        iteration += 1

    return best_solution, best_distance


def parse_coordinate(coord_str):
    coord_str = coord_str.replace('°', '.').replace("'", '')
    direction = coord_str[-1]
    value = float(coord_str[:-1])

    if direction in ['S', 'W']:
        value = -value

    return value


# Wczytanie danych o miastach
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

# Przygotowanie macierzy odległości
city_coords = [latlon_to_xyz(lat, lon) for name, lat, lon in cities]
n = len(city_coords)
distances = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        distances[i][j] = euclidean_distance(city_coords[i], city_coords[j])

# Interakcja z użytkownikiem
city_a = input("Enter the starting city (City A): ")
city_a_index = None

for i, (name, _, _) in enumerate(cities):
    if name == city_a:
        city_a_index = i
        break

if city_a_index is None:
    print(f"Error: City '{city_a}' not found in the list.")
else:
    print("\nRunning Simulated Annealing algorithm...")
    route, total_distance = simulated_annealing(distances, city_a_index)

    print("\nOptimal route found:")
    for i in route:
        print(cities[i][0])
    print(f"\nTotal distance: {total_distance:.2f} kilometers")