import pandas as pd 
import csv

books = pd.read_csv('books.csv')

print(books.head())

print(books.isnull().sum())

df = books.fillna("Not Available")

print(df.isnull().sum())

df.to_csv('clean_books.csv')

val = df.describe()


print(val)