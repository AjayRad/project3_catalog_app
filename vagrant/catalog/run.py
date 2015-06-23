#!flask/bin/python
from catalogapp import app
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="run Falsk app in debug mode",
                    action="store_true")
args = parser.parse_args()


if __name__ == '__main__':
    if args.debug:
        print "debug mode turned on"
        app.debug = True
    else:
        app.debug = False
    app.run(host='0.0.0.0', port=5000)
