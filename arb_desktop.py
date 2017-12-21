

from arblib import *

test_mode = False

def clear():
    print(chr(27) + "[2J")


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


if __name__ == "__main__":
    arbs = []
    while True:
        try:
            clear()
            if test_mode:
                print "********** TEST MODE **********"
            pairs = get_pairs(test_mode)
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
