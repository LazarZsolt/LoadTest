import pause
import datetime
import sys
import urllib2


def main(args):
    try:
        pause.until(float(args[3]))
        StartTime = datetime.datetime.now() #the start of time measring
        print(str(StartTime))
        try:
            response = urllib2.urlopen(args[2], timeout=float(args[1])) #opening the given url with a given timeout
        except urllib2.URLError as e:
            print(e)
            sys.exit(2)
        if response.code != 200:
            sys.exit(1)

        print(str(datetime.datetime.now()-StartTime))
    except KeyboardInterrupt:
        sys.exit(4)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""This program takes 3 argument:
        - The maximum amount of time waiting for answer
        - The link to open
        - The exact time when it needs to be open as linux timestamp""")
        sys.exit(3)
    main(sys.argv)
    sys.exit(0)