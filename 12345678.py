def calculate_t_test(x1, x2, s1, s2, n1, n2):
    numerator = abs(x1 - x2)
    denominator = ((s1 ** 2 / n1) + (s2 ** 2 / n2)) ** 0.5
    if denominator == 0:
        return 0  # Avoid division by zero
    t_score = round(numerator / denominator, 4)
    return t_score

def calculate_minkowski_distance(data1, data2, n, p=3):
    distance = 0
    for i in range(n):
        distance += abs(data1[i] - data2[i]) ** p
    minkowski_distance = (distance ** (1/p))
    return round(minkowski_distance, 4)

def calculate_profit_percentage(profit_2020, profit_2021):
    absolute_profit_change = abs(profit_2020 - profit_2021)
    if profit_2020 == 0:
        return 0  # Avoid division by zero
    percentage_change = (absolute_profit_change / profit_2020) * 100
    return round(percentage_change, 4)

def main(csvfile):
    try:
        with open(csvfile, 'r') as file:
            headers = file.readline().strip().lower().split(',')
            country_data = {}
            category_data = {}

            for line in file:
                data = line.strip().split(',')
                country = data[headers.index('country')]
                category = data[headers.index('category')]
                employees = int(data[headers.index('number of employees')])
                median_salary = float(data[headers.index('median salary')])
                profit_2020 = float(data[headers.index('profits in 2020(million)')])
                profit_2021 = float(data[headers.index('profits in 2021(million)')])
                org_id = data[headers.index('organisation id')]

                # Calculate t-test score for profits
                t_test_score = calculate_t_test(profit_2020, profit_2021, 0, 0, 1, 1)

                # Calculate Minkowski distance
                minkowski_distance = calculate_minkowski_distance([employees], [median_salary], 1, p=3)

                # Store t-test score and Minkowski distance for each country
                country_data.setdefault(country, [t_test_score, minkowski_distance])

                # Calculate absolute percentage of profit change
                profit_change_percentage = calculate_profit_percentage(profit_2020, profit_2021)

                # Update category-wise data dictionary
                category_data.setdefault(category, {}).setdefault(org_id, [employees, profit_change_percentage])

            # Calculate ranks within each category based on number of employees and profit change
            for category, org_data in category_data.items():
                sorted_orgs = sorted(org_data.keys(), key=lambda x: (org_data[x][0], -org_data[x][1]), reverse=True)
                for idx, org_id in enumerate(sorted_orgs, start=1):
                    org_data[org_id].append(idx)

            # Return the required dictionaries
            return country_data, category_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}, {}

# Example usage
if __name__ == "__main__":
    csvfile = r"D:\Users\J.I Traders\Desktop\Freelancing\python_organization\Organisations (1).csv"  # Provide the correct file path here
    country_data, category_data = main(csvfile)
    print("Country Data:", country_data)
    print("Category Data:", category_data)
