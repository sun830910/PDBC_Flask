# -*- coding: utf-8 -*-

"""
Created on 12/21/20 3:54 PM
@Author  : Justin Jiang
@Email   : jw_jiang@pku.edu.com
"""

import csv
import sqlite3
import logging


class tsv_importer(object):
    def __init__(self, tsv_path):
        self.tsv_path = tsv_path

    def read_from_tsv(self):
        try:
            tsv_file = open(self.tsv_path, newline='')
            data = csv.DictReader(tsv_file, delimiter='\t')
            return data
        except Exception as e:
            logging.warning("Can not read from tsv！ {}".format(e))

    @staticmethod
    def write_to_db(data, db_path):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS iMusic(Name varchar(30),AlbumId varchar(30), GenreId varchar(30), Composer varchar(30), Milliseconds varchar(30), UnitPrice varchar(30))")
            for row in data:
                cur.execute(
                    "INSERT INTO Track(Name, AlbumId, GenreId, Composer, Milliseconds, UnitPrice) VALUES (?,?,?,?,?,?);",
                    [row['Name'], row['AlbumId'], row['GenreId'], row['Composer'], row['Milliseconds'],
                     row['UnitPrice']])
            conn.commit()
        return


def main():
    tsv_path = 'TracksToAdd.tsv'
    db_path = "iMusic.db"

    importer = tsv_importer(tsv_path)
    data = importer.read_from_tsv()
    for row in data:
        print(row)
    tsv_importer.write_to_db(data, db_path)


if __name__ == '__main__':
    main()
