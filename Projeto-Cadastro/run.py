from flask import Flask, redirect, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD = 'static/assets'
app.config['UPLOAD'] = UPLOAD
app.config['dados_login'] = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route("/home")
def home():
    if not app.config['dados_login']:
        return redirect('/')
    return render_template("home.html", nome_usuario=app.config['dados_login'])

@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/')

@app.route('/voltar')
def voltar():
    return redirect('/consulta1')

@app.route('/voltar2')
def voltar2():
    return redirect('/consulta2')

@app.route('/voltar3')
def voltar3():
    return redirect('/consulta3')

@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = "SELECT * from tb_login WHERE usuario=? AND senha=?"
    cursor.execute(sql, (usuario, senha))
    usuario = cursor.fetchone()
    if usuario:
        app.config['dados_login'] = usuario
        return redirect('/home')
    conexao.close()
    return redirect('/')

@app.route('/cadastro1')
def cadastro1():
    if not app.config['dados_login']:
        return redirect('/')
    return render_template("cadastro_cliente.html", usuario=app.config['dados_login'])

@app.route("/enviar", methods=['POST'])
def enviar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    rua = request.form['rua']
    cidade = request.form['cidade']
    estado = request.form['estado']
    numero = request.form['numero']
    data_cadastro = request.form['data_cadastro']
    cpf = request.form['cpf']
    cep = request.form['cep']
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'INSERT INTO tb_clientes (nome, email, telefone, rua, cidade, estado, numero, data_cadastro, cpf, cep) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(sql, (nome, email, telefone, rua, cidade, estado, numero, data_cadastro, cpf, cep))
    conexao.commit()
    conexao.close()
    return redirect('/consulta1')

@app.route('/consulta1')
def consulta1():
    if not app.config['dados_login']:
        return redirect('/')
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'SELECT * FROM tb_clientes'
    cursor.execute(sql)
    clientes = cursor.fetchall()
    conexao.close()
    return render_template('consulta_cliente.html', clientes=clientes, usuario=app.config['dados_login'])

@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'DELETE FROM tb_clientes WHERE cliente_id = ?'
    cursor.execute(sql, (id,))
    conexao.commit()
    conexao.close()
    return redirect('/consulta1')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        rua = request.form['rua']
        cidade = request.form['cidade']
        estado = request.form['estado']
        numero = request.form['numero']
        data_cadastro = request.form['data_cadastro']
        cpf = request.form['cpf']
        cep = request.form['cep']
        sql = "UPDATE tb_clientes SET nome = ?, email = ?, telefone = ?, rua = ?, cidade = ?, estado = ?, numero = ?, data_cadastro = ?, cpf = ?, cep = ? WHERE cliente_id = ?"
        cursor.execute(sql, (nome, email, telefone, rua, cidade, estado, numero, data_cadastro, cpf, cep, id))
        conexao.commit()
        conexao.close()
        return redirect('/consulta1')
    else:
        cursor.execute("SELECT * FROM tb_clientes WHERE cliente_id = ?", (id,))
        clientes = cursor.fetchone()
        conexao.close()
        return render_template('editar.html', cliente=clientes)

@app.route('/ver/<int:id>', methods=['GET'])
def ver(id):
    if not app.config['dados_login']:
        return redirect('/')
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'SELECT * FROM tb_clientes WHERE cliente_id = ?'
    cursor.execute(sql, (id,))
    cliente = cursor.fetchone()
    conexao.close()
    return render_template('ver.html', cliente=cliente, usuario=app.config['dados_login'])

@app.route('/ver2/<int:id>', methods=['GET'])
def ver2(id):
    if not app.config['dados_login']:
        return redirect('/')
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'SELECT * FROM tb_fornecedor WHERE fornecedor_id = ?'
    cursor.execute(sql, (id,))
    fornecedores = cursor.fetchone()
    conexao.close()
    return render_template('ver2.html', fornecedores=fornecedores, usuario=app.config['dados_login'])

@app.route('/cadastro2')
def cadastro2():
    if not app.config['dados_login']:
        return redirect('/')
    return render_template("cadastro_fornecedor.html", fornecedor=app.config['dados_login'])

@app.route("/mandar", methods=['POST'])
def mandar():
    nome = request.form['nome']
    site = request.form['site']
    email = request.form['email']
    telefone = request.form['telefone']
    rua = request.form['rua']
    cidade = request.form['cidade']
    estado = request.form['estado']
    numero = request.form['numero']
    data_cadastro = request.form['data_cadastro']
    cnpj = request.form['cnpj']
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'INSERT INTO tb_fornecedor (nome, email, telefone, site, rua, cidade, estado, numero, data_cadastro, cnpj) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(sql, (nome, email, telefone, site, rua, cidade, estado, numero, data_cadastro, cnpj))
    conexao.commit()
    conexao.close()
    return redirect('/consulta2')

@app.route('/consulta2')
def consulta2():
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'SELECT * FROM tb_fornecedor'
    cursor.execute(sql)
    fornecedores = cursor.fetchall()
    conexao.close()
    return render_template('consulta_fornecedor.html', fornecedores=fornecedores)

@app.route('/excluir2/<int:id>', methods=['GET'])
def excluir2(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'DELETE FROM tb_fornecedor WHERE fornecedor_id = ?'
    cursor.execute(sql, (id,))
    conexao.commit()
    conexao.close()
    return redirect('/consulta2')

@app.route('/editar2/<int:id>', methods=['GET', 'POST'])
def editar2(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        site = request.form['site']
        email = request.form['email']
        telefone = request.form['telefone']
        rua = request.form['rua']
        cidade = request.form['cidade']
        estado = request.form['estado']
        numero = request.form['numero']
        data_cadastro = request.form['data_cadastro']
        cnpj = request.form['cnpj']
        sql = "UPDATE tb_fornecedor SET nome = ?, email = ?, telefone = ?, rua = ?, cidade = ?, estado = ?, numero = ?, data_cadastro = ?, cnpj = ?, site = ? WHERE fornecedor_id = ?"
        cursor.execute(sql, (nome, email, telefone, rua, cidade, estado, numero, data_cadastro, cnpj, site, id))
        conexao.commit()
        conexao.close()
        return redirect('/consulta2')
    else:
        cursor.execute("SELECT * FROM tb_fornecedor WHERE fornecedor_id = ?", (id,))
        fornecedores = cursor.fetchone()
        conexao.close()
        return render_template('editarfornecedor.html', fornecedor=fornecedores)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('login2.html')
    elif request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        imagem = request.files['imagem']
        nome_imagem = None
        if imagem:
            extensao = imagem.filename.split('.')[-1]
            nome_imagem = f"{usuario.strip().lower().replace(' ', '_')}.{extensao}"
            caminho_imagem = os.path.join(app.config['UPLOAD'], nome_imagem)
            imagem.save(caminho_imagem)
        with sqlite3.connect('models/cadastro.db') as conexao:
            cursor = conexao.cursor()
            sql = 'INSERT INTO tb_login (nome_usuario, usuario, senha, imagem) VALUES (?, ?, ?, ?)'
            cursor.execute(sql, (nome_usuario, usuario, senha, nome_imagem))
            conexao.commit()
        return redirect('/')

@app.route('/cadastro3')
def cadastro3():
    if not app.config['dados_login']:
        return redirect('/')
    return render_template("cadastro_usuario.html", usuario=app.config['dados_login'])

@app.route('/lancar', methods=['POST'])
def lancar():
    nome_usuario = request.form['nome_usuario']
    usuario = request.form['usuario']
    senha = request.form['senha']
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    imagem = request.files['imagem']
    nome_imagem = None
    if imagem:
        extensao = imagem.filename.split('.')[-1]
        nome_imagem = f"{usuario.strip().lower().replace(' ', '_')}.{extensao}"
        caminho_imagem = os.path.join(app.config['UPLOAD'], nome_imagem)
        imagem.save(caminho_imagem)
    with sqlite3.connect('models/cadastro.db') as conexao:
        cursor = conexao.cursor()
        sql = 'INSERT INTO tb_login (nome_usuario, usuario, senha, imagem) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (nome_usuario, usuario, senha, nome_imagem))
        conexao.commit()
    conexao.close()
    return redirect('/cadastro3')

@app.route('/consulta3')
def consulta3():
    if not app.config['dados_login']:
        return redirect('/')
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'SELECT * FROM tb_login'
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    conexao.close()
    return render_template('consulta_usuarios.html', usuarios=usuarios, dados_login=app.config['dados_login'])

@app.route('/excluir3/<int:id>', methods=['GET'])
def excluir3(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    sql = 'DELETE FROM tb_login WHERE usuario_id = ?'
    cursor.execute(sql, (id,))
    conexao.commit()
    conexao.close()
    return redirect('/consulta3')

@app.route('/editar3/<int:id>', methods=['GET', 'POST'])
def editar3(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        usuario = request.form['usuario']
        senha = request.form['senha']
        imagem = request.files['imagem']
        nome_imagem = None
        if imagem:
            extensao = imagem.filename.split('.')[-1]
            nome_imagem = f"{usuario.strip().lower().replace(' ', '_')}.{extensao}"
            caminho_imagem = os.path.join(app.config['UPLOAD'], nome_imagem)
            imagem.save(caminho_imagem)
        sql = "UPDATE tb_login SET nome_usuario = ?, usuario = ?, senha = ?, imagem = ? WHERE usuario_id = ?"
        cursor.execute(sql, (nome_usuario, usuario, senha, nome_imagem, id))
        conexao.commit()
        conexao.close()
        return redirect('/consulta3')
    else:
        cursor.execute("SELECT * FROM tb_login WHERE usuario_id = ?", (id,))
        usuario = cursor.fetchone()
        conexao.close()
        return render_template('editarusuario.html', usuario=usuario)
    
@app.route('/ver3/<int:id>', methods=['GET'])
def ver3(id):
    if not app.config['dados_login']:
        return redirect('/')

    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_login WHERE usuario_id = ?'
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()  # Alterado para 'usuario'

    conexao.close()

    # Verifique se o usuário foi encontrado
    if usuario is None:
        return "Usuário não encontrado.", 404

    return render_template('ver3.html', usuario=usuario, usuario_logado=app.config['dados_login'])


app.run(host= '127.0.0.1', port=80, debug=True)