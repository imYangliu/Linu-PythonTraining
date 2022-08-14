#collatz数列
import sys

def collatz(number):
    if number % 2 == 0:
        return number//2
    else:
        return 3*number+1

while True:
    try:
        count = 0
        number = int(input("Please input a number:"))
        if(number<=0):
            print(f"error integer,{number} been turn into {-number}")
            number = - number
        while True:
            number = collatz(number)
            count = count + 1
            print(number)
            if number == 1:
                print(f"get 1 after {count} times")
                break
    except ValueError:
        print("error input, program exit!")
        sys.exit()
