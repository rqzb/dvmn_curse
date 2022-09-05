import requests
import json
from sys import argv


class Weather():
    def __init__(self):
        self.location = ''
        self.units = ''
        self.options = ''
        self.language = ''
        self.url = 'https://wttr.in/'

        self.load_config()

    def load_config(self):
        with open('config.json', 'r') as file:
            config_data = json.load(file)

        self.units = config_data['units']        
        self.options = config_data['options']
        self.language = config_data['language']

    def dump_config(self):
        config_data = {
                "units": self.units,
                "options": self.options,
                "language": self.language
            }

        with open('config.json', 'w') as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)
    
    def get_help(self):
        r = requests.get(f'{self.url}:help')
        print(r.text)
    
    def execute(self):
        f_url = f'{self.url}{self.location}?{self.units}{self.options}&lang={self.language}'
        r = requests.get(f_url)
        print(r.text) 

def main():
    script, flag = argv
    weather = Weather() #Я хотел чтобы активация класса прошла здесь, но это не работает 
                        #(функции не видят переменную weather), поэтому в каждой из функции
                        #мне пришлось проинициализировать класс

    functions = {
        "-ml": execute_by_my_location,
        "-l": execute_by_another_location,
        "-u": change_units,
        "-o": change_options,
        "-lang": change_language,
        "-h": show_help
            }

    functions[flag]()

def execute(location:str):
    weather = Weather()
    weather.location = location
    weather.execute()

def execute_by_my_location(*args):
    execute('')

def execute_by_another_location():
    location = input('Please, write place that we looking for: ')
    execute(location)

def change_units():
    units = input('Please, write units that you need: ')

    weather = Weather()
    weather.units = units
    weather.dump_config()

def change_options():
    options = input('Please, write the options you require: ')

    weather = Weather()
    weather.options = options
    weather.dump_config()

def change_language():
     language = input('Please, write language: ')
     
     weather = Weather()
     weather.language = language
     weather.dump_config() 

def show_help():
    help_str = """
     "-ml" execute by my location
     "-l" execute by another location
     "-u" change units
     "-o" change options
     "-lang" change language
    
    You can see options, units and languages down below
    """
    print(help_str)
    user_answer = input('Show help of wttr.in? [Y/n]: ')
    
    if user_answer.lower() == 'y':
        weather = Weather()
        weather.get_help()


if __name__ == '__main__':
    main()

