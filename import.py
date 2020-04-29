from csv import reader
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_csv_rows(filename):
    csvfile = open(filename)
    csvreader = reader(csvfile)
    for row in csvreader:
        yield row


def main():
    engine = create_engine(getenv('DATABASE_URL'))
    db = scoped_session(sessionmaker(bind=engine))

    for i, row in enumerate(get_csv_rows('books.csv')):
        if i > 0:
            db.execute('INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)',
                    {'isbn':row[0], 'title':row[1], 'author':row[2], 'year':row[3]})
    db.commit()



if __name__ == "__main__":
    main()