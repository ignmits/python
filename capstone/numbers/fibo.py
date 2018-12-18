'''
    Enter a number and have the program fibonacci
'''
import system

system.clear()



def fibo_rec(n):
    '''
    Calculate fibonacci number for the n.
    Highly in-efficient.
    Takes a lot of time with number as low 35+
    '''
    if n <=1:
        return n
    else:
        return fibo_rec(n-1) + fibo_rec(n-2)

def fibo_list(n):
    # Using Array, inefficient memory management
    # f = [0,1]
    # for n in range(2,n+1):
    #     f.append(f[n-1] + f[n-2])
    # return f[n]
    

    if n <= 1:
        return 0
    a = 0
    b = 1
    for n in range(1,n):
        a, b = b, a+b
    return b

def main():
    print('Welcome to generate  nth fibonaccci number')

    while True:
        try:
            num = int(input('\nPlease enter number to generate fibonacci number : '))
        except TypeError:
            print('Please enter a valid input')
            break
        else:
            print('{}\r'.format(fibo_list(num)))


if __name__ == "__main__":
    main()
