import csv


# Read File
def read_file(filename="census.csv"):
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)



def remove_duplicates(data):
    seen = set()
    unique_data = []
    for row in data:

        key = (row["STNAME"], row["CTYNAME"], row["CENSUS2010POP"])
        if key not in seen:
            seen.add(key)
            unique_data.append(row)
    return unique_data



def count_cities(data):
    city_count = {}

    for row in data:
        state = row["STNAME"]
        city = row["CTYNAME"]


        if state == city and state != "District of Columbia":
            continue

        if state not in city_count:
            city_count[state] = 0

        city_count[state] += 1

    return city_count


def get_high_low_num_city(city_count):
    max_state = max(city_count, key=city_count.get)
    min_state = min(city_count, key=city_count.get)

    print(f"\nState with the highest number of cities: {max_state} ({city_count[max_state]})")
    print(f"State with the lowest number of cities: {min_state} ({city_count[min_state]})")



def total_population_per_state(data):
    population = {}

    for row in data:
        state = row["STNAME"]
        city = row["CTYNAME"]
        pop = int(row["CENSUS2010POP"])


        if state == city and state != "District of Columbia":
            continue

        if state not in population:
            population[state] = 0

        population[state] += pop

    return population



def get_high_low_population_city(data):
    high_pop = {}
    low_pop = {}

    for row in data:
        state = row["STNAME"]
        city = row["CTYNAME"]
        pop = int(row["CENSUS2010POP"])

        if state == city and state != "District of Columbia":
            continue


        if state not in high_pop or pop > high_pop[state][1]:
            high_pop[state] = (city, pop)


        if state not in low_pop or pop < low_pop[state][1]:
            low_pop[state] = (city, pop)

    print("\nCity with the highest population per state:")
    for state, (city, pop) in high_pop.items():
        print(f"{state}: {city} ({pop})")

    print("\nCity with the lowest population per state:")
    for state, (city, pop) in low_pop.items():
        print(f"{state}: {city} ({pop})")


def save_results(city_count, population):
    with open("US2010Census.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["State", "Total Cities", "Total 2010 Population"])

        for state in city_count:
            writer.writerow([state, city_count[state], population.get(state, 0)])

    print("\nResults saved to US2010Census.csv")



def main():
    data = read_file()

    data = remove_duplicates(data)

    city_count = count_cities(data)

    print("\nTotal cities per state:")
    for state, count in city_count.items():
        print(f"{state}: {count}")

    get_high_low_num_city(city_count)
    get_high_low_population_city(data)
    population = total_population_per_state(data)
    save_results(city_count, population)


if __name__ == "__main__":
    main()
