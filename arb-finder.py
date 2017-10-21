

import sys, urllib2, os
from pyquery import PyQuery
from itertools import groupby
from functools import reduce
from time import sleep

test_mode = False
threshold = 0.05
market_display_count = 5

def clear():
    print(chr(27) + "[2J")

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

    
def print_markets(markets):
    i = 1
    for m in markets:
        print str(i )+ ") " + m["market"] + "(" + "{0:.8f}".format(m["price"]) + ")"
        i += 1
    print  
    
    
def beep():
    print('\a')
    
def print_arbs(arbs):
    for a in arbs:
        print
        print "--=== " + a["pair"] + " - " + "{0:.2f}%".format(a["arb"] * 100) + " ===--"
        if a["new"]:
            print "*** NEW ***"
            beep()
        else:
            print
        print "Lowests markets:"
        i = 1
        print_markets(a["lowests_markets"])
        
        print "Highest markets: " 
        print_markets(a["highest_markets"])
        print 
        print "Average price: " + "{0:.8f}".format(a["average_price"])
        
        
def get_currencies():        
    with open("currencies.txt") as f:
        c = f.readline()
        return c.split(",")
    
def get_ignore_list():
    with open("ignorelist.txt") as f:
        lines = f.readlines()
        return [l.split(",") for l in [l.strip() for l in lines]]
    
def get_pairs(ignore_list):
    html = ""
    for c in currencies:
        if test_mode:
            with open(c + ".html") as f:
                html = f.read()
        else:
            url = "https://coinmarketcap.com/currencies/" + c + "/#native"
            rqst = urllib2.urlopen(url)
            html = rqst.read()
      
    pq = PyQuery(html)

    pairs = []
    for e in pq('#markets-table tbody tr').items():
        if e('td:nth-child(7)').text() == "Recently":
            market = e('td:nth-child(2)').text()        
            pair = e('td:nth-child(3)').text()
            
            price = float(e('td:nth-child(5) >span').attr('data-native').strip("$"))
            
            if contains(ignore_list, lambda x: (x[0] == market or x[0] == "*") and (x[1] in pair or x[1] == "*")) == False:
                pairs.append({"market" : market, "pair" : pair, "price" : price })
            
    pairs.sort(key=lambda p: p["pair"])   
    
    return pairs
    
def get_arbs(pairs, old_arbs):
    arbs = []
    for k, g in groupby(pairs, lambda p: p["pair"]):
        group_pairs = list(g)
        if len(group_pairs) > 1:       
            max_price_market = max(group_pairs, key=lambda e: e["price"])
            min_price_market = min(group_pairs, key=lambda e: e["price"])
            average_price_market = float(sum([p["price"] for p in group_pairs])) / len(group_pairs)        
            
            arb =  1 - min_price_market["price"] / max_price_market["price"]        
            
            if arb > threshold:            
                arbs.append({"pair" : k, 
                                   "arb" : arb, 
                                   "highest_markets" : sorted(group_pairs, key=lambda e: e["price"], reverse = True)[:market_display_count], 
                                   "lowests_markets" : sorted(group_pairs, key=lambda e: e["price"])[:market_display_count], 
                                   "average_price" : average_price_market,
                                   "new" : contains(old_arbs, lambda e: e["pair"] == k) == False
                                   })
            
    arbs.sort(key= lambda k: k["arb"], reverse=True)
    
    return arbs
    

if __name__ == "__main__":    
    arbs = []
    while True:
        try:
            clear()
            if test_mode:
                print "********** TEST MODE **********"            
            currencies = get_currencies()
            ignore_list = get_ignore_list()
            pairs = get_pairs(ignore_list)
            arbs = get_arbs(pairs, arbs)
            print_arbs(arbs)
            if len(arbs) == 0:
                print "Nothing found"
            sleep(60)
        except KeyboardInterrupt:            
            raise
        
        except:
            pass
            raise
