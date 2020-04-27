from csv import reader
from sqlalchemy import create_engine
from os import getenv


def get_csv_rows(filename):
    csvfile = open(filename)
    csvreader = reader(csvfile)
    for row in csvreader:
        yield row

def connect_database(db_url=None):
    if db_url == None:
        db_url = getenv('DATABASE_URL')
    engine = create_engine(db_url)
    return engine

def escape(string):
    pass


def main():
    engine = connect_database('postgres://qhutchfxohvldy:06fb88a98fcb777f47b0cf6c3dd38bf8c6ccc0cd22cb540da4e607bd0b431bd8@ec2-54-197-34-207.compute-1.amazonaws.com:5432/d567u6iinhno1a')
    
    #with engine.begin() as connection:
        #connection.execute('CREATE TABLE books (id SERIAL PRIMARY KEY, isbn INTEGER, title TEXT NOT NULL, author TEXT, year INTEGER);') 
    
    with engine.begin() as connection:
        for i, row in enumerate(get_csv_rows('books.csv')):
            if i > 0:
                escaped_row = []
                for field in row:
                    escaped_row.append(escape(field))
                isbn, title, author, year = escaped_row
                connection.execute('INSERT INTO books (isbn, title, author, year) VALUES ({}, {}, {}, {});'.format(isbn, title, author, year))


if __name__ == "__main__":
    main()