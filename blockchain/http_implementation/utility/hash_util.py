import hashlib as _hl   # use _ to not export in the module
import json

#__all__ = ['hash_block', 'hash_string_256']

def hash_string_256(string):
    return _hl.sha256(string).hexdigest()

def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.__dict__ for tx in hashable_block['transactions']]
    return  hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())