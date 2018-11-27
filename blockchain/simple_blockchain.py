from random import randint

def get_last_blockchain_value():
    return blockchain[-1]

def add_value():
    try:
        amount = float(input('Enter Transaction Value : '))
        if len(blockchain) == 0:
            blockchain.append([[1],amount])
        else:
            blockchain.append([get_last_blockchain_value(),amount])
    except:
        print('Invaid amount .....')

def get_user_choice():
    while True:
        print('\n\tChoose Menu')
        print('\n1. Add a new transaction value')
        print('\n2. Display transaction value')
        print('\n3. Alter Blockchain')
        print('\n4. Validate Blockchain')
        print('\nQ. Quit')
        ch = input('\nEnter Choice : ')
        
        if ch not in ('1','2','3','4','q','Q'):
            print('Invalid Choice. Try Again.')
        else:
            return ch

def display_blockchain():
    if blockchain_exist():
        print('The Blockchain value is : ')
        for block in blockchain:
            print(block)

def blockchain_exist():
    if len(blockchain) == 0:
        print('\nBlockchain not created.')
        return False
    return True

def alter_blockchain():
    if blockchain_exist():
        blockchain[randint(0,len(blockchain)-1)] = [-12]

def verify_blockchain():
    if blockchain_exist():
        for index in range(len(blockchain)-1):
            if index == 0:
                continue
            if blockchain[index][0] == blockchain[index-1]:
                continue
            else:
                return False

        return True

def main():

    while True:
        user_input = get_user_choice()
        if user_input == '1':
            add_value()
        elif user_input == '2':
            display_blockchain()
        elif user_input == '3':
            alter_blockchain()
        elif user_input == '4':
            if verify_blockchain():
                print('\nThe Blockchain is Valid')
            else:
                print('\nThe Blockchain has been compromised')
                break
        else:
            break


if __name__  ==  "__main__":
    blockchain = []
    main()
