

if __name__ == "__main__":
    formula_str = input("Enter a Horn formula: ")
    formula = parse_horn(formula_str)
    if is_satisfiable(formula):
        print("The formula is satisfiable.")
    else:
        print("The formula is not satisfiable.")