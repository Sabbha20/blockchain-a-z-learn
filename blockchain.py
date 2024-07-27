import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash="0")

    def create_block(self, proof, prev_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": prev_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        if len(self.chain) == 0:
            return "Blockchain is empty"
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_idx = 1
        while block_idx < len(chain):
            curr_block = chain[block_idx]
            if curr_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            curr_proof = curr_block["proof"]
            hash_operation = hashlib.sha256(
                str(curr_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = curr_block
            block_idx += 1
