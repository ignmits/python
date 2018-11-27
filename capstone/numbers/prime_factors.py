

def prime_fact(num):
    fact_list = []
    while num != 1:
        for i in range(2,num+1):
            if num % i == 0:
                num = int(num / i)
                fact_list.append(i)
                break
    return fact_list


def main():

    while True:
        try:
            num = int(input('\nPlease enter number to calculate prime factors : '))
        except ValueError:
            print ('Please Enter valid input')
            continue
        else:
            print('Factorial List : {}'.format(prime_fact(num)))
            break


if __name__ == "__main__":
    main()
