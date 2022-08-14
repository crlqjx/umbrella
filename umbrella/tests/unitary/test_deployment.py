import os

from umbrella.contract import Contract

contract_path = r'./solidity_contracts/PriceStorage.sol'
contract_name = 'PriceConsumer'
contract = Contract(contract_path, contract_name)


def test_initialize_contract():

    assert contract._name == contract._name
    assert contract._path == contract_path
    assert contract._content is not None


def test_compile_contract():
    contract.compile()
    assert contract.abi
    assert contract.bytecode


def test_deploy_contract():
    assert os.environ['WEB3_NET'] == 'RINKEBY', 'tests must be run on rinkeby testnet'

    contract.deploy()

    assert contract.creator_address == "0x384Fc9cd0B6b2CAA9faD39ABBc3d442dB6f6F1ea"
    assert contract.receipt['from'] == contract.creator_address
    assert contract.receipt['contractAddress']
