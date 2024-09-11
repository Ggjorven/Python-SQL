import sys
import sqlite3

s_DataBase = sqlite3.connect("TODO")

def main(argv: list[str]):
    print("------------------------")
    print("Temporary main function.")
    print("------------------------")

if __name__ == '__main__':
    main(sys.argv)