import json
import random


class CityPicker:

    def __init__(self, data_path):
        self.cities = []
        with open(data_path, 'r') as file:
            city_data = json.load(file)
            total_population = sum(city['population'] for city in city_data)
            for city in city_data:
                city_name = city['name']
                city_population = city['population']
                city_weight = city_population / total_population
                self.cities.extend([city_name] * int(city_weight * 10000))

    def pick_random_city(self):
        if self.cities:
            return random.choice(self.cities)
        else:
            return None


# Пример использования
data_path = 'input.json'
city_picker = CityPicker(data_path)
selected_city = city_picker.pick_random_city()
if selected_city:
    print(f'Selected city: {selected_city}')
else:
    print('No cities available.')