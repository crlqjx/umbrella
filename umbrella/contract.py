import os
import json

from solcx import compile_standard
from umbrella import w3, eth_address, private_key, chain_id


class Contract:
    def __init__(self, contract_path: str, contract_name: str):
        self.creator_address = eth_address

        self._path = contract_path
        self._name = contract_name
        self._filename = os.path.basename(self._path)
        self._content = self._read_contract()

    @property
    def abi(self):
        return self._abi

    @property
    def bytecode(self):
        return self._bytecode

    @property
    def factory(self):
        return self._contract_factory

    @property
    def receipt(self):
        return self._transaction_receipt

    def _read_contract(self):
        with open(self._path, 'r') as raw_contract:
            contract_content = raw_contract.read()
        return contract_content

    def _compile_contract(self):

        compiled_contract = compile_standard(
            {
                "language": "Solidity",
                "sources": {str(self._filename): {"content": self._content}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                }
            }
        )

        self._compiled_contract = compiled_contract

    def _get_bytecode(self):
        bytecode = \
            self._compiled_contract["contracts"][self._filename][self._name]["evm"]["bytecode"]["object"]

        self._bytecode = bytecode

    def _save_abi(self, abi_path):
        abi = self._compiled_contract['contracts'][self._filename][self._name]['abi']
        self._abi = abi
        with open(abi_path, 'w') as json_file:
            json.dump(abi, json_file)

    def _factory(self):
        self._contract_factory = w3.eth.contract(abi=self._abi, bytecode=self._bytecode)

    def _build_transaction(self):
        nonce = w3.eth.getTransactionCount(self.creator_address)
        tx_params = self._contract_factory.constructor().buildTransaction({
            "chainId": chain_id,
            "from": self.creator_address,
            "nonce": nonce
        })

        self._transaction_params = tx_params

    def _sign_transaction(self):
        self._signed_transaction = w3.eth.account.sign_transaction(self._transaction_params, private_key=private_key)

    def _send_transaction(self):
        transaction_hash = w3.eth.send_raw_transaction(self._signed_transaction.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        self._transaction_receipt = transaction_receipt

    def compile(self):
        self._compile_contract()
        self._get_bytecode()
        self._save_abi(f"./abis/{self._name}.json")
        self._factory()

    def deploy(self):
        self._build_transaction()
        self._sign_transaction()
        self._send_transaction()
