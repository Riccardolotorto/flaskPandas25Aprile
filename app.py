from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import os
import squarify
import matplotlib.pyplot as plt
df = pd.read_csv("https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/metacritic_games.csv")

@app.route('/')
def home():
    l = list(set(df["platform"]))
    l.sort()
    return render_template("home.html", lista = l)

@app.route('/esercizio1', methods = ["GET"])
def esercizio1():
    piattaforma = request.args.get("piattaforma")
    df1 = df[df["platform"] == piattaforma][["game"]].to_html()
    return render_template("risultato.html", tabella = df1)

@app.route('/esercizio2', methods = ["GET"])
def esercizio2():
    inzio = int(request.args.get("inzio"))
    fine = int(request.args.get("fine"))
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['year'] = pd.DatetimeIndex(df['release_date']).year
    df2 = df[(df["year"] >= inzio) & (df["year"] <= fine)][["game"]].to_html()
    return render_template("risultato.html", tabella = df2)

@app.route('/esercizio3')
def esercizio3():
    df['total_score'] = df['metascore'] + df['user_score']
    df3 = df[df["total_score"] == df["total_score"].max()][["game"]].to_html()
    return render_template("risultato.html", tabella = df3)

@app.route('/esercizio4')
def esercizio4():
    df4 = df.groupby("platform").count()[["game"]].sort_values(by="game", ascending = False).reset_index().to_html()
    return render_template("risultato.html", tabella = df4)

@app.route('/esercizio5', methods = ["GET"])
def esercizio5():
    n = int(request.args.get("numero"))
    d = df.groupby("platform").count()[["game"]].sort_values(by="game", ascending = False).reset_index()
    df5 = d[d["game"] > n][["platform"]].to_html()
    return render_template("risultato.html", tabella = df5)

@app.route('/esercizio6')
def esercizio6():
    dd = df.groupby("platform").count()[["game"]].sort_values(by="game", ascending = False).reset_index()
    #primo grafico
    dati = dd["game"]
    strighe = dd["platform"]
    plt.figure(figsize=(10, 8))
    plt.pie(dati, labels=strighe, autopct='%1.1f%%') 
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    #grafico 2
    colors = ['#91DCEA', '#64CDCC', '#5FBB68', '#F9D23C', '#F9A729', '#FD6F30']
    squarify.plot(sizes = dati, label = strighe, color = colors, alpha=.8)
    plt.axis('off')
    dir = "static/images"
    file_name = "graf2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("grafici.html")

@app.route('/esercizio7', methods = ["GET"])
def esercizio7():
    piatt = request.args.get("piatt")
    genere = request.args.get("genere")
    df7 = df[(df["platform"] == piatt.upper()) & (df["genre"] == genere.capitalize())][["game"]].to_html()
    return render_template("risultato.html", tabella = df7)

@app.route('/esercizio8')
def esercizio8():
    ddd = df.groupby(["genre", "platform"]).count()[["game"]].sort_values(by="game", ascending = False).reset_index()
    ddd['percentuale'] = (ddd["game"] / ddd["game"].sum()) * 100
    df8 = ddd.to_html()
    return render_template("risultato.html", tabella = df8)

@app.route('/esercizio9')
def esercizio9():
    h = df.groupby(["genre", "platform"]).count()[["game"]].sort_values(by="game", ascending = False).reset_index()
    h['percentuale'] = (h["game"] / h["game"].sum()) * 100
    dati2 = h["percentuale"]
    strighe2 = h["platform"] + "/" + h["genre"]
    plt.figure(figsize=(15, 12))
    plt.pie(dati2, labels=strighe2, autopct='%1.1f%%') 
    dir = "static/images"
    file_name = "graf3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 125)
    return render_template("grafico3.html")

@app.route('/esercizio10', methods = ["GET"])
def esercizio10():
    piattaformaCheck = request.args.getlist("piattaformaCheck")
    df10 = df[df["platform"].isin(piattaformaCheck)][["game"]].to_html()
    return render_template("risultato.html", tabella = df10)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)