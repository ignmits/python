from functools import reduce
from collections import OrderedDict
import json
# to save in binary format
import pickle
#library to send request through http
import requests

#custom imports
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

#constant for mining rewards
MINING_REWARD = 10


class Blockchain:
    '''
    Blockchain class for blockchain object
    '''
    def __init__(self, public_key, node_id):
        #initialize empty blockchain
        # __ to make it private
        self.__chain = []
        #unhandled transactions
        self.__open_transactions = []
        genesis_block = Block(0,'',[],100,0)
        self.__chain = [genesis_block]
        #key to identify the owner
        self.public_key = public_key
        #to manage peern nodes. __ for private
        self.__peer_nodes = set()
        self.node_id = node_id
        self.load_data()

    @property
    def chain(self):
        '''
        To set chain as the propert of Blockchain Class.
        hence can be accessible directly like class object.
        '''
        return self.__chain[:]


    @chain.setter
    def chain(self, val):
        '''
        Setter property to assign value to the object property directly
        '''
        self.__chain = val

    def get_open_transaction(self):
        '''
        Return list of Open  Transactions.
        '''
        return self.__open_transactions[:]

    def load_data(self):
        try:
            # To open file for reading in binary mode
            # with open('blockchain.p',mode='rb') as f:
            with open('blockchain_{}.txt'.format(self.node_id),mode='r') as f:
                # To read binary data
                # file_content = pickle.loads(f.read())

                # Read all lines of the file
                file_content = f.readlines()
                
                # Read everything except the open chains
                blockchain = json.loads(file_content[0][:-1])
                #print(blockchain)
                updated_blockchain = []
                converted_tx = []
                updated_block = []
                for block in blockchain:
                    #print('\nnew block : {}'.format(block))
                    converted_tx = [Transaction(tx['sender'], tx['receiver'], tx['amount'], tx['signature']) for tx in block['transactions']]
                    updated_block = Block(block['index'],block['previous_hash'], converted_tx ,block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain   #with property setter and getter
                #handling open transactions
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                converted_tx = []
                for tx in open_transactions:
                    converted_tx = [Transaction(tx['sender'], tx['receiver'], tx['amount'], tx['signature']) for tx in open_transactions]
                    updated_tx = Transaction(tx['sender'], tx['receiver'], tx['amount'], tx['signature'])
                    updated_transactions.append(updated_tx)
                self.__open_transactions = updated_transactions
                #read peer nodes from the file
                peer_node = json.loads(file_content[2])
                self.__peer_nodes = set(peer_node)
        except (IOError, IndexError):
            pass
    
    def save_data(self):
        #with open('blockchain.p',mode='bw') as f:
        with open('blockchain_{}.txt'.format(self.node_id),mode='w') as f:
            save_chain = [block.__dict__ for block in 
                [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) 
                for block_el in self.__chain]
                ]
            f.write(json.dumps(save_chain))
            f.write('\n')
            save_transaction = [tx.__dict__ for tx in self.__open_transactions]
            f.write(json.dumps(save_transaction))
            #add peer nodes
            f.write('\n')
            f.write(json.dumps(list(self.__peer_nodes)))
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


    def get_balances(self, sender = None):
        '''
        Calculate balances for a user.
        Arguments :
            participant : User name to access to access amount as a sender or a receiver        
        '''
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
            
        participant = self.public_key
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender==participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
        tx_receiver = [[ tx.amount for tx in block.transactions if tx.receiver == participant] for block in self.__chain]
        amount_received = 0
        amount_received = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, signature, amount, is_receiving = False):
        if self.public_key == None:
            return False
        transaction = Transaction(sender,recipient, amount, signature)
        if Verification.verify_transaction(transaction, self.get_balances):
            self.__open_transactions.append(transaction)
            #add into file
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender':sender, 'recipient':recipient, 'amount':amount, 'signature':signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined')
                    except requests.exceptions.ConnectionError:
                        continue
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
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.public_key, MINING_REWARD, '')
        copied_transaction = self.__open_transactions[:]
        for tx in copied_transaction:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain),hashed_block,copied_transaction,proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self,node):
        '''Add a new node to the peer node network

            Arguments : 
                node : The node URL which should be added
        '''
        self.__peer_nodes.add(node)
        self.save_data()
    
    def remove_peer_node(self, node):
        '''Remove a node from the peer node network

            Arguments : 
                node : The node URL which should be added
        '''
        #discard to avoid failure in case the node does not exist
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_node(self):
        return list(self.__peer_nodes)