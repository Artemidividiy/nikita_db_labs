from faker import Faker
from rich.console import Console
from rich.table import Table
from rich.style import Style
import random
from datetime import datetime
from rich.progress import track
import json
import psycopg2
from psycopg2.extensions import AsIs
from os.path import isfile, join
from os import listdir
currencies = ("рубль(ей)", "доллар(ов)", "евро", "юань(и)")
profiles = ("продуктовый", "галантерейный", "канцелярский",
            "сапожный", "машиностроительный", "фермерский")
positions = ("директор", "уборщик", "менеджер")

OWNER_COUNT = 10000
COOPERATIVE_COUNT = 100_000
PARTNERSHIP_COUNT = 100_000
WORKER_COUNT = 10000
PASSPORT_COUNT = OWNER_COUNT + WORKER_COUNT

MAX_DATES_FOR_MONTS = {
    1: 31, 2: 28,
    3: 31, 4: 30,
    5: 31, 6: 30,
    7: 31, 8: 31,
    9: 30, 10: 31,
    11: 30, 12: 31
}

# todo: сгенерированы паспорты, кооперативы, владельцы, партнерства, 


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

    def generate_date_time(self):
        current_moment = datetime.now()
        year = random.randint(1999, current_moment.year)
        if year is current_moment.year:
            month = random.randint(1, current_moment.month)
        else:
            month = random.randint(1, 12)
        if (month == current_moment.month):
            day = random.randint(1, current_moment.day)
        else:
            day = random.randint(1, MAX_DATES_FOR_MONTS[month])
        if day == current_moment.day:
            hour = random.randint(0, current_moment.hour)
        else:
            hour = random.randint(0, 23)
        if hour == current_moment.hour:
            minute = random.randint(0, current_moment.minute)
        else:
            minute = random.randint(0, 59)
        if minute == current_moment.minute:
            second = random.randint(0, current_moment.second)
        else:
            second = random.randint(0, 59)
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def generate_job(self): return self.faker.job()


class DBWorker:
    def __init__(self, host, port, database_name, user) -> None:
        self.logger = Logger()
        self.connection = psycopg2.connect(
            dbname=database_name, user=user, port=port, host=host)
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def drop_table():
        pass
    def delete_table_content(self, table_name: str):
        self.cursor.execute("delete from %s;", (AsIs(table_name),))
    def drop_all(self):
        try:
            self.cursor.execute("""drop table public.cooperatives cascade;""")
            self.cursor.execute("""drop table public.passports cascade;""")
            self.cursor.execute("""drop table public.workers cascade;""")
            self.cursor.execute("""drop table public.owners cascade;""")
            self.cursor.execute(
                """drop table public.workers_cooperatives cascade;""")
            self.cursor.execute("""drop table public.partnerships cascade;""")
        except:
            Console().log("[orange] all tables are already deleted [/orange]")

    def create_all(self):
        self.drop_all()
        create_files = [f for f in listdir(
            "./lab2/scripts") if isfile(join("./scripts", f))]
        with open("./lab2/scripts/create_passports.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        with open("./lab2/scripts/create_cooperatives.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        with open("./lab2/scripts/create_owners.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        with open("./lab2/scripts/create_partnerships.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        with open("./lab2/scripts/create_workers.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        with open("./lab2/scripts/create_worker_cooperatives.sql", 'r') as f:
            self.cursor.execute(f.read())
            f.close()
        # for i in track(range(len(create_files))):
        #     with open(f'./scripts/{create_files[i]}', 'r') as f:
        #         if (f.name.find("insert") == -1):
        #             self.cursor.execute(f.read())

    def fill_passports(self):
        t = datetime.now()
        for i in track(range(PASSPORT_COUNT), description="Generating passports"):
            tmp = Passport()
            self.cursor.execute(
                """INSERT INTO public.passports(
	first_name, middle_name, last_name, place_code, date_given, series, "number", id)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (tmp.name, tmp.middle_name, tmp.last_name, tmp.place_code, tmp.data_given, tmp.series, tmp.number, i))
        Console().log(
            f"[green] {self.fill_passports} done [/green] in [yellow] {datetime.now() - t} [/yellow] ")

    def fill_cooperatives(self):
        t = datetime.now()
        for i in track(range(COOPERATIVE_COUNT), description="Generating cooperatives"):
            tmp = Cooperative()
            self.cursor.execute(
                """INSERT INTO public.cooperatives(
	name, placement, capital, workers_count, profile, id)
	VALUES (%s, %s, %s, %s, %s, %s);""", (tmp.name, tmp.placement, tmp.capital, tmp.workers_count, tmp.profile, i)
            )
        Console().log(f"done in [yellow] {datetime.now() - t}")

    def fill_owners(self):
        t = datetime.now()
        for i in track(range(OWNER_COUNT), description="Generating owners"):
            tmp = Owner()
            self.cursor.execute("""INSERT INTO public.owners(
	id, full_name, address, region, passport_data)
	VALUES (%s, %s, %s, %s, %s);""", (i, tmp.name, tmp.adress, tmp.region, tmp.passport_data))
        Console().log(f"done in [yellow] {datetime.now() - t}")

    def fill_workers(self):
        t = datetime.now()
        for i in track(range(WORKER_COUNT), description="Generating workers"):
            tmp = Worker()
            self.cursor.execute("""INSERT INTO public.workers(
	id, first_name, middle_name, last_name, is_owner, partnership, "position", salary, passport)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (i, tmp.first_name, tmp.middle_name, tmp.last_name, tmp.is_owner, tmp.cooperative, tmp.position, tmp.salary, tmp.passport))
        Console().log(f"done in [yellow] {datetime.now() - t}")

    def fill_partnerships(self):
        t = datetime.now()
        for i in track(range(PARTNERSHIP_COUNT), description="Generating partnerships"):
            tmp = Partnership()
            # self.logger.write_data([f"generated partnership: {i}\n"])
            self.cursor.execute("""INSERT INTO public.partnerships(
	id, owner, cooperative, date, registration_data, pie_size)
	VALUES (%s, %s, %s, %s, %s, %s);""", (i, tmp.owner, tmp.cooperative, tmp.date, tmp.registration_data, tmp.pie_size))
        # self.logger.write_data([f"inserted into database\n"])
        Console().log(f"done in [yellow] {datetime.now() - t}")

    def fill_worker_cooperatives(self):
        t = datetime.now()
        for i in track(range(WORKER_COUNT)):
            tmp = WorkerCooperative()
            self.cursor.execute("""INSERT INTO public.workers_cooperatives(
	id, worker, cooperative)
	VALUES (%s, %s, %s);""", (i, tmp.worker, tmp.cooperative))
        Console().log(f"done in [yellow] {datetime.now() - t}")

    def generate_all(self):
        t = datetime.now()
        self.fill_passports()
        self.fill_cooperatives()
        self.fill_owners()
        self.fill_partnerships()
        self.fill_workers()
        self.fill_worker_cooperatives()
        Console().log(f"done generating in [yellow] {datetime.now() - t}")


class Worker:
    def __init__(self) -> None:
        self.fakerWrapper = FakerWrapper()
        self.generate_worker()

    def generate_worker(self):
        fullname: str = self.fakerWrapper.generate_name()
        self.first_name = fullname.split(" ")[0]
        self.middle_name = fullname.split(" ")[1]
        self.last_name = fullname.split(" ")[2]
        self.is_owner = True if random.randint(0, 10) % 2 == 0 else False
        if (self.is_owner):
            self.cooperative = random.randint(1, PARTNERSHIP_COUNT - 1)
        else:
            self.cooperative = None
        self.job = self.fakerWrapper.generate_job()
        self.position = random.choice(positions)
        self.salary = self.fakerWrapper.generate_money()
        self.passport = random.randint(1, PASSPORT_COUNT - 1)


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


class WorkerCooperative:
    def __init__(self) -> None:
        self.generate_connection()
        self.generate_connection()

    def generate_connection(self):
        self.worker = random.randint(1, WORKER_COUNT - 1)
        self.cooperative = random.randint(1, COOPERATIVE_COUNT - 1)


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
        self.data_given = self.faker.generate_date_time()
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
        self.passport_data = random.randint(1, PASSPORT_COUNT - 1)

    def to_map(self):
        d = self.__dict__
        d['passport_data'] = self.passport_data.to_map()
        return d


class Partnership:
    def __init__(self) -> None:
        self.cooperative = random.randint(1, COOPERATIVE_COUNT - 1)
        self.owner = random.randint(1, OWNER_COUNT - 1)
        self.registration_data = random.randint(1, 1000000)
        # TODO: слишком долго, оптимизировать
        self.date = FakerWrapper().generate_date_time()
        self.pie_size = random.randint(1, 1000) / 1000


class Interface:
    def __init__(self):
        self.console = Console()
        
        self.db_worker = DBWorker(
            host="127.0.0.1", port="8014", user="postgres", database_name="labs")

    def start(self):
        self.select_variant()
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
        with open("./lab2/data_generator/configs/menu_config.json", 'r')as f:
            try:
                self.hotkeys = json.load(fp=f)
                print(self.hotkeys)
                for i in list(self.hotkeys.keys()):
                    table_of_choice.add_row(f"{i}", str(self.hotkeys[i]))
                self.console.print(table_of_choice)
            except:
                self.console.log("print_menu method [red] error [/red]")

    def select_variant(self):
        self.print_menu()
        variant = self.ask_for_input("variant")
        variant = variant[0]
        while variant not in list(self.hotkeys.keys()):
            self.console.clear()
            self.console.print("[orange] wrong input [/orange]")
            self.print_menu()
            variant = self.ask_for_input("variant")
        match variant:
            case "0":
                self.shutdown()
            case "1":
                self.db_worker.generate_all()
                input()
                self.console.clear()
                self.select_variant()
            case "2":
                self.db_worker.create_all()
                input()
                self.console.clear()
                self.select_variant()
            case "3":
                self.db_worker.delete_table_content("owners")
                self.db_worker.fill_owners()
                input()
                self.console.clear()
                self.select_variant()
            case "4":
                self.db_worker.delete_table_content("partnerships")
                self.db_worker.fill_partnerships()
                input()
                self.console.clear()
                self.select_variant()
            case "5":
                self.db_worker.delete_table_content("workers")
                self.db_worker.fill_workers()
                input()
                self.console.clear()
                self.select_variant()
            case "6":
                self.db_worker.delete_table_content("workers_cooperatives")
                self.db_worker.fill_worker_cooperatives()
                input()
                self.console.clear()
                self.select_variant()

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


class Logger: 
    def __init__(self) -> None:
        pass
    
    def write_data(self, *content): 
         with open(f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_log.txt", 'a') as f:
            f.writelines(f"{datetime.now()} {content}")

   