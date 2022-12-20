from faker import Faker
from rich.console import Console
from rich.table import Table
from rich.style import Style
import random
import json
import psycopg2

currencies = ("рубль(ей)", "доллар(ов)", "евро", "юань(и)")
profiles = ("продуктовый", "галантерейный", "канцелярский",
            "сапожный", "машиностроительный", "фермерский")

OWNER_COUNT = 10000
COOPERATIVE_COUNT = 10000
PARTNERSHIP_COUNT = 10000


class FakerWrapper:
    def __init__(self):
        self.faker = Faker(locale='ru-RU')

    def generate_money(self):
        currency = random.choice(currencies)
        return str(random.randint(1, 200000000)) + f" {currency}"

    def generate_location(self):
        return self.faker.address()

    def generate_region(self): return self.faker.administrative_unit()

    def generate_company_name(self): return self.faker.company()

    def generate_name(self): return self.faker.name()

    def generate_date_time(self): return self.faker.date_object()


class DBWorker:
    def __init__(self, address, port, database_name, user) -> None:
        self.connection = psycopg2.connect(f"dbname={database_name} user={user} port={port} address={address}")
        self.cursor = self.connection.cursor()
    
    def generate_all(self):
        pass


class Cooperative:
    def __init__(self):
        self.fakerWrapper = FakerWrapper()
        self.generate_cooperative()

    """генерирует кооператив
    """

    def generate_cooperative(self):
        self.name = self.fakerWrapper.generate_company_name()
        self.placement = self.fakerWrapper.generate_region()
        self.capital = self.fakerWrapper.generate_money()
        self.workers_count = random.randint(1, 255)
        self.profile = random.choice(profiles)

    def generate_places(self):
        pass

    def to_string(self) -> str:
        return f"{self.name}\n {self.placement}"


class Passport:
    def __init__(self) -> None:
        self.faker = FakerWrapper()
        self.generate_passport()

    def generate_passport(self):
        fullname = self.faker.generate_name()
        self.name = fullname.split(" ")[0]
        self.middle_name = fullname.split(" ")[1]
        self.last_name = fullname.split(" ")[2]
        self.place_code = str(random.randint(100, 999)) + \
            "-" + str(random.randint(100, 999))
        self.given_date = self.faker.generate_date_time()
        self.series = str(random.randint(10, 99)) + str(random.randint(10, 99))
        self.number = random.randint(100000, 999999)

    def to_map(self):
        return self.__dict__


class Owner:
    def __init__(self) -> None:
        self.faker = FakerWrapper()
        self.generate_owner()

    def generate_owner(self):
        self.name = self.faker.generate_name()
        self.adress = self.faker.generate_location()
        self.region = self.faker.generate_region()
        self.passport_data = Passport()

    def to_map(self):
        d = self.__dict__
        d['passport_data'] = self.passport_data.to_map()
        return d


class Partnership:
    def __init__(self) -> None:
        self.cooperative = Cooperative()
        self.owner = Owner()
        self.registration_data = random.randint(1, 1000000)
        self.date = FakerWrapper().generate_date_time()
        self.pie_size = random.randint(1, 1000) / 1000


class Interface:
    def __init__(self):
        self.console = Console()
        self.db_worker = DBWorker()

    """
        (a, b, c) = interface.ask_for_input("a","b","c")
    """

    def ask_for_input(self, *vars) -> list:
        target = []
        for i in vars:
            self.console.log(f'provide {i=}')
            target.append(input())
        return target

    """prints menu for generator"""

    def print_menu(self):
        table_of_choice = Table(title="Generator menu")
        table_of_choice.add_column("hotkey", style=Style(color="green"))
        table_of_choice.add_column("description")
        with open("./data_generator/configs/menu_config.json", 'r')as f:
            try:
                self.hotkeys = json.load(fp=f)
                for i in list(self.hotkeys.keys()):
                    table_of_choice.add_row(f"{i}", str(self.hotkeys[i]))
                self.console.print(table_of_choice)
            except:
                self.console.log("print_menu method [red] error [/red]")

    def select_variant(self):
        self.print_menu()
        variant = self.ask_for_input("variant")
        while variant not in list(self.hotkeys.keys()):
            self.console.clear()
            self.console.print("[orange] wrong input [/orange]")
            self.print_menu()
            variant = self.ask_for_input("variant")
        match variant:
            case "0":
                self.shutdown()
            case "1":
                self.generator.generate_all()
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass

    def shutdown(self):
        self.console.print("[green] shutting down [/green]")
        exit()
    """ to display table
    vars: list(n, m+1) - table with **column names**
    example:
    ```python
        interface.debug_output_table([["name", a, b], ["age", 12, 24]])
    ```
    | name | age |
    | a    | 12  |
    | b    | 24  |
    """

    def debug_output_table(self, vars: list):
        self.console.log("print_debud_table method: [green] start [/green]")
        target = Table()
        if (len(vars)) > 10:
            for i in range(5, len(vars) - 5):
                vars.remove(i)
        for i in range(len(vars)):
            target.add_column(f'{vars[i][0]}')
            # что я высрал еб твою мать
        for i in range(1, len(vars)):
            target.add_row(*[str(vars[_][i]) for _ in range(len(vars[i]))])
        self.console.print(target)
        self.console.log("print_debud_table method: [green] end [/green]\n")

    def debug_output_obj(self, value: object):
        try:
            self.console.print(str(value))
        except:
            self.console.log(self.console.log(
                f"debug_output_obj method: [red] error [/red]\nno convert to string for object of type {type(value)}"))
