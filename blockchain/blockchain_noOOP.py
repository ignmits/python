#from random import randint
from functools import reduce

# for storing in ordered dictionary format since they are not ordered.To avoid messing up with the hash key generated
from collections import OrderedDict

import json

# to save in binary format
import pickle

#custom imports
from hash_util import hash_block, hash_string_256

#constant for mining rewards
MINING_REWARD = 10

owner = 'Mits'
participants = {'Mits'}


def get_transaction_value():
    '''
    Accept value from the user to send amount to a recipient via blockchain

    
    '''
    tx_recipient = input('\nEnter the recipient of the transaction : ')
    tx_amount = float(input('\nEnter the amount please : '))
    return tx_recipient, tx_amount

def add_transaction(recipient, sender = owner, amount = 1.0):
    #transaction = {'sender' : sender,
    #        'recipient':recipient,
    #        'amount':amount}
    transaction = OrderedDict([('sender',sender),('recipient',recipient),('amount',amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        #add into file
        save_data()
        return True
    return False


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
        blockchain[0] = {'previous_hash': '',
                'index':0,
                'transactions': [{'sender':'Amit','recipient':'Vinod','amount':343.343}]
                }




def verify_blockchain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False

        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            return False
    return True


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str (last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    #print(guess_hash)
    return guess_hash[0:2] == '00'



def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()
    #reward_transaction = {
    #        'sender' : 'MINING',
    #        'recipient' : owner,
    #        'amount' : MINING_REWARD
    #        }
    reward_transaction = OrderedDict([('sender','MINING'),('recipient',owner),('amount',MINING_REWARD)])
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = {'previous_hash': hashed_block,
            'index':len(blockchain),
            'transactions':copied_transaction,
            'proof' : proof
            }
    blockchain.append(block)
    return True

def verify_transaction(transaction):
    sender_balance = get_balances(transaction['sender'])
    return sender_balance >= transaction['amount']

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def get_balances(participant):
    '''
    Calculate balances for a user.

    Arguments :
        participant : User name to access to access amount as a sender or a receiver        
    '''
    tx_sender = [[ tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender']==participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0

    amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)

    #citation needed for future again

    #for tx in tx_sender:
    #    if len(tx) == 0:
    #        continue
    #    amount_sent += tx[0]

    tx_receiver = [[ tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0

    amount_received = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
    #for tx in tx_receiver:
    #    if len(tx) == 0:
    #        continue
    #    amount_received += tx[0]
    return amount_received - amount_sent


def load_data():
    try:
        #with open('blockchain.p',mode='rb') as f:
        with open('blockchain.txt',mode='r') as f:
            #file_content = pickle.loads(f.read())
            file_content = f.readline()
            global blockchain
            global open_transactions
            global genesis_block

            #change after adding pickle
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            #below code without pickling
            blockchain = json.loads(file_content[0][:-1])
            blockchain = [{'previous_hash':block['previous_hash'],
                            'index':block['index'],
                            'proof': block['proof'],
                            #ordered dict for transactions
                            'transactions' : [OrderedDict([
                                    ('sender', tx['sender']),
                                    ('recipient',tx['recipient']),
                                    ('amount', tx['amount'])
                            ]) for tx in block['transactions']]
                            } for block in blockchain]

            open_transactions = json.loads(file_content[1])
            open_transactions = [OrderedDict([
                                ('sender', tx['sender']),
                                ('recipient', tx['recipient']),
                                ('amount',tx['amount'])
                                ]) for tx in open_transactions]
    except (IOError, ValueError):
    #genesis block to have the first index block to create a block-chain
        genesis_block = {'previous_hash': '',
            'index':0,
            'transactions': [],
            'proof' : 100
            }
        blockchain = [genesis_block]
        open_transactions = []

def save_data():
    #with open('blockchain.p',mode='bw') as f:
    with open('blockchain.txt',mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))

        #to save binary data
        # save_data = {
        #     'chain' : blockchain,
        #     'ot' : open_transactions
        # }
        # f.write(pickle.dumps(save_data))

#try:
load_data()
# except:
#     genesis_block = {'previous_hash': '',
#             'index':0,
#             'transactions': [],
#             'proof' : 100
#             }
#     blockchain = [genesis_block]
#     open_transactions = []

def get_user_choice():
    '''
    Get User choice to perform operations on the Blockchain
    '''
    while True:
        print('\n\tChoose Menu')
        print('\n1. Add a new transaction value')
        print('\n2. Mine a Block')
        print('\n3. Display Chain')
        print('\n4. Alter Blockchain')
        print('\n5. Validate Blockchain')
        print('\n6. View Particiapnts')
        print('\n7. Verify Transactions')
        print('\nQ. Quit')
        ch = input('\nEnter Choice : ')
        
        if ch not in ('1','2','3','4','q','Q','5','6','7'):
            print('Invalid Choice. Try Again.')
        else:
            return ch


while True:
    user_input = get_user_choice()
    if user_input == '1':
        tx_data = get_transaction_value()
        #unpacking tuple
        recipient, amount = tx_data
        if add_transaction(recipient,amount=amount):
            print('Transaction Added')
        else:
            print('Transaction Failed')
        #print(open_transactions)
    elif user_input == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_input == '3':
        display_blockchain()
    elif user_input == '4':
        alter_blockchain()
    elif user_input == '5':
        if verify_blockchain():
            print('\nThe Blockchain is Valid')
        else:
            print('\nThe Blockchain has been compromised')
            break
    elif user_input == '6':
        print(participants)
    elif user_input == '7':
        if verify_transactions():
            print('Valid Transactions')
        else:
            print('Invalid Transactions')
    else:
        break
    print('New Balance for {} : {:10.2f}'.format(owner, get_balances('Mits')))
    if not verify_blockchain():
        print('\nThe Blockchain has been compromised')
        break