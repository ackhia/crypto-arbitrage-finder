

import sys, urllib2, os
from pyquery import PyQuery
from itertools import groupby
from functools import reduce

test_mode = False
threshold = 0.08
market_display_count = 5

def clear():
    os.system('cls')

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

    
def print_markets(markets):
    i = 1
    for m in markets:
        print str(i )+ ") " + m["market"] + "(" + str(m["price"] )+ ")"
        i += 1
    print  
    
    
def print_arbs(arbs):
    for a in arbs:
        if a["arb"] > threshold:
            print
            print "--=== "+ a["pair"] + " - " + "{0:.2f}%".format(a["arb"] * 100) + " ===--"
            print
            print "Lowests markets:"
            i = 1
            print_markets(a["lowests_markets"])
            
            print "Highest markets: " 
            print_markets(a["highest_markets"])
            print 
        
        
def get_currencies():        
    with open(sys.argv[1]) as f:
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
            url = "https://coinmarketcap.com/currencies/" + c
            rqst = urllib2.urlopen(url)
            html = rqst.read()
      
    pq = PyQuery(html)

    pairs = []
    for e in pq('#markets-table tbody tr').items():
        if e('td:nth-child(7)').text() == "Recently":
            market = e('td:nth-child(2)').text()        
            pair = e('td:nth-child(3)').text()
            pair = pair.replace("BCH", "BCC")
            
            price = float(e('td:nth-child(5)').text().strip("$"))
            
            if contains(ignore_list, lambda x: (x[0] == market or x[0] == "*") and (x[1] in pair or x[1] == "*")) == False:
                pairs.append({"market" : market, "pair" : pair, "price" : price })
            
    pairs.sort(key=lambda p: p["pair"])   
    
    return pairs
    
def get_arbs(pairs):
    arbs = []
    for k, g in groupby(pairs, lambda p: p["pair"]):
        group_pairs = list(g)
        if len(group_pairs) > 1:       
            max_price_market = max(group_pairs, key=lambda e: e["price"])
            min_price_market = min(group_pairs, key=lambda e: e["price"])
            average_price_market = float(sum([p["price"] for p in group_pairs])) / len(group_pairs)        
            
            arb =  1 - min_price_market["price"] / max_price_market["price"]        
            
            arbs.append({"pair" : k, 
                               "arb" : arb, 
                               "highest_markets" : sorted(group_pairs, key=lambda e: e["price"], reverse = True)[:market_display_count], 
                               "lowests_markets" : sorted(group_pairs, key=lambda e: e["price"])[:market_display_count], 
                               "average_price" : average_price_market })
            
    arbs.sort(key= lambda k: k["arb"], reverse=True)
    
    return arbs
    

if __name__ == "__main__":    
    clear()
    currencies = get_currencies()
    ignore_list = get_ignore_list()
    pairs = get_pairs(ignore_list)
    arbs = get_arbs(pairs)
    print_arbs(arbs)
