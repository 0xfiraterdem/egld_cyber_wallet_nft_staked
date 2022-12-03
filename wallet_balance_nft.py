import time

import requests

nft_bilgi = {
    'HOTEL': 'https://api.elrond.com/nfts/CITYNFT-26cded-01/accounts?from=0&size=350',
    'AIR_PORT': 'https://api.elrond.com/nfts/CITYNFT-26cded-02/accounts?from=0&size=350',
    'APARTMENT': 'https://api.elrond.com/nfts/CITYNFT-26cded-03/accounts?from=0&size=350',
    'FIRE_STATION' : 'https://api.elrond.com/nfts/CITYNFT-26cded-04/accounts?from=0&size=350',
    'GAS_STATION' : 'https://api.elrond.com/nfts/CITYNFT-26cded-05/accounts?from=0&size=350',
    'MEDIA_CENTER' : 'https://api.elrond.com/nfts/CITYNFT-26cded-06/accounts?from=0&size=350',
    'SHOPPING_MALL' : 'https://api.elrond.com/nfts/CITYNFT-26cded-07/accounts?from=0&size=350',
    'POLICE_STATION' : 'https://api.elrond.com/nfts/CITYNFT-26cded-08/accounts?from=0&size=350',
    'HOSPITAL' : 'https://api.elrond.com/nfts/CITYNFT-26cded-09/accounts?from=0&size=350',
    'DINER': 'https://api.elrond.com/nfts/CITYNFT-26cded-0a/accounts?from=0&size=350',
    'RESIDENCE': 'https://api.elrond.com/nfts/CITYNFT-26cded-0b/accounts?from=0&size=350',
    'BUS_STATION': 'https://api.elrond.com/nfts/CITYNFT-26cded-0c/accounts?from=0&size=350',
    'NIGHT_CLUP': 'https://api.elrond.com/nfts/CITYNFT-26cded-0d/accounts?from=0&size=350',
    'FINANCE_CENTER': 'https://api.elrond.com/nfts/CITYNFT-26cded-0e/accounts?from=0&size=350'
}

nft_sayi = len(nft_bilgi.keys())
nft_url = [*nft_bilgi.values()]
nft_name = [*nft_bilgi.keys()]
list_wallet=[]
def wallets():
    for i in range(0, nft_sayi):
        url = nft_url[i]
        url = requests.get(url)
        url = url.json()
        for i in url:
            if i['address'] not in list_wallet:
                if 'erd1qqqqqqq' not in i['address']:
                    list_wallet.append(i['address'])
    return list_wallet

def wallet_balance(wallet):
    liste=[]
    for i in range(0, nft_sayi):
        url = nft_url[i]
        url = requests.get(url)
        url = url.json()
        hex_i=hex(i+1)[0:3:2]
        time.sleep(0.1)
        for x in url:
            if wallet in x['address']:
                  liste.append(hex_i)
    return liste

def wallets_14nfts():
    list_14nft=[]
    url1 = nft_url[0]
    url1 = requests.get(url1)
    url1 = url1.json()
    for addr in url1:
        if 'erd1qqqqqqq' not in addr['address']:
            if len(wallet_balance(addr['address'])) == 14:
                list_14nft.append(addr['address'])
    return list_14nft

def wallet_per_nft_balance(wallet,hex):
    indx=int(hex,16)-1
    url = nft_url[indx]
    url = requests.get(url)
    url = url.json()
    time.sleep(0.1)
    for addr in url:
        if 'erd1qqqqqqq' not in addr['address']:
            if wallet in addr['address']:
                return addr['balance']
