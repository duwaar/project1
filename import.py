from csv import reader


def main():
    csvfile = open('books.csv')
    csvreader = reader(csvfile)
    for row in csvreader:
        print(row)


if __name__ == "__main__":
    main()