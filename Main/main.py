import sys
import sqlite3

def main(argv: list[str]):
    dataBase = sqlite3.connect("assets/FastFood.s3db")

    cursor = dataBase.cursor()

    for row in cursor.execute("select * from bestelling"):  
        print(row)  
  
    dataBase.close()

if __name__ == '__main__':
    main(sys.argv)