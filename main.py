import pandas as pd
import random
import colorama

# Importowanie danych z pliku CSV
data = pd.read_csv("values.csv", sep=';')

# Przypisanie zmiennych
row1 = data.iloc[0].tolist()  # Wartości przedmiotów
row2 = data.iloc[1].tolist()  # Wagi przedmiotów
row_length = len(row1)

# Pobranie liczby osobników w populacji
population = int(input("Podaj liczebnosc populacji: "))
max_weight = int(input("Podaj maksymalny udzwig np. 15: "))
crossover_probability = float(input("Podaj prawdopodobienstwo krzyzowania np. 0.82: "))
mutation_probability = float(input("Podaj prawdopodobienstwo mutacji np. 0.15: "))
iteration_number = int(input("Podaj liczbe iteracji np. 20: "))

# Tworzenie losowych list dla każdego osobnika
for i in range(1, population + 1):
    random_list = [random.randint(0, 1) for _ in range(row_length)]
    globals()[f'list{i}'] = random_list
    globals()[f'list{i}a'] = random_list.copy()

# Pętla główna, która wykonuje 3 iteracje (pokazując ewolucję populacji)
for generation in range(1, iteration_number+1):
    print(f"\n{colorama.Fore.BLUE}--- Generacja {generation} ---{colorama.Fore.RESET}")

    # Ocena osobników - sumowanie wartości i wagi oraz sprawdzanie przeciążenia
    for i in range(1, population + 1):
        current_list = globals()[f'list{i}']
        current_listAAA = globals()[f'list{i}a']  # Oryginalna lista 0 i 1 dla bieżącego osobnika

        # Obliczanie sumy wartości i wagi
        list1_sum_value = sum(row1[j] if current_list[j] == 1 else 0 for j in range(row_length))
        list1_sum_weight = sum(row2[j] if current_list[j] == 1 else 0 for j in range(row_length))

        # Obsługa przeciążonych plecaków
        while list1_sum_weight >= max_weight:
            print(f"list{i} jest przeciążona")

            # Zmiana losowego elementu z 1 na 0 lub z 0 na 1
            random_index = random.randint(0, row_length - 1)
            current_list[random_index] = 1 - current_list[random_index]

            # Ponowne przeliczenie wartości i wagi po zmianie
            list1_sum_value = sum(row1[j] if current_list[j] == 1 else 0 for j in range(row_length))
            list1_sum_weight = sum(row2[j] if current_list[j] == 1 else 0 for j in range(row_length))

            # Sprawdzenie czy waga jest poniżej lub równa limitowi
            if list1_sum_weight <= max_weight:
                print(f"Po korekcie, list {i} mieści się w limicie wagowym")
            else:
                print(f"Po korekcie, list {i} nadal jest przeciążona")
        else:
            print(f"List {i} jest w normie.")

    # Wyświetlenie populacji
    print("\nPopulacja po ocenie:")
    for i in range(1, population + 1):
        print(globals()[f'list{i}'])

    # Koło ruletki - selekcja osobników
    roulette_temp = []
    roulette_chosen = []
    roulette_values = []
    roulette_random_values = []
    sum_value = 0

    # Sumowanie wartości
    for i in range(1, population + 1):
        current_list = globals()[f'list{i}']

        # Obliczanie sumy wartości
        list1_sum_value = sum(row1[j] if current_list[j] == 1 else 0 for j in range(row_length))

        # Obliczanie sumy
        roulette_temp.append(list1_sum_value)
        sum_value += list1_sum_value

    # Ustawianie przedziałów w liście
    for element in roulette_temp:
        percentage = (element / sum_value) * 100
        roulette_values.append(percentage)

    for i in range(1, len(roulette_values)):
        roulette_values[i] += roulette_values[i - 1]

    # Wypisywanie przedziałów
    print(roulette_values)

    # Losowanie liczb z przedziału 1-100
    for i in range(1, population + 1):
        roulette_random_values.append(random.randint(1, 100))

    # Losowanie i przypisanie osobników do przedziałów
    for random_value in roulette_random_values:
        for idx, value in enumerate(roulette_values):
            if random_value <= value:
                roulette_chosen.append(globals()[f'list{idx + 1}'])
                break

    print("\nPopulacja po selekcji (koło ruletki):")
    for chosen in roulette_chosen:
        print(chosen)

    # Krzyżowanie
    crossover_pairs = []

    if len(roulette_chosen) % 2 != 0:
        print(f"Liczba osobników jest nieparzysta. Ostatni osobnik ({roulette_chosen[-1]}) nie weźmie udziału w krzyżowaniu.")

    # Tworzenie par do krzyżowania (pomijamy ostatniego, jeśli jest nieparzysta liczba osobników)
    for i in range(0, len(roulette_chosen) - 1, 2):
        pair = (roulette_chosen[i], roulette_chosen[i + 1])
        crossover_pairs.append(pair)

    # Lista do przechowywania nowych osobników po krzyżowaniu
    new_generation = []

    # Sprawdzanie i wykonywanie krzyżowania
    for idx, (parent1, parent2) in enumerate(crossover_pairs):
        random_value = random.uniform(0, 1)

        # Wypisywanie wylosowanej liczby
        print(f"Wylosowana liczba dla pary {idx + 1} ({parent1}, {parent2}): {random_value:.4f}")

        # Sprawdzanie, czy krzyżowanie ma się odbyć
        if random_value < crossover_probability:
            crossover_point = random.randint(1, row_length - 1)

            # Tworzenie nowych osobników po krzyżowaniu
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            new_generation.extend([child1, child2])

            print(f"Para {idx + 1} ({parent1}, {parent2}) {colorama.Fore.GREEN}zostanie poddana krzyżowaniu{colorama.Fore.RESET} w punkcie {crossover_point}.")
            print(f"Nowi potomkowie: {child1} oraz {child2}")
        else:
            new_generation.extend([parent1, parent2])
            print(f"Para {idx + 1} ({parent1}, {parent2}) {colorama.Fore.RED}NIE zostanie poddana krzyżowaniu{colorama.Fore.RESET}.")

    # Jeżeli liczba osobników była nieparzysta, ostatni osobnik zostaje w populacji bez zmiany
    if len(roulette_chosen) % 2 != 0:
        print(f"Ostatni osobnik ({roulette_chosen[-1]}) pozostaje w populacji bez krzyżowania.")
        new_generation.append(roulette_chosen[-1])

    # Wyświetlenie nowej generacji po krzyżowaniu
    print("\nNowa generacja po krzyżowaniu:")
    for individual in new_generation:
        print(individual)

    # Mutacja
    for individual in new_generation:
        mutation_value = random.uniform(0, 1)
        if mutation_value <= mutation_probability:
            print(f"Osobnik {individual} {colorama.Fore.GREEN}podlega{colorama.Fore.RESET} mutacji (wylosowana liczba: {mutation_value})")

            # Wykonaj mutację
            index_to_mutate = random.randint(0, len(individual) - 1)
            print(f"Wylosowany indeks: {index_to_mutate}")
            individual[index_to_mutate] = 1 - individual[index_to_mutate]  # Zmieniamy 0 na 1 lub 1 na 0
            print(f"Nowy osobnik po mutacji: {individual}")
        else:
            print(f"Osobnik {individual} {colorama.Fore.RED}nie podlega{colorama.Fore.RESET} mutacji (wylosowana liczba: {mutation_value})")

    # Wyświetlenie nowych osobników po krzyżowaniu i mutacji
    print("\nPopulacja po krzyżowaniu i mutacji:")
    for individual in new_generation:
        print(individual)

# Zaktualizowanie populacji na nową generację
for i in range(1, population + 1):
    globals()[f'list{i}'] = new_generation[i - 1]

# Po zakończeniu X generacji, wybierz najlepszego osobnika z ostatniej generacji
best_individual = None
best_value = 0
best_weight = 0

# Sprawdź każdy osobnik w nowej generacji
for individual in new_generation:
    # Oblicz wartość i wagę osobnika
    individual_value = sum(row1[j] if individual[j] == 1 else 0 for j in range(row_length))
    individual_weight = sum(row2[j] if individual[j] == 1 else 0 for j in range(row_length))

    # Sprawdź, czy osobnik nie przekracza maksymalnej wagi i czy ma większą wartość niż dotychczasowy najlepszy
    if individual_weight <= max_weight and individual_value > best_value:
        best_individual = individual
        best_value = individual_value
        best_weight = individual_weight

# Wyświetl najlepszego osobnika
if best_individual:
    print()
    print(f"{colorama.Fore.BLUE}Najlepszy osobnik po {iteration_number} generacjach:{colorama.Fore.RESET}")
    print(f"{colorama.Fore.BLUE}Osobnik: {best_individual}{colorama.Fore.RESET}")
    print(f"{colorama.Fore.BLUE}Wartość: {best_value}{colorama.Fore.RESET}")
    print(f"{colorama.Fore.BLUE}Waga: {best_weight}{colorama.Fore.RESET}")
else:
    print("Nie znaleziono najlepszego osobnika spełniającego ograniczenia wagowe.")