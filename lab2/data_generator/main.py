from generator import FakerWrapper, Owner
from generator import Interface
from rich.progress import track


def main():
    interface = Interface()

    # a,b,c = interface.ask_for_input("a","b","c")
    # interface.debug_output_obj()
    # interface.debug_output_table([["name", "a", "b"], ["age", 12, 14], ["tmp", 1, 2]])
    interface.start()


if __name__ == "__main__":
    main()
