# -*- coding: utf-8 -*-

"""
Created on 12/21/20 3:54 PM
@Author  : Justin Jiang
@Email   : jw_jiang@pku.edu.com
"""

import csv
import sqlite3


def read_from_tsv(file_path):
    with open(file_path, newline='') as tsv_file:
        data = csv.DictReader(tsv_file, delimiter='\t')
        return data

def main():
    with open('TracksToAdd.tsv', newline='') as tsvfile, sqlite3.connect('./iMusic.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS iMusic(Name varchar(30),AlbumId varchar(30), GenreId varchar(30), Composer varchar(30), Milliseconds varchar(30), UnitPrice varchar(30))")
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            cur.execute(
                "INSERT INTO Track(Name, AlbumId, GenreId, Composer, Milliseconds, UnitPrice) VALUES (?,?,?,?,?,?);",
                [row['Name'], row['AlbumId'], row['GenreId'], row['Composer'], row['Milliseconds'], row['UnitPrice']])
        conn.commit()
    return


if __name__ == '__main__':
    # main()
    file = 'TracksToAdd.tsv'
