import os

from web3 import Web3
from web3.middleware import geth_poa_middleware

import yaml

env = os.getenv('UMBRELLA_ENV')
web3_net = os.getenv('WEB3_NET')

assert env is not None, 'Set UMBRELLA_ENV as "DEV" or "PROD" in environment variables'
assert web3_net is not None, 'Set ethereum net in environment variable WEB3_NET'

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

private_key = config[env]['PRIVATE_KEY']
eth_address = config[env]['ETH_ADDRESS']
chain_id = config[web3_net]['CHAIN_ID']
web3_provider_address = config[web3_net]['URL']

# Connecting to configured net
w3 = Web3(Web3.HTTPProvider(web3_provider_address))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
