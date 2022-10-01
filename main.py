from web3 import Web3

import config
import time

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
panabi = config.contract_abi
sender_address = '0xDF7d5f31aeEf70D5BA19D0b5627C119B01E18E0D'



def transactions(sender_address, contract_adress, start_time, trans_amount, private_key):
    tokenToBuy = web3.toChecksumAddress(contract_adress)
    spend = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
    contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
    nonce = web3.eth.get_transaction_count(sender_address)
    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
        0,  # set to 0, or specify minimum amount of token you want to receive - consider decimals!!!
        [spend, tokenToBuy],
        sender_address,
        (int(start_time) + 10000)
    ).buildTransaction({
        'from': sender_address,
        'value': web3.toWei(trans_amount, 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gas': 250000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(web3.toHex(tx_token))


if __name__ == '__main__':
    for key, secret in config.wallets.items():
        transactions(key, config.contract, config.start_time, config.trans_amount, secret)
