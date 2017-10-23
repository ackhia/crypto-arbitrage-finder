

from arblib import *
from time import gmtime, strftime

test_mode = False

def write_arbs(arbs):
    with open("arblog.csv", "a") as f:
        for a in arbs:
            if a["new"]:
                f.write("{},{},{:.2f}%,{},{:.8f},{},{:.8f},{:.8f}\n".format(
                                                                   strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                                                                   a["pair"],
                                                                   a["arb"] * 100,
                                                                   a["lowests_markets"][0]["market"],
                                                                   a["lowests_markets"][0]["price"],
                                                                   a["highest_markets"][0]["market"],
                                                                   a["highest_markets"][0]["price"],
                                                                   a["average_price"]))


if __name__ == "__main__":
    arbs = []
    while True:
        try:
            if test_mode:
                print "********** TEST MODE **********"
            pairs = get_pairs(test_mode)
            arbs = get_arbs(pairs, arbs)
            write_arbs(arbs)
            print "Arbs found: " + str(len(arbs))
            sleep(60)
        except KeyboardInterrupt:
            raise

        except:
            pass
            raise
