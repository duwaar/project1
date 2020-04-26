from csv import reader
import sqlalchemy


def get_csv_rows(filename):
    csvfile = open(filename)
    csvreader = reader(csvfile)
    for row in csvreader:
        yield row


def main():
    for row in get_csv_rows('books.csv'):
        print(row)
    



if __name__ == "__main__":
    main()