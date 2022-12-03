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
        balance_stake.extend(balance_unbonding)
        balance_stake=list(set(balance_stake))
        for indx in range(0, len(balance_stake)):
            balance_stake[indx] = base64.b64decode(balance_stake[indx]).hex()
        if wallet['sender'] not in wallets:
            if len(balance_stake) == 14:
                if len(balance_unbonding) == 0:
                    data3 = requests.post(post_url,json={
                                              "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                              "funcName": "getUserStakedNftBalance", "args": [f"{hex_wallet}"]})
                    data4 = requests.post(post_url,json={
                                                "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                                "funcName": "getUserPoolScore", "args": [f"{hex_wallet}"]})
                    sett =int(int(base64.b64decode(data4.json()['returnData'][0]).hex(),16)-(int(base64.b64decode(data3.json()['returnData'][0]).hex(),16))/7)
                    snapshot.append({"address": f"{wallet['sender']}", "set": f"{sett}"})
                    time.sleep(1)

                else:
                    balance = []
                    for elmn in balance_stake:
                        data5 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        data6 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserUnbondingAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        try:
                            veri1 = int(base64.b64decode(data5.json()['returnData'][0]).hex(),16)
                        except:
                            veri1 =0
                        try:
                            veri2 = int(base64.b64decode(data6.json()['returnData'][0]).hex(),16)
                        except:
                            veri2= 0
                        balance.append(veri1+veri2)
                    snapshot.append({"address": f"{wallet['sender']}", "set": f"{min(balance)}"})
                    time.sleep(1)

        else:
            balance_stake.extend(wallet_balance_nft.wallet_balance(wallet['sender']))
            balance_stake = list(set(balance_stake))
            if len(balance_stake)==14:
                if len(balance_unbonding)==0:
                    balance =[]
                    for elmn in balance_stake:
                        data7 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        try:
                            veri1 = int(base64.b64decode(data7.json()['returnData'][0]).hex(), 16)
                        except:
                            veri1=0
                        veri2 = wallet_balance_nft.wallet_per_nft_balance(wallet['sender'], elmn)
                        if veri2 is not None:
                            veri = veri1+int(veri2)
                        else:
                            veri = veri1
                        balance.append(veri)
                    snapshot.append({"address": f"{wallet['sender']}", "set": f"{min(balance)}"})
                    time.sleep(1)

                else:
                    balance = []
                    for elmn in balance_stake:
                        data5 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        data6 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserUnbondingAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        try:
                            veri1 = int(base64.b64decode(data5.json()['returnData'][0]).hex(), 16)
                        except:
                            veri1 = 0
                        try:
                            veri2 = int(base64.b64decode(data6.json()['returnData'][0]).hex(), 16)
                        except:
                            veri2 = 0
                        veri3 = wallet_balance_nft.wallet_per_nft_balance(wallet['sender'], elmn)
                        if veri3 is not None:
                            veri = veri1+veri2+int(veri3)
                        balance.append(veri1 + veri2)
                    snapshot.append({"address": f"{wallet['sender']}", "set": f"{min(balance)}"})
                    time.sleep(1)

        time.sleep(0.6)


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
