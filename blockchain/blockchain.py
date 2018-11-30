#from random import randint
from functools import reduce
# for storing in ordered dictionary format since they are not ordered.To avoid messing up with the hash key generated
from collections import OrderedDict
import json
# to save in binary format
import pickle
#custom imports
from hash_util import hash_block, hash_string_256
#import classes
from block import Block
from transaction import Transaction

#constant for mining rewards
MINING_REWARD = 10
owner = 'Mits'
participants = {'Mits'}
blockchain = []

def get_transaction_value():
    '''
    Accept value from the user to send amount to a recipient via blockchain
    '''
    tx_recipient = input('\nEnter the recipient of the transaction : ')
    tx_amount = float(input('\nEnter the amount please : '))
    return tx_recipient, tx_amount

def add_transaction(recipient, sender = owner, amount = 1.0):
    transaction = Transaction(sender,recipient,amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        #participants.add(sender)
        #participants.add(recipient)
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


def verify_blockchain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block.transactions[:-1],block.previous_hash,block.proof):
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
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str (last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == '00'


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('MINING',owner,MINING_REWARD)
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = Block(len(blockchain),hashed_block,copied_transaction,proof)
    blockchain.append(block)
    return True


def verify_transaction(transaction):
    sender_balance = get_balances(transaction.sender)
    return sender_balance >= transaction.amount


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

def get_balances(participant):
    '''
    Calculate balances for a user.
    Arguments :
        participant : User name to access to access amount as a sender or a receiver        
    '''
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender==participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
    tx_receiver = [[ tx.amount for tx in block.transactions if tx.receiver == participant] for block in blockchain]
    amount_received = 0
    amount_received = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
    return amount_received - amount_sent


def load_data():
    global blockchain
    global open_transactions
    global genesis_block
    try:
        #with open('blockchain.p',mode='rb') as f:
        with open('blockchain.txt',mode='r') as f:
            #file_content = pickle.loads(f.read())
            file_content = f.readlines()
            
            blockchain = json.loads(file_content[0][:-1])
            #print(blockchain)
            updated_blockchain = []
            converted_tx = []
            updated_block = []
            for block in blockchain:
                print('\nnew block : {}'.format(block))
                converted_tx = [Transaction(tx['sender'],tx['receiver'],tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'],block['previous_hash'], converted_tx ,block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            #handling open transactions
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            converted_tx = []
            for tx in open_transactions:
                converted_tx = [Transaction(tx['sender'],tx['receiver'],tx['amount']) for tx in open_transactions]
                updated_tx = Transaction(tx['sender'],tx['receiver'],tx['amount'])
                updated_transactions.append(updated_tx)
            open_transactions = updated_transactions
    except (IOError):
    #genesis block to have the first index block to create a block-chain
        genesis_block = Block(0,'',[],100,0)
        blockchain = [genesis_block]
        open_transactions = []
    #print('Processed Output')
    #print('\nBlock : {}'.format(blockchain))
    #print('\nOpenTransaction : {}'.format(open_transactions))


def save_data():
    #with open('blockchain.p',mode='bw') as f:
    with open('blockchain.txt',mode='w') as f:
        save_chain = [block.__dict__ for block in 
            [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) 
            for block_el in blockchain]
            ]
        f.write(json.dumps(save_chain))
        f.write('\n')
        save_transaction = [tx.__dict__ for tx in open_transactions]
        f.write(json.dumps(save_transaction))
        #to save binary data
        # save_data = {
        #     'chain' : blockchain,
        #     'ot' : open_transactions
        # }
        # f.write(pickle.dumps(save_data))


load_data()


def get_user_choice():
    '''
    Get User choice to perform operations on the Blockchain
    '''
    while True:
        print('\n\tChoose Menu')
        print('\n1. Add a new transaction value')
        print('\n2. Mine a Block')
        print('\n3. Display Chain')
        #print('\n4. Alter Blockchain')
        print('\n5. Validate Blockchain')
        #print('\n6. View Particiapnts')
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
    # elif user_input == '4':
    #     alter_blockchain()
    elif user_input == '5':
        if verify_blockchain():
            print('\nThe Blockchain is Valid')
        else:
            print('\nThe Blockchain has been compromised')
            break
    # elif user_input == '6':
    #     print(participants)
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
