'''
    Enter a number and have the program fibonacci
'''
import system

system.clear()

def fibo(num):
    a, b = 1, 1
    for k in range (num):
        yield a
        a, b = b, a + b

def main():
    print('Welcome to generate fibonaccci series')

    while True:
        try:
            num = int(input('\nPlease enter number for fibonacci : '))
        except TypeError:
            print('Please enter a valid input')
            continue
        else:
            for fibo_series in fibo(num):
                print('{}\r'.format(fibo_series))
            break


if __name__ == "__main__":
    main()
