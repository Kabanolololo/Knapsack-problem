import pandas as pd
import random
import colorama

# Importowanie danych z pliku CSV
data = pd.read_csv("values.csv", sep=';')

# Przypisanie zmiennych
row1 = data.iloc[0].tolist()  # Wartości przedmiotów
row2 = data.iloc[1].tolist()  # Wagi przedmiotów
row_length = len(row1)
max_weight = 18  # Maksymalna dopuszczalna waga plecaka

# Pobranie liczby osobników w populacji
population = int(input("Podaj liczebnosc populacji: "))

# Tworzenie losowych list dla każdego osobnika
for i in range(1, population + 1):
    random_list = [random.randint(0, 1) for _ in range(row_length)]
    globals()[f'list{i}'] = random_list
    globals()[f'list{i}a'] = random_list.copy()

# Ocena osobników - sumowanie wartości i wagi oraz sprawdzanie przeciążenia
for i in range(1, population + 1):
    current_list = globals()[f'list{i}']
    current_listAAA = globals()[f'list{i}a']  # Oryginalna lista 0 i 1 dla bieżącego osobnika

    # Obliczanie sumy wartości i wagi
    list1_sum_value = sum(row1[j] if current_list[j] == 1 else 0 for j in range(row_length))
    list1_sum_weight = sum(row2[j] if current_list[j] == 1 else 0 for j in range(row_length))

    # Wyświetlanie sum wartości i wagi
    #print(f"Suma wartości dla list{i}: {list1_sum_value}")
    #print(f"Suma wagi dla list{i}: {list1_sum_weight}")

    # Obsługa przeciążonych plecaków
    while list1_sum_weight > max_weight:
        print(f"list{i} jest przeciążona")
        #print("Aktualna lista:", current_list)

        # Zmiana losowego elementu z 1 na 0 lub z 0 na 1
        random_index = random.randint(0, row_length - 1)
        current_list[random_index] = 1 - current_list[random_index]  # Zamiana 0 na 1 lub 1 na 0
        #print(f"Zmieniono wartość na pozycji {random_index}, nowa lista:", current_list)

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

#Wyswietlenie list
for i in range(1, population + 1):
    print(globals()[f'list{i}'])

#Pusty print
print()

                                            #Koło ruletki
roulette_temp = []
roulette_chosen = []
roulette_values = []
roulette_random_values = []
sum_value = 0

# Sumumowanie wartosci
for i in range(1, population + 1):
    current_list = globals()[f'list{i}']

    # Obliczanie sumy wartości
    list1_sum_value = sum(row1[j] if current_list[j] == 1 else 0 for j in range(row_length))

    # Obliczanie sumy
    roulette_temp.append(list1_sum_value)
    sum_value += list1_sum_value

# Wyświetlanie sumy wartości
print(f"Suma wartości dla wszystkich list: {sum_value}")

# Ustawianie przedziałów w liscie
for element in roulette_temp:
    percentage = (element / sum_value) * 100
    roulette_values.append(percentage)

for i in range(1, len(roulette_values)):
    roulette_values[i] += roulette_values[i - 1]

print(roulette_values)

# Losowanie X (tyle ile wynosi wartosc populacji) liczb z zakresu 1 - 100
for i in range(1, population + 1):
    roulette_random_values.append(random.randint(1,100))

print(roulette_random_values)

for random_value in roulette_random_values:
    # Ustalanie, do którego przedziału należy wylosowana liczba
    for idx, value in enumerate(roulette_values):
        if random_value <= value:
            roulette_chosen.append(globals()[f'list{idx + 1}'])
            print(f"Wylosowana liczba {random_value} należy do przedziału dla listy {idx + 1}.")
            break

# Wyświetlenie zawartości listy wybranych osobników
print("Wybrane osobniki (roulette_chosen):")
for chosen in roulette_chosen:
    print(chosen)
                                        # Proces krzyzowania, mutacji oraz sprawdzenia wartosci i wagi
#zmienne
#crossover_probability = float(input("Podaj prawdopodobieństwo krzyżowania (wartość od 0 do 1): "))
crossover_probability = 0.82
mutation_probability = 0.15
    #Krzyzowanie
# Sprawdzenie, czy liczba osobników jest parzysta
if len(roulette_chosen) % 2 != 0:
    skipped_individual = roulette_chosen.pop(random.randint(0, len(roulette_chosen) - 1))
    print(f"Liczba osobników jest nieparzysta. Osobnik bez pary: {skipped_individual}")

# Tworzenie listy par do krzyżowania
crossover_pairs = []
for i in range(0, len(roulette_chosen), 2):
    # Tworzenie pary z dwóch kolejnych osobników
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
print(new_generation)

    # Mutacja
for individual in new_generation:
    mutation_value = random.uniform(0, 1)

    # Sprawdzanie, czy wylosowana liczba jest mniejsza lub równa prawdopodobieństwu mutacji
    if mutation_value <= mutation_probability:
        print(
            f"Osobnik {individual} {colorama.Fore.GREEN}podlega{colorama.Fore.RESET} mutacji (wylosowana liczba: {mutation_value})")

        # Wykonaj mutację: Losujemy indeks, który podlega mutacji
        index_to_mutate = random.randint(0, len(individual) - 1)  # Losujemy indeks
        print(f"Wylosowany indeks: {index_to_mutate}")
        individual[index_to_mutate] = 1 - individual[index_to_mutate]  # Zmieniamy 0 na 1 lub 1 na 0

        print(f"Nowy osobnik po mutacji: {individual}")

    else:
        print(
            f"Osobnik {individual} {colorama.Fore.RED}nie podlega{colorama.Fore.RESET} mutacji (wylosowana liczba: {mutation_value})")