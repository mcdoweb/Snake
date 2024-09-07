import math as m

def which_method(x):
    if x == "Better":
        return 1
    elif x == "Normal":
        return 0
    else:
        quit()

def quit():
    print("Invalid input\n")
    exit(1)

def diffEQ (x, y):
    value = x  + .5*y**2 
    return value

def better_method(h, Startinput, Endinput, Starting_y):
    x_new = Startinput
    y_new = Starting_y
    step = h

    while x_new < Endinput:
        k_1 = diffEQ(x_new, y_new)
        u_n = y_new + step * k_1
        x_new = x_new + h
        k_2 = diffEQ(x_new, u_n)
        y_new = y_new + step * ((k_1 + k_2) / 2)
    return y_new

def normal_method(h, Startinput, Endinput, Starting_y):
    x_new = Startinput
    y_new = Starting_y
    step = h

    while x_new < Endinput:
        y_new = y_new + step * diffEQ(x_new, y_new)
        x_new = x_new + h
    return y_new


Method = input("Enter the method you want to use (Better or Normal): ")
which_method(Method)
h = float(input("Step Size: "))
Startinput = float(input("Starting x: "))
Endinput = float(input("Ending x: "))
Starting_y = float(input("Starting y: "))
if Startinput + h > Endinput:
    print("\nEnding Size is less than the sum of Starting Size and Step Size")
    quit()
if Startinput >= Endinput:
    print("\nStaring Size is greater than Ending Size")
    quit()
if h % (Endinput - Startinput) == 0:
    print("\nInvalid step size, not a multiple of the difference between the starting and ending x values.")
    quit()


if which_method(Method) == 1:
    y_final = better_method(h, Startinput, Endinput, Starting_y)
    print(f"\nThe approximate value of y is: {y_final}\n")
else:
    y_final = normal_method(h, Startinput, Endinput, Starting_y)
    print(f"\nThe approximate value of y is: {y_final}\n")
        