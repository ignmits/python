
def check_binary(bin_num):
    for i in str(bin_num):
        if i not in '10':
            return False
    return True

def convert_binary(num):
    dec_num = 0
    power = 0
    while True:
        dec_num += (num%10)*(2**power)
        power += 1
        num = round(num // 10)
        if num == 0:
            return dec_num

def binary_to_decimal():
        try:
            bin_input = int(input('\nEnter a Binary Number : '))
            if check_binary(bin_input):
                print('\nThe decimal for {} is {}'.format(bin_input,convert_binary(bin_input)))
            else:
                print('\nThis is not a valid Binary Number. Please try again.')
        except:
            print('Enter binary number only')

def decimal_to_binary():
    while True:
        #try:
            dec_input = int(input('\nEnter a Decimal Number : '))
            dec_num = dec_input
            bin_str = ''

            while True:
                bin_str = bin_str + str(dec_num % 2)
                dec_num = dec_num // 2
                if dec_num == 0:
                    break

            print('\nThe binary of {} is {}'.format(dec_input,bin_str[::-1]))
        #except:
        #   print('\nThis is not a valid Decimal number. Please try again.')
            break

def display_menu():
    while True:
        print('\n1. Decimal to Binary')
        print('\n2. Binary to Decimal')
        print('\n3. Exit')
        try:
            ch = int(input('\n\nEnter Choice : '))
            if ch not in (1,2,3):
                print('Choice out of range')
                continue
            else:
                return ch
        except ValueError:
            print('\nProvide a valid input.')
            continue

def main():
    while True:
        ch = display_menu()
        if ch == 1:
            decimal_to_binary()
        elif ch == 2:
            binary_to_decimal()
        else:
            break


if __name__ == "__main__":
    main()
