from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS usuarios")
    c.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            senha TEXT
        )
    ''')

    c.execute("""INSERT INTO usuarios(login, senha) VALUES
              ('adminjoao13', 'No_brute_force'),
              ('Joao', '40028922'),
              ('WhiteHat', 'GTHC{xxxx.xxxx.xxxx} '),
              ('MariaDb', 'fsfs324'),
              ('Pedro', '1fewr322'),
              ('GrayHat4x', 'M4sT3R3D'),
              ('RavS2', 'S4wty4949'),
              ('BlueHat4x', 'SQL'),
              ('Flask', 'asd213me'),
              ('Vitor213', '43GSFSA43'),
              ('Carol23', 'DSADSA24'),
              ('BlackHat4x', 'Y0u'),
              ('Lucas','123456789'),
              ('Sqlinjetcion','222222222'),
              ('helloword!','1321fslike')
              """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    mensagem = ""
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        query = f"SELECT * FROM usuarios WHERE login = '{login}' AND senha = '{senha}'"

        conn = sqlite3.connect("usuarios.db")
        c = conn.cursor()
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            return redirect("/painel")
        else:
            mensagem = "Credenciais inválidas! "
    return render_template("sql_injection.html", mensagem=mensagem)


@app.route("/painel", methods=["GET", "POST"])
def painel():
    resultado = ""
    if request.method == "POST":
        comando = request.form["comando"]
        try:
            conn = sqlite3.connect("usuarios.db")
            c = conn.cursor()
            c.execute(comando)
            dados = c.fetchall()
            comando_perigoso = any(x in comando.upper()
                                   for x in ["DELETE", "DROP", "INSERT", "UPDATE"])
            if comando_perigoso:
                resultado = "Vamos jogar direito ,você quer derrubar a base de dados haha!!"
            else:
                resultado = "\n".join([str(linha) for linha in dados])
        except Exception as e:
            resultado = f"Erro: {str(e)}"
    return render_template("painel.html", resultado=resultado)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
