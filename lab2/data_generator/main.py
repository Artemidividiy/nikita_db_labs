from generator import FakerWrapper, Owner
from generator import Interface
from rich.progress import track


def main():
    interface = Interface()

    # a,b,c = interface.ask_for_input("a","b","c")
    # interface.debug_output_obj()
    # interface.debug_output_table([["name", "a", "b"], ["age", 12, 14], ["tmp", 1, 2]])
    interface.debug_output_obj(track(range(10)))

    interface.print_menu()
    owner = Owner()
    print(owner.to_map())


if __name__ == "__main__":
    main()
