import argparse

# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument("--A1", dest='argument1', help="This is the first argument")
parser.add_argument("--A2", dest="test1", help="this is anotehr argument")
# Parse and print the results
args = parser.parse_args()
test = args.argument1
test2 = args.test1
print(test2)
print(test)
print(args.argument1)

#paser2 = argparse.ArgumentParser()
#parser.add_argument(())