import datetime
import hashlib
import json
from flask import Flask, jsonify

LEADING_ZEROS = "000000000000000000"
SPLIT_CHECK = len(LEADING_ZEROS)
# Our Blockchain structure
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
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:SPLIT_CHECK] == LEADING_ZEROS:
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
            if hash_operation[:SPLIT_CHECK] != LEADING_ZEROS:
                return False
            previous_block = curr_block
            block_idx += 1

        return True


# Web app
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Our very first Blockchain
bcn = Blockchain()


# Mining new block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = bcn.get_previous_block()
    previous_proof = previous_block["proof"]

    curr_proof = bcn.proof_of_work(previous_proof=previous_proof)
    previous_hash = bcn.hash(previous_block)

    curr_block = bcn.create_block(curr_proof, previous_hash)

    response = {
        "message": "You mined a block, Buddy!!! ",
        "index": curr_block["index"],
        "timestamp": curr_block["timestamp"],
        "proof": curr_block["proof"],
        "previous_hash": curr_block["previous_hash"]
    }

    return jsonify(response), 200


# fetching full blockchain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
        "chain": bcn.chain,
        "length": len(bcn.chain),
        "timestamp": bcn.chain[-1]['timestamp'] if bcn.chain else "N/A",
        "message": "Blockchain data retrieved successfully.",
    }
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def is_valid():
    b_chain = bcn.chain
    response = {
        "latest-block": b_chain[-1],
        "validity": "VALID" if bcn.is_chain_valid(b_chain) else "INVALID",
        "timestamp": b_chain[-1]['timestamp'] if bcn.chain else "N/A",

    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
