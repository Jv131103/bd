import os
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

#Configurando o MySQL
app.config["MYSQL_DATABASE_USER"] = 'root'
app.config["MYSQL_DATABASE_PASSWORD"] = 'mudar123'
app.config["MYSQL_DATABASE_DB"] = 'teste'
app.config["MYSQL_DATABASE_HOST"] = 'db'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template("aulamvc.html")


@app.route("/gravar", methods=["POST", "GET"])
def listar():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    if nome and email and senha:
        conect = mysql.connect()
        cursor = conect.cursor()
        cursor.execute('insert into tbl_user (user_name, user_username, user_password) VALUES (%s, %s, %s)', (nome, email, senha))
        conect.commit()
    return render_template('aulamvc.html')


@app.route("/listar", methods=["POST", "GET"])
def list():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_user")  # Substitua 'sua_tabela' pelo nome da tabela que você deseja consultar
        data = cursor.fetchall()
        conn.commit()
        return render_template("lista.html", datas=data)
    except Exception as e:
        print("Erro ao listar dados:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)
