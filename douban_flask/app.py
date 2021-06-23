from flask import Flask, render_template
import sqlite3
import jieba
import os

app = Flask(__name__)


mydir =os.path.join(os.path.abspath(os.path.dirname(__file__)),'movie.db')
print(mydir)
@app.route('/')
def index():
    con = sqlite3.connect('movie.db')
    cur = con.cursor()
    sql = 'select instroduction from movie250'
    sql2 = 'select count(cname) from movie250'
    data = cur.execute(sql)
    text = ""
    movie_count = 0
    for item in data:
        text = text + item[0]
    cut = jieba.cut(text)
    string = ' '.join(cut)
    str_count = len(string)
    data2 = cur.execute(sql2)
    for item in data2:
        movie_count = item[0]
    cur.close()
    con.close()
    return render_template('index.html', str_count=str_count, movie_count=movie_count)


@app.route('/index')
def home():
    return index()


@app.route('/movie')
def movie():
    data_list = list()
    con = sqlite3.connect(mydir)
    cur = con.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        data_list.append(item)
    cur.close()
    con.close()
    # print(data_list)
    return render_template("movie.html", movies=data_list)


@app.route('/score')
def score():
    score = list()  # 评分
    num = list()  # 电影数量
    num1= list()  #评价数量
    con = sqlite3.connect(mydir)
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])
    sql = "select SUM(case when rated <=200000 then 1 else 0 end)," \
          "SUM(case when rated>200000 and rated<= 500000  then 1 else 0 end)," \
          "SUM(case when rated >500000 and rated<= 1000000 then 1 else 0 end)," \
          "SUM(case when rated >1000000 then 1 else 0 end)" \
          " from movie250 "
    data = cur.execute(sql)
    for item in data:
        num1.append(item[0])
        num1.append(item[1])
        num1.append(item[2])
        num1.append(item[3])

    cur.close()
    con.close()
    return render_template('score.html', score=score, num=num,num1=num1)


@app.route('/word')
def word():
    return render_template('word.html')


@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run(debug=True)
