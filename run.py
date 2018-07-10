import re
import os
import csv
import operator
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup

filename = 'profitability.csv'
try:
	os.remove(filename)
except:
	print('Creating Profitability.csv')
f = open(filename, 'w')



hash_1080ti = {
'c11': 26.11,
'x17': 17.27,
'sib': 18.5,
'lyra2re2': 63/1000,
'xevan': 5.15,
'timetravel': 35.5,
'tribus': 92,
'phi': 30,
'hsr': 18.2,
'bitcore': 20.5,
'skunk': 48,
'blakecoin': 7.6,
'lyra2z': 3.1,
'x16r': 15,
'keccak': 1.2,
'neoscrypt': 1.88,
'daggerhashimoto': 53,
} #GH

nicehash_algo_map = {
0: 'scrypt',
1 : 'sha256',
2 : 'scryptnf',
3 : 'x11',
4 : 'x13',
5 : 'keccak',
6 : 'x15',
7 : 'nist5',
8 : 'neoscrypt',
9 : 'lyra2re',
10 : 'whirlpoolx',
11 : 'qubit',
12 : 'quark',
13 : 'axiom',
14 : 'lyra2re2',
15 : 'scryptjanenf16',
16 : 'blake256r8',
17 : 'blake256r14',
18 : 'blake256r8vnl',
19 : 'hodl',
20 : 'daggerhashimoto',
21 : 'decred',
22 : 'cryptonight',
23 : 'lbry',
24 : 'equihash',
25 : 'pascal',
26 : 'x11gost',
27 : 'sia',
28 : 'blake2s',
29 : 'skunk',
30 : 'cryptonightv7'

}

#Yiimp

yiimp = 'http://api.yiimp.eu/api/status'
yiimp2 = Request(yiimp)
yiimp_html = urlopen(yiimp2)


yiimp_soup = soup(yiimp_html, "html.parser")
yiimp_soup = str(yiimp_soup)
a = yiimp_soup.split('}')
#f.write('Yiimp.eu\n')
for coin in a:
	
	try:
		#print (coin.index('actual_last24h'))
		coin = coin[coin.index('"') + 1:]
		algorithm = coin[:coin.index('"')]
		

		pos_last24h = coin.index('actual_last24h')
		coin = coin[pos_last24h:]
		pos_earning_start = coin.index('0.')
		coin = coin[pos_earning_start:]
		pos_earning_end = coin.index('"')
		actual24hr_earning = coin[:pos_earning_end]
		
		try: 
			temp = float(actual24hr_earning)*hash_1080ti[algorithm]
			mbtc_earning = str(temp)
			hash_rate = str(hash_1080ti[algorithm])
		except:
			mbtc_earning = '0'
			hash_rate = '0'
		f.write('yiimp' + ',' + algorithm + ',' + hash_rate + ',' + actual24hr_earning + ',' + mbtc_earning + '\n')
	except:
		continue

yiimp_html.close()


#Zpool
zpool = 'https://www.zpool.ca/api/status'
zpool2 = Request(zpool, headers={'User-Agent' : "Magic Browser"})
zpool_html = urlopen(zpool2)


zpool_soup = soup(zpool_html, "html.parser")
zpool_soup = str(zpool_soup)
b = zpool_soup.split('}')

#f.write('Zpool.ca\n')
for coin in b:
	try:
		#print (coin.index('actual_last24h'))
		coin = coin[coin.index('"') + 1:]
		algorithm = coin[:coin.index('"')]
		

		pos_last24h = coin.index('actual_last24h')
		coin = coin[pos_last24h:]
		pos_earning_start = coin.index('0.')
		coin = coin[pos_earning_start:]
		pos_earning_end = coin.index('"')
		actual24hr_earning = coin[:pos_earning_end]
		
		try: 
			temp = float(actual24hr_earning)*hash_1080ti[algorithm]
			mbtc_earning = str(temp)
			hash_rate = str(hash_1080ti[algorithm])
		except:
			mbtc_earning = '0'
			hash_rate = '0'
		f.write('zpool' + ',' + algorithm + ',' + hash_rate + ',' + actual24hr_earning + ',' + mbtc_earning + '\n')
	except:
		continue

zpool_html.close()

#Nicehash
nicehash = 'https://api.nicehash.com/api?method=stats.global.24h'
nicehash2 = Request(nicehash, headers={'User-Agent' : "Magic Browser"})
nicehash_html = urlopen(nicehash2)


nh_soup = soup(nicehash_html, "html.parser")
nh_soup = str(nh_soup)
nh_soup = nh_soup[nh_soup.index('[') + 1:nh_soup.index(']')]
c = nh_soup.split('},')

#f.write('Zpool.ca\n')
for coin in c:
	#print (coin)
	try:
		actual24hr_earning = coin[coin.index(':"')+2:coin.index('",')]
		coin = coin[coin.index('algo'):]
		algorithm = nicehash_algo_map[int(coin[coin.index(':')+1:coin.index(',')])]
		mbtc_earning = hash_1080ti[algorithm] * float(actual24hr_earning)
		#print (algorithm)
		f.write('nicehash' + ',' + algorithm + ',' + str(hash_1080ti[algorithm]) + ',' + actual24hr_earning + ',' + str(mbtc_earning) + '\n')
	except:
		continue
		
	
nicehash_html.close()


f.close()
f = open(filename,'r')
unsorted_csv = csv.reader(f,delimiter=',')
sorted_csv = sorted(unsorted_csv,key=operator.itemgetter(4), reverse=True)
f.close()
os.remove(filename)

f = open(filename, 'w')
header = "Pool, Algorithm, Hash Rate, 24h Revenue/MH (mBTC), 24hr Revenue 1080ti (mBTC)\n"
f.write(header)
for row in sorted_csv:
	f.write(', '.join(row)+'\n')
f.close()

