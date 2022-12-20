from generator import Interface


def main(): 
    interface = Interface()
    
    # a,b,c = interface.ask_for_input("a","b","c")
    # interface.debug_output_obj()
    interface.print_debug_table([["name", "a", "b"], ["age", 12, 14], ["tmp", 1, 2]])

if __name__ == "__main__": 
    main()