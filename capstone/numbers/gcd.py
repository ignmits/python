from system import clear

clear()

def EuclidGCD(a,b):
    #print(a)
    #print(b)
    if b == 0:
        print(a)
        return a
    else:
        return EuclidGCD(b, a%b)

def main():
    print('\nWelcome to generate  GCD')
    gcd_num = 0
    while True:
        try:
            print('\nEnter number to calcualte GCD')
            num1 = int(input('\nNumber 1 : '))
            num2 = int(input('\nNumber 2 : '))
        except (TypeError, ValueError):
            print('Please enter a valid input')
            break
        else:
            if num1 > num2:
                gcd_num = EuclidGCD(num1,num2)
            else:
                gcd_num = EuclidGCD(num2,num1)
            print('\nThe GCD for {} and {} is : {}\r'.format(num1, num2, gcd_num))


if __name__ == "__main__":
    main()
