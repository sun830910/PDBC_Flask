# -*- coding: utf-8 -*-

"""
Created on 12/21/20 5:05 PM
@Author  : Justin Jiang
@Email   : jw_jiang@pku.edu.com
"""

import sqlite3
import regex
import logging


def get_data_from_db(database, table, attribute):
    result = set()
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT {table}.{attribute} FROM {table}".format(table=table, attribute=attribute))
        sql_result = cur.fetchall()
        for idx in sql_result:
            result.add(idx[attribute])
    except Exception as e:
        logging.warning("Can't get {attribute} from {table}: {error}".format(attribute=attribute, table=table, error=e))
    return result


def is_float(sentence):
    pattern = "^\d.*\.\d.*$"
    if regex.search(pattern, sentence) != None:
        return True
    return False


if __name__ == '__main__':
    sample = "1.a3"
    print(is_float(sample))
    sample = "1.03"
    print(is_float(sample))
