def check_prime(num):

    for i in range (2,int(num**0.5+1)):
        if num % i == 0:
            return False
    #return False for i in range (2,num**0.5+1) if num % 2 == 0
    return True

def begin():
    num = 2
    print("\nThe first prime number is {}".format(num))

    while True:
        try:
            ans = input('\nPlease enter y/Y to next prime number : ')
        except ValueError:
            print ('Please Enter valid input')
            continue
        else:
            if ans.upper() != 'Y':
                break
            else:
                while True:
                    num  += 1
                    if check_prime(num):
                        print('The next Prime number is = {}'.format(num))
                        break
                    else:
                        continue


if __name__ == "__main__":
    begin()
