from functools import reduce
from collections import OrderedDict
import json
# to save in binary format
import pickle

#custom imports
from utility.hash_util import hash_block
from utility.verification import Verification

#import classes
from block import Block
from transaction import Transaction

#constant for mining rewards
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        #initialize empty blockchain
        self.__chain = []
        #unhandled transactions
        self.__open_transactions = []
        genesis_block = Block(0,'',[],100,0)
        self.__chain = [genesis_block]
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transaction(self):
        return self.__open_transactions[:]

    def load_data(self):
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
                    #print('\nnew block : {}'.format(block))
                    converted_tx = [Transaction(tx['sender'],tx['receiver'],tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'],block['previous_hash'], converted_tx ,block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain   #with property setter and getter
                #handling open transactions
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                converted_tx = []
                for tx in open_transactions:
                    converted_tx = [Transaction(tx['sender'],tx['receiver'],tx['amount']) for tx in open_transactions]
                    updated_tx = Transaction(tx['sender'],tx['receiver'],tx['amount'])
                    updated_transactions.append(updated_tx)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            pass
    
    def save_data(self):
        #with open('blockchain.p',mode='bw') as f:
        with open('blockchain.txt',mode='w') as f:
            save_chain = [block.__dict__ for block in 
                [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) 
                for block_el in self.__chain]
                ]
            f.write(json.dumps(save_chain))
            f.write('\n')
            save_transaction = [tx.__dict__ for tx in self.__open_transactions]
            f.write(json.dumps(save_transaction))
            #to save binary data
            # save_data = {
            #     'chain' : blockchain,
            #     'ot' : open_transactions
            # }
            # f.write(pickle.dumps(save_data))



    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        #use verification class
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balances(self):
        '''
        Calculate balances for a user.
        Arguments :
            participant : User name to access to access amount as a sender or a receiver        
        '''
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender==participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
        tx_receiver = [[ tx.amount for tx in block.transactions if tx.receiver == participant] for block in self.__chain]
        amount_received = 0
        amount_received = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, amount = 1.0):
        transaction = Transaction(sender,recipient,amount)
        if Verification.verify_transaction(transaction, self.get_balances):
            self.__open_transactions.append(transaction)
            #add into file
            self.save_data()
            return True
        return False

    # def blockchain_exist(self):
    #     if len(self.__chain) == 0:
    #         print('\nBlockchain not created.')
    #         return False
    #     return True

    def get_last_blockchain(self):
        if len(self.__chain) < 1:
            return None
        else:
            return self.__chain[-1]

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        copied_transaction = self.__open_transactions[:]
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain),hashed_block,copied_transaction,proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()