import pandas as pd 
import csv



def get_matches(book_name):
    books_list = []
    with open('clean_books.csv', 'r') as file_reader:
        flines = file_reader.readline()
        print(flines.rstrip())
        search = file_reader.readlines()

        for i, sline in enumerate(search):
            if book_name.upper() in sline.upper():
                books_list.append(i)
    return books_list


    


