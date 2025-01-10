import os
import requests
import json
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chain_finding_covalent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Retrieve Covalent API Key from Environment Variable
COVALENT_API_KEY = "Your Api Key"

if not COVALENT_API_KEY:
    logger.error("No Covalent API key found. Please set the COVALENT_API_KEY environment variable.")
    raise ValueError("No Covalent API key found. Please set the COVALENT_API_KEY environment variable.")

# List of all 52 supported networks with their respective Covalent chain IDs
NETWORKS = [
    {
        "name": "Ethereum",
        "chain_id": 1
    },
    {
        "name": "Binance Smart Chain",
        "chain_id": 56
    },
    {
        "name": "Polygon PoS",
        "chain_id": 137
    },
    {
        "name": "Avalanche",
        "chain_id": 43114
    },
    {
        "name": "Fantom Opera",
        "chain_id": 250
    },
    {
        "name": "Arbitrum",
        "chain_id": 42161
    },
    {
        "name": "Optimism",
        "chain_id": 10
    },
    # ... Add all other supported networks ...
]

# Wallet address to query
WALLET_ADDRESS = "0xbEb5Fc579115071764c7423A4f12eDde41f106Ed"

def get_token_balances(chain_id, wallet_address):
    """
    Fetch ERC20 token balances for a given wallet address on a specified chain using Covalent API.

    :param chain_id: Covalent chain ID
    :param wallet_address: Wallet address to query
    :return: List of tokens with non-zero balances
    """
    base_url = f"https://api.covalenthq.com/v1/{chain_id}/address/{wallet_address}/balances_v2/"
    params = {
        'key': COVALENT_API_KEY,
        'nft': False,  # Exclude NFTs
        'no-nft-fetch': True,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get('data', {}).get('items'):
            logger.info(f"No token data found for chain ID {chain_id}.")
            return []

        # Filter tokens with non-zero balance
        tokens_with_balance = [
            token for token in data['data']['items']
            if token.get('balance', '0') != '0' and float(token.get('balance', '0')) > 0
        ]

        return tokens_with_balance

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error for chain ID {chain_id}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception for chain ID {chain_id}: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error for chain ID {chain_id}: {e}")

    return []

def get_chains_with_tokens(wallet_address):
    """
    Identify all chains where the wallet address holds ERC20 tokens.

    :param wallet_address: Wallet address to query
    :return: List of chain names with tokens
    """
    chains_with_tokens = []

    for network in NETWORKS:
        chain_name = network['name']
        chain_id = network['chain_id']

        logger.info(f"Fetching token balances on {chain_name} (Chain ID: {chain_id})...")
        tokens = get_token_balances(chain_id, wallet_address)

        if tokens:
            chains_with_tokens.append(chain_name)
            logger.info(f"Tokens found on {chain_name}: {len(tokens)} token(s)")
        else:
            logger.info(f"No tokens found on {chain_name}.")

    return chains_with_tokens

if __name__ == "__main__":
    logger.info(f"Fetching chain names for wallet address: {WALLET_ADDRESS}...\n")
    chains = get_chains_with_tokens(WALLET_ADDRESS)

    if chains:
        logger.info("\nChains holding tokens for the given address:")
        logger.info(", ".join(chains))
    else:
        logger.info("\nNo chains found with tokens for the given address or an error occurred.")
