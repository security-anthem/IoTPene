import sys, os;
import api
def print_usage():
    print("---------------------")
    print("|       IoTPene     |")
    print("---------------------")
    print("")
    print("Usage:")
    print("Parameters:")
    print("db")

if __name__ == '__main__':
    print("IoTPene")

    if len(sys.argv) < 2:
        print_usage()
    if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
        print_usage()
    if sys.argv[1] == "db":
        api.api_run(sys.argv)

