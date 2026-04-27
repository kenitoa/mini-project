user_input_a = input("integer > ")

if user_input_a.isdigit():
    number_input_a = int(user_input_a)
    print("radius : ", number_input_a)
    print("rounded : ", 2 * 3.14 * number_input_a)
    print("area : ", 3.14 * number_input_a * number_input_a)