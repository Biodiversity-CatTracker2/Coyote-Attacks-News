#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import sqlite3
import sys
import time
# from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv
from tqdm import tqdm


class Database:

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

    def create_db(self) -> None:
        c = self.conn.cursor()
        c.execute('''CREATE TABLE news
                     (title text, link text, published_date text, summary text, language text)'''
                  # noqa: E501
                  )
        self.conn.commit()

    def insert_db(self, data: dict) -> None:
        c = self.conn.cursor()
        c.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?)",
                  (data['title'], data['link'], data['published_date'],
                   data['summary'], data['language']))
        self.conn.commit()

    def get_db(self) -> list:
        c = self.conn.cursor()
        c.execute(f"SELECT * FROM {self.db_name}")
        rows = c.fetchall()
        self.conn.close()
        return rows


def newscatcher_request(token: str,
                        query: str,
                        from_date: str,
                        to_date: str,
                        page: int = 1,
                        page_size: int = 100,
                        media: bool = False,
                        search_in: Optional[str] = 'title',
                        language: str = 'en') -> dict:
    url = "https://newscatcher.p.rapidapi.com/v1/search_enterprise"

    if not search_in:
        search_in = ''

    querystring = {
        "q": query,
        "lang": language,
        "sort_by": "date",
        "from": from_date,
        "to": to_date,
        "page": str(page),
        "page_size": str(page_size),
        "media": media,
        "search_in": search_in
    }

    headers = {
        "X-RapidAPI-Key": token,
        "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return json.loads(response.text)


def run(db_name: str, start_date: str, end_date: str):
    db = Database(db_name=db_name)
    # db.create_db()

    q = '(coyote) AND (bite OR attack OR kill OR chase OR aggressive OR nip)'
    results_1 = newscatcher_request(os.environ['RAPID_API_KEY'],
                                    q,
                                    start_date,
                                    end_date,
                                    page=1)

    if not results_1.get('articles'):
        print(results_1)
        return
    articles = results_1['articles']
    total_pages = results_1['total_pages']
    print(f'Total number of pages for current request: {total_pages}')

    for _page in tqdm(range(2, total_pages + 1)):
        results = newscatcher_request(os.environ['RAPID_API_KEY'],
                                      q,
                                      start_date,
                                      end_date,
                                      page=_page)

        if not results.get('status'):
            print(results)
            continue
        elif results['status'] == 'No matches for your search.':
            print(results)
            continue
        else:
            articles.extend(results['articles'])
            print(f'Added {len(results["articles"])} article...')
        print('Sleeping for 3.5 mins...')
        time.sleep(60 * 3.5)

    if not articles:
        print('No articles found...')
        db.conn.close()
        sys.exit(0)

    articles_unique = []

    for x in articles:
        if all(y['title'].lower() != x['title'].lower()
               for y in articles_unique):
            articles_unique.append(x)

    for article in articles_unique:
        db.insert_db(article)

    db.conn.close()


def opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--db-name',
                        help='Name of the database file',
                        type=str,
                        required=True)
    parser.add_argument('-s',
                        '--start-date',
                        help='Search from this date',
                        type=str,
                        required=True)
    parser.add_argument('-e',
                        '--end-date',
                        help='Search until this date',
                        type=str,
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    load_dotenv()
    args = opts()
    run(args.db_name, args.start_date, args.end_date)
    # example: run('db.sqlite3', '2021-01-01', '2022-12-31')
    # today_date = datetime.today().strftime('%Y-%m-%d')
