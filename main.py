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

        balance_stake.extend(balance_unbonding)
        balance_stake=list(set(balance_stake))
        for indx in range(0, len(balance_stake)):
            balance_stake[indx] = base64.b64decode(balance_stake[indx]).hex()
        if wallet['sender'] in wallets:
            balance_stake.extend(wallet_balance_nft.wallet_balance(wallet['sender']))
            balance_stake = list(set(balance_stake))
            if len(balance_stake)==14:
                balance =[]
                for elmn in balance_stake:
                    data3 = requests.post(post_url, json={
                        "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                        "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                    veri1 = int(base64.b64decode(data3.json()['returnData'][0]).hex(), 16)
                    veri2 = wallet_balance_nft.wallet_per_nft_balance(wallet['sender'], elmn)
                    if veri2 is not None:
                        veri = veri1+int(veri2)
                    else:
                        veri = veri1
                    balance.append(veri)
                snapshot.append({"address": f"{wallet['sender']}", "set": f"{min(balance)}"})
        else:
            if len(balance_stake) == 14:
                balance = []

                for elmn in balance_stake:
                    data3 = requests.post(post_url,json={
                                              "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                              "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}",f"{elmn}"]})
                    balance.append(int(base64.b64decode(data3.json()['returnData'][0]).hex(),16))
                snapshot.append({"address" : f"{wallet['sender']}", "set" : f"{min(balance)}"})
        time.sleep(1)

if len(wallet_balance_nft.wallets_14nfts())!=0:
    balance=[]
    for addr in wallet_balance_nft.wallets_14nfts():
        for i in snapshot:
            if addr not in i['address']:
                for i in range(0,14):
                    veri = wallet_balance_nft.wallet_per_nft_balance(addr, i)
                    balance.append(veri)
                snapshot.append({"address" : f"{addr}", "set" : f"{min(balance)}"})
                time.sleep(0.6)
print(len(snapshot))
ss= open("snapshot.txt", "w")
ss.write(f'{snapshot}')
ss= open("snapshot.txt", "r")
print(ss.read())

