import base64
import time

import erdpy.accounts
import requests

import wallet_balance_nft

url = "https://api.elrond.com/accounts/erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz/transactions?size=10000&fields=function,sender&function=stake"
post_url = "https://api.elrond.com/query"
url = requests.get(url).json()
stake_wallet = []
snapshot=[]
wallets=wallet_balance_nft.wallets()
i=0
for wallet in url:
    if wallet['sender'] not in stake_wallet:
        stake_wallet.append(wallet['sender'])
        hex_wallet = erdpy.accounts.Address(wallet['sender']).hex()
        data1 = requests.post(post_url,
                              json={"scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                    "funcName": "getUserStakedNftNonces", "args": [f"{hex_wallet}"]})
        try:
            balance_stake = data1.json()['returnData']
        except:
            balance_stake =[]
        data2 = requests.post(post_url,
                              json={"scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                    "funcName": "getUserUnbondingNftNonces", "args": [f"{hex_wallet}"]})
        try:
            balance_unbonding = data2.json()['returnData']
        except:
            balance_unbonding=[]

        z=balance_stake
        balance_stake.extend(balance_unbonding)
        balance_stake=list(set(balance_stake))
        if len(balance_stake)==14:
            snapshot.append(wallet['sender'])
        else:
            if wallet['sender'] in wallets:
                for indx in range(0,len(balance_stake)):
                    balance_stake[indx]=base64.b64decode(balance_stake[indx]).hex()
                balance_stake.extend(wallet_balance_nft.wallet_balance(wallet['sender']))
                balance_stake = list(set(balance_stake))
                if len(balance_stake)==14:
                    snapshot.append(balance_stake)
        i+=1
        print(i)
        time.sleep(0.6)

if len(wallet_balance_nft.wallets_14nfts())!=0:
    for addr in wallet_balance_nft.wallets_14nfts():
        if addr not in snapshot:
            snapshot.append(addr)
snapshot= open("snapshot.txt", "w")
snapshot.write(f'{snapshot}')
snapshot= open("snapshot.txt", "r")
print(snapshot.read())

