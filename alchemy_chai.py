import os
import requests
import json
import logging
from eth_utils import is_address

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chain_finding.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Retrieve Alchemy API Key from Environment Variable
API_KEY = 'm8cl1paDPILQriOpcuxTmCLlmKj2VemA'

if not API_KEY:
    logger.error("No Alchemy API key found. Please set the ALCHEMY_API_KEY environment variable.")
    raise ValueError("No Alchemy API key found. Please set the ALCHEMY_API_KEY environment variable.")

# List of all 52 networks with their respective Alchemy HTTP URLs
NETWORKS = [
    {
        "name": "World Chain",
        "url": "https://worldchain-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Shape",
        "url": "https://shape-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Ethereum",
        "url": "https://eth-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "ZKsync",
        "url": "https://zksync-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Optimism",
        "url": "https://opt-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Polygon PoS",
        "url": "https://polygon-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Geist",
        "url": "https://geist-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Arbitrum",
        "url": "https://arb-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Starknet",
        "url": "https://starknet-mainnet.g.alchemy.com/starknet/version/rpc/v0_7/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Arbitrum Nova",
        "url": "https://arbnova-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Astar",
        "url": "https://astar-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Polygon zkEVM",
        "url": "https://polygonzkevm-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "ZetaChain",
        "url": "https://zetachain-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Fantom Opera",
        "url": "https://fantom-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Mantle",
        "url": "https://mantle-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Berachain",
        "url": "https://berachain-bartio.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Blast",
        "url": "https://blast-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Linea",
        "url": "https://linea-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Zora",
        "url": "https://zora-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Polynomial",
        "url": "https://polynomial-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Base",
        "url": "https://base-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Scroll",
        "url": "https://scroll-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Gnosis",
        "url": "https://gnosis-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Frax",
        "url": "https://frax-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "BNB Smart Chain",
        "url": "https://bnb-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Avalanche",
        "url": "https://avax-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Solana",
        "url": "https://solana-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Metis",
        "url": "https://metis-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "opBNB",
        "url": "https://opbnb-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "CrossFi",
        "url": "https://crossfi-testnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Flow EVM",
        "url": "https://flow-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "ApeChain",
        "url": "https://apechain-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Lens",
        "url": "https://lens-sepolia.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Soneium",
        "url": "https://soneium-minato.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Rootstock",
        "url": "https://rootstock-mainnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Unichain",
        "url": "https://unichain-sepolia.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    {
        "name": "Abstract",
        "url": "https://abstract-testnet.g.alchemy.com/v2/m8cl1paDPILQriOpcuxTmCLlmKj2VemA"
    },
    # Add remaining networks up to 52
]

# Wallet address to query
WALLET_ADDRESS = "0xbEb5Fc579115071764c7423A4f12eDde41f106Ed"

# Validate Wallet Address (Ethereum-based addresses)
if not is_address(WALLET_ADDRESS):
    logger.error("Invalid wallet address format.")
    raise ValueError("Invalid wallet address format.")

def get_token_balances(network_url, wallet_address):
    """
    Fetch ERC20 token balances for a given wallet address on a specified network.

    :param network_url: Alchemy HTTP URL for the network
    :param wallet_address: Wallet address to query
    :return: List of tokens with non-zero balances
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [
            wallet_address,
            "erc20"
        ],
        "id": 1
    }

    try:
        response = requests.post(network_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            error_message = data['error'].get('message', 'Unknown error')
            logger.error(f"Error fetching token balances: {error_message}")
            return []

        tokens = data.get('result', {}).get('tokenBalances', [])
        # Filter tokens with non-zero balance
        tokens_with_balance = []
        for token in tokens:
            try:
                balance_hex = token.get('tokenBalance', '0x0')
                balance_int = int(balance_hex, 16)
                if balance_int > 0:
                    tokens_with_balance.append({
                        "contractAddress": token.get('contractAddress'),
                        "tokenBalance": balance_int
                    })
            except ValueError:
                logger.warning(f"Invalid balance format for token: {token.get('contractAddress')}")
                continue

        return tokens_with_balance

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

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
        network_url = network['url']

        logger.info(f"Fetching token balances on {chain_name}...")
        tokens = get_token_balances(network_url, wallet_address)

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
