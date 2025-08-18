
import hashlib, json, time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0", data="Genesis Block")

    def create_block(self, data, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
        }
        block["hash"] = self.hash(block)
        self.chain.append(block)
        return block

    def hash(self, block):
        block_copy = block.copy()
        block_copy.pop("hash", None)
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()

    def get_last_block(self):
        return self.chain[-1]
