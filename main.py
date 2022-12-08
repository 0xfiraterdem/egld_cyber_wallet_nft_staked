import base64
import datetime
import time
import ast
import erdpy.accounts
import requests

import wallet_balance_nft

url = "https://api.elrond.com/accounts/erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz/transactions?size=10000&fields=function,sender&function=stake"
url = requests.get(url).json()
post_url = "https://api.elrond.com/query"

stake_wallet = open("Stake_Wallets.txt", "r")
stake_wallet = ast.literal_eval(stake_wallet.read())
for wallet in url:
    if wallet['sender'] not in stake_wallet:
        stake_wallet.append(wallet['sender'])
staking_wallet = open("Stake_Wallets.txt", "w")
staking_wallet.write(f'{stake_wallet}')

wallets = wallet_balance_nft.wallets()
start = datetime.datetime.now()
snapshot = []
i = 0

for wallet in stake_wallet:
    hex_wallet = erdpy.accounts.Address(wallet).hex()
    data1 = requests.post(post_url,
                          json={"scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                "funcName": "getUserStakedNftNonces",
                                "args": [f"{hex_wallet}"]})

    data2 = requests.post(post_url,
                          json={"scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                "funcName": "getUserUnbondingNftNonces", "args": [f"{hex_wallet}"]})

    if wallet not in wallets:
        if 'returnData' in data1.json().keys():
            balance_stake = data1.json()['returnData']
            if 'returnData' not in data2.json().keys():
                if len(balance_stake) == 14:
                    time.sleep(0.5)
                    data3 = requests.post(post_url, json={
                        "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                        "funcName": "getUserStakedNftBalance", "args": [f"{hex_wallet}"]})

                    time.sleep(0.5)
                    data4 = requests.post(post_url, json={
                        "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                        "funcName": "getUserPoolScore", "args": [f"{hex_wallet}"]})
                    a = int(base64.b64decode(data4.json()['returnData'][0]).hex(), 16)
                    b = int(base64.b64decode(data3.json()['returnData'][0]).hex(), 16)
                    sett = int((a - b) / 7)
                    snapshot.append({"address": f"{wallet}", "set": f"{sett}"})
            else:
                balance_unbonding = data2.json()['returnData']
                balance_stake.extend(balance_unbonding)
                balance_stake.extend(balance_unbonding)
                balance_stake = list(set(balance_stake))
                if len(balance_stake) == 14:
                    balance = []
                    for indx in range(0, len(balance_stake)):
                        time.sleep(0.25)
                        elmn = base64.b64decode(balance_stake[indx]).hex()
                        data5 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        time.sleep(0.25)
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
                        balance.append(veri1 + veri2)
                    snapshot.append({"address": f"{wallet}", "set": f"{min(balance)}"})
        else:
            if 'returnData' in data2.json().keys():
                balance_unbonding = data2.json()['returnData']
                if len(balance_unbonding) == 14:
                    balance = []
                    for indx in range(0, len(balance_unbonding)):
                        time.sleep(0.25)
                        elmn = base64.b64decode(balance_unbonding[indx]).hex()
                        data6 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserUnbondingAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        veri = int(base64.b64decode(data6.json()['returnData'][0]).hex(), 16)
                        balance.append(veri)
                    snapshot.append({"address": f"{wallet}", "set": f"{min(balance)}"})
    else:
        if 'returnData' in data1.json().keys():
            balance_stake = data1.json()['returnData']
            if 'returnData' not in data2.json().keys():
                for indx in range(0, len(balance_stake)):
                    balance_stake[indx] = base64.b64decode(balance_stake[indx]).hex()
                balance_stake.extend(wallet_balance_nft.wallet_balance(wallet))
                balance_stake = list(set(balance_stake))
                if len(balance_stake) == 14:
                    balance = []
                    for elmn in balance_stake:
                        time.sleep(0.25)
                        data7 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        try:
                            veri1 = int(base64.b64decode(data7.json()['returnData'][0]).hex(), 16)
                        except:
                            veri1 = 0
                        veri2 = wallet_balance_nft.wallet_per_nft_balance(wallet, elmn)
                        if veri2 is not None:
                            veri = veri1 + int(veri2)
                        else:
                            veri = veri1
                        balance.append(veri)
                    snapshot.append({"address": f"{wallet}", "set": f"{min(balance)}"})
            else:
                balance_unbonding = data2.json()['returnData']
                balance_stake.extend(balance_unbonding)
                balance_stake = list(set(balance_stake))
                for indx in range(0, len(balance_stake)):
                    balance_stake[indx] = base64.b64decode(balance_stake[indx]).hex()
                balance_stake.extend(wallet_balance_nft.wallet_balance(wallet))
                balance_stake = list(set(balance_stake))
                if len(balance_stake) == 14:
                    balance = []
                    for elmn in balance_stake:
                        time.sleep(0.25)
                        data5 = requests.post(post_url, json={
                            "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                            "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                        time.sleep(0.25)
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
                        time.sleep(0.25)
                        veri3 = wallet_balance_nft.wallet_per_nft_balance(wallet, elmn)
                        if veri3 is not None:
                            veri = veri1 + veri2 + int(veri3)
                        else:
                            veri = veri1 + veri2
                        balance.append(veri)
                    snapshot.append({"address": f"{wallet}", "set": f"{min(balance)}"})
        else:
            if 'returnData' in data2.json().keys():
                balance_unbonding = data2.json()['returnData']
                if 'returnData' not in data1.json().keys():
                    for indx in range(0, len(balance_unbonding)):
                        balance_unbonding[indx] = base64.b64decode(balance_unbonding[indx]).hex()
                    balance_unbonding.extend(wallet_balance_nft.wallet_balance(wallet))
                    balance_unbonding = list(set(balance_unbonding))
                    if len(balance_unbonding) == 14:
                        balance = []
                        for elmn in balance_unbonding:
                            time.sleep(0.25)
                            data7 = requests.post(post_url, json={
                                "scAddress": "erd1qqqqqqqqqqqqqpgqsu2vxxx5l3tjgcnjl6mftlz5dtz5cp5s398syqw3gz",
                                "funcName": "getUserStakedAmountPerNonce", "args": [f"{hex_wallet}", f"{elmn}"]})
                            try:
                                veri1 = int(base64.b64decode(data7.json()['returnData'][0]).hex(), 16)
                            except:
                                veri1 = 0
                            time.sleep(0.25)
                            veri2 = wallet_balance_nft.wallet_per_nft_balance(wallet, elmn)
                            if veri2 is not None:
                                veri = veri1 + int(veri2)
                            else:
                                veri = veri1
                            balance.append(veri)
                        snapshot.append({"address": f"{wallet}", "set": f"{min(balance)}"})
    time.sleep(0.5)
    i += 1
    print(f"{i} ", datetime.datetime.now() - start)
print(len(snapshot))
nfts_14 = wallet_balance_nft.wallets_14nfts()
if len(nfts_14) != 0:
    for addr in nfts_14:
        if addr[0] not in snapshot:
            balance = addr[1:]
            snapshot.append({"address": f"{addr[0]}", "set": f"{min(balance)}"})
print(len(snapshot))
ss = open("snapshot.txt", "w")
ss.write(f'{snapshot}')
ss = open("snapshot.txt", "r")
print(ss.read())
print(datetime.datetime.now() - start)

