from faker import Faker
from rich.console import Console
from rich.table import Table


class Generator:
    def __init__(self):
        pass


class FakerWrapper:
    def __init__(self):
        self.faker = Faker()


class Interface:
    def __init__(self):
        self.console = Console()

    """ 
        (a, b, c) = interface.ask_for_input("a","b","c")
    """

    def ask_for_input(self, *vars) -> list:
        target = []
        for i in vars:
            self.console.log(f'provide {i=}')
            target.append(input())
        return target

    """ to display table
    vars: list(n, m+1) - table with **column names**
    example:
    ```python
        interface.print_debug_table([["name", a, b], ["age", 12, 24]])
    ```
    | name | age |
    | a    | 12  |
    | b    | 24  |
    """

    def print_debug_table(self, vars: list):
        self.console.log("print_debud_table method: [green] start [/green]")
        target = Table()
        for i in range(len(vars)):
                target.add_column(f'{vars[i][0]}')
            # что я высрал еб твою мать
        for i in range(1, len(vars)): 
            target.add_row(*[str(vars[_][i]) for _ in range(len(vars[i]))])
        
            
        self.console.print(target)
