from decimal import Decimal, getcontext
'''

CALCULATE THE VALUE OF 'e'

'''

def calc_e(k):
    '''
        CALCULATE VALUE OF e PRECISION K
    '''
    getcontext().prec = k + 1

    return Decimal(1).exp()



def main():
    '''
        ACCEPT PRECISION TO EVALUATE e
    '''
    while True:
        try:
            precision = int(input('\nEnter precision to evaluate value of e : '))
        except ValueError:
            print('PLEASE ENTER A VALID INPUT')
            continue
        else:
            break

    e_value = calc_e(precision)
    print('The value of e upto precision of {} digits is \n e = {}'.format(precision, e_value))


if __name__ == "__main__":
    main()
