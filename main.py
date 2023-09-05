import sqlite3 as sql
from sklearn.svm import SVC
import random
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys




def parse():
    url = "https://aldebaran.ru/genre/nauka_obrazovanie/fizika/?pagenum=2"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    req = urlopen(req, timeout=10).read()

    soup = BeautifulSoup(req, "html.parser")
    items = soup.select("p.booktitle a")
    con = sql.connect("new_articles.db")
    cur = con.cursor()
    for i in items:
        origin = "https://aldebaran.ru"
        link = origin+i.get("href")
        cur.execute(f"INSERT INTO `articles` VALUES('{i.get_text()}', '{origin}', '{link}', 'physics')")

    con.commit()
    cur.close()
    sys.exit()

parse()



headers = []

con = sql.connect("new_articles.db")
cur = con.cursor()

cur.execute("SELECT * FROM `articles`")
rows = cur.fetchall()

for row in rows:
    headers.append(row[0])
y = []
for row in rows:
    if row[3] == "programming":
        y.append("Да")
    else:
        y.append("Нет")
print(y)

vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
X = vectorizer.fit_transform(headers)
clf = SVC(probability=True)
clf.fit(X, y)
print("Исследовать: ")
test = input()
zz = clf.predict_proba(vectorizer.transform([test]))
f = zz[0][0]
ff = round(f, 2)
fff = ff*100
print("Result for ", fff, sep=" ")
