import math
import random


def funkcja_kwadratowa(x, a, b, c):
    """Funkcja kwadratowa postaci f(x) = a*x^2 + b*x + c"""
    return a * x ** 2 + b * x + c


def symulowane_wyzarzanie(f, x_min, x_max, T_poczatkowa=1000, alpha=0.95,
                          max_iter=1000, T_min=0):
    """
    Implementacja algorytmu symulowanego wyżarzania do znajdowania minimum funkcji.

    Parametry:
    - f: funkcja do minimalizacji
    - x_min, x_max: przedział poszukiwań
    - T_poczatkowa: początkowa temperatura
    - alpha: współczynnik schładzania (0 < alpha < 1)
    - max_iter: maksymalna liczba iteracji
    - T_min: minimalna temperatura (warunek stopu)

    Zwraca:
    - x: znaleziony punkt minimalny
    - f(x): wartość funkcji w punkcie minimalnym
    - temperatury: lista temperatur w kolejnych iteracjach
    - minima: lista najmniejszych wartości funkcji w kolejnych iteracjach
    """
    # Inicjalizacja
    x = random.uniform(x_min, x_max)
    fx = f(x)
    temperatury = [T_poczatkowa]
    minima = [fx]

    T = T_poczatkowa
    najlepszy_x = x
    najlepszy_fx = fx

    iteracja = 0
    print("\nProces schładzania - wartości temperatury i minima funkcji:")
    print(f"Iteracja {iteracja:3d}: T = {T:8.5f}, Min f(x) = {najlepszy_fx:8.5f}")

    while T > T_min and iteracja < max_iter:
        # Generowanie nowego rozwiązania
        x_nowy = x + random.uniform(-1, 1) * T
        x_nowy = max(x_min, min(x_max, x_nowy))

        fx_nowy = f(x_nowy)
        delta = fx_nowy - fx

        # Decyzja o akceptacji
        if delta < 0:
            x, fx = x_nowy, fx_nowy
            if fx < najlepszy_fx:
                najlepszy_x, najlepszy_fx = x, fx
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                x, fx = x_nowy, fx_nowy

        # Schładzanie
        T *= alpha
        temperatury.append(T)
        minima.append(najlepszy_fx)
        iteracja += 1

        # Wyświetlanie informacji co 10 iteracji lub na końcu
        if iteracja % 10 == 0 or T <= T_min or iteracja == max_iter:
            print(f"Iteracja {iteracja:3d}: T = {T:8.5f}, Min f(x) = {najlepszy_fx:8.5f}")

    return najlepszy_x, najlepszy_fx, temperatury, minima


# Pobranie danych od użytkownika
print("Podaj współczynniki funkcji kwadratowej f(x) = a*x^2 + b*x + c")
a = float(input("Współczynnik a: "))
b = float(input("Współczynnik b: "))
c = float(input("Wyraz wolny c: "))


# Utworzenie funkcji
def f(x):
    return funkcja_kwadratowa(x, a, b, c)


# Parametry algorytmu
x_min, x_max = -10, 10
T_poczatkowa = 100
alpha = 0.95
max_iter = 150

# Uruchomienie algorytmu
x_opt, f_opt, temperatury, minima = symulowane_wyzarzanie(f, x_min, x_max,
                                                          T_poczatkowa, alpha, max_iter)

# Wyniki
print("\nPodsumowanie:")
print(f"Znalezione minimum: x = {x_opt:.5f}, f(x) = {f_opt:.5f}")

# Obliczenie teoretycznego minimum (dla porównania)
if a != 0:
    x_teoretyczne = -b / (2 * a)
    y_teoretyczne = f(x_teoretyczne)
    print(f"Minimum teoretyczne: x = {x_teoretyczne:.5f}, f(x) = {y_teoretyczne:.5f}")
    print(f"Różnica w x: {abs(x_opt - x_teoretyczne):.5f}")
    print(f"Różnica w f(x): {abs(f_opt - y_teoretyczne):.5f}")
else:
    print("Funkcja nie jest kwadratowa (a = 0), nie ma minimum globalnego")

# Pełna lista temperatur i minimów (można zakomentować jeśli niepotrzebne)
print("\nPełna lista:")
print("Iteracja | Temperatura | Min f(x)")
print("---------------------------------")
for i, (temp, min_fx) in enumerate(zip(temperatury, minima)):
    print(f"{i:7d} | {temp:10.5f} | {min_fx:8.5f}")