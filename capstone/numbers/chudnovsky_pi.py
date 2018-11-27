from decimal import Decimal, getcontext
'''

Using Chudnovsky Algorithm

REF : https://en.wikipedia.org/wiki/Chudnovsky_algorithm

'''

def calc_pi(k):
    '''
        CALCULATE PI USING CHUDNOVSKY ALGORITHM UPTO PRECISION K
    '''
    set_prec_range = 10
    getcontext().prec = k + 1
    
    c = 426880 * Decimal(10005).sqrt()
    m = 1
    l = 13591409
    x = 1
    k = 6
    s = 13591409

    for x in range(1,set_prec_range):
        k += 12
        m = m * Decimal(k**3 - 16*k) / Decimal(k+1)**3
        l += 545140134
        x *= 262537412640768000
        s += Decimal(m * l) / Decimal(x)

    pi = Decimal(c) / Decimal (s)
    return pi



def main():
    '''
        ACCEPT PRECISION FOR CALCULATING THE VALUE OF PI
    '''
    while True:
        try:
            precision = int(input('\nEnter precision to calculatevalue of PI : '))
        except ValueError:
            print('PLEASE ENTER A VALID INPUT')
            continue
        else:
            break

    pi_value = calc_pi(precision)
    print('The value of PI upto precision of {} digits is \n PI = {}'.format(precision, pi_value))


if __name__ == "__main__":
    main()
