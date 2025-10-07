from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui-pode-ser-qualquer-coisa'

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Pega a URL de conexão do ambiente do Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- CONFIGURAÇÃO DAS ESCALAS E DADOS INICIAIS ---
MAPA_CATEGORIA_POSTO = {
    'CAP': 'CAP', '1º TEN': 'OFICIAL_SUBALTERNO',
    '2º TEN': 'OFICIAL_SUBALTERNO', 'ASP': 'OFICIAL_SUBALTERNO',
}
REGRAS_ESCALAS = {
    'TEAM': {'CAP': 1, 'OFICIAL_SUBALTERNO': 2}, 'TREM': {'CAP': 1, 'OFICIAL_SUBALTERNO': 2},
    'PT': {'OFICIAL_SUBALTERNO': 1}, 'RANCHO': {'OFICIAL_SUBALTERNO': 1}
}
DADOS_INICIAIS_EFETIVO = [
    {'graduacao': 'Cap', 'nome': 'MADSON'}, {'graduacao': 'Cap', 'nome': 'PIFANO DIAS'},
    {'graduacao': 'Cap', 'nome': 'BRUNA'}, {'graduacao': 'Cap', 'nome': 'GADIOLI'},
    {'graduacao': 'Cap', 'nome': 'GLEICE RODRIGUES'}, {'graduacao': 'Cap', 'nome': 'HÁKYLLA'},
    {'graduacao': 'Cap', 'nome': 'GUIMARAES'}, {'graduacao': 'Cap', 'nome': 'CARAMASCHI'},
    {'graduacao': 'Cap', 'nome': 'THARICK'}, {'graduacao': 'Cap', 'nome': 'CARVALHO'},
    {'graduacao': 'Cap', 'nome': 'JOÃO PEDRO'}, {'graduacao': 'Cap', 'nome': 'JACY'},
    {'graduacao': 'Cap', 'nome': 'LIDIANE RIBEIRO'}, {'graduacao': 'Cap', 'nome': 'CAMILA'},
    {'graduacao': 'Cap', 'nome': 'POLISEL'}, {'graduacao': 'Cap', 'nome': 'BOECHAT'},
    {'graduacao': 'Cap', 'nome': 'JOSIAS'}, {'graduacao': 'Cap', 'nome': 'ANDREIA CARDOSO'},
    {'graduacao': 'Cap', 'nome': 'GISELE'}, {'graduacao': 'Cap', 'nome': 'REZEK'},
    {'graduacao': 'Cap', 'nome': 'MANOEL BEZERRA'}, {'graduacao': 'Cap', 'nome': 'LETICIA CASTRO'},
    {'graduacao': '1º Ten', 'nome': 'ROURE'}, {'graduacao': '1º Ten', 'nome': 'DESLANDES'},
    {'graduacao': '1º Ten', 'nome': 'UCHÔA'}, {'graduacao': '1º Ten', 'nome': 'LUCIANA CUSTODIO'},
    {'graduacao': '1º Ten', 'nome': 'IONE'}, {'graduacao': '1º Ten', 'nome': 'CAMILA MARIOTO'},
    {'graduacao': '1º Ten', 'nome': 'AISHA'}, {'graduacao': '1º Ten', 'nome': 'ZATTERA'},
    {'graduacao': '1º Ten', 'nome': 'ANA BESSA'}, {'graduacao': '1º Ten', 'nome': 'CARVALHO'},
    {'graduacao': '1º Ten', 'nome': 'ALBERNAZ'}, {'graduacao': '1º Ten', 'nome': 'ANDRE FELIPE'},
    {'graduacao': '1º Ten', 'nome': 'HASSAN'}, {'graduacao': '1º Ten', 'nome': 'LEONARDO CASTRIA'},
    {'graduacao': '1º Ten', 'nome': 'DE JESUS'}, {'graduacao': '1º Ten', 'nome': 'MATTA'},
    {'graduacao': '1º Ten', 'nome': 'SOTOLANI'}, {'graduacao': '1º Ten', 'nome': 'SÍLVIA MARTONI'},
    {'graduacao': '1º Ten', 'nome': 'LETÍCIA'}, {'graduacao': '1º Ten', 'nome': 'VERONICA'},
    {'graduacao': '1º Ten', 'nome': 'ZACCARO'}, {'graduacao': '1º Ten', 'nome': 'GABRIEL'},
    {'graduacao': '1º Ten', 'nome': 'VELOSO'}, {'graduacao': '1º Ten', 'nome': 'HERBERT'},
    {'graduacao': '1º Ten', 'nome': 'EMILY BRAZ'}, {'graduacao': '1º Ten', 'nome': 'GOMES PIRES'},
    {'graduacao': '1º Ten', 'nome': 'LAGE'}, {'graduacao': '1º Ten', 'nome': 'FERNANDA OLIVEIRA'},
    {'graduacao': '1º Ten', 'nome': 'ARANTES'}, {'graduacao': '1º Ten', 'nome': 'CARVALHO'},
    {'graduacao': '1º Ten', 'nome': 'DO VALE'}, {'graduacao': '1º Ten', 'nome': 'DINIZ'},
    {'graduacao': '1º Ten', 'nome': 'MAUTONE'}, {'graduacao': '1º Ten', 'nome': 'ANACLETO'},
    {'graduacao': '1º Ten', 'nome': 'LIVIA SOUZA'}, {'graduacao': '1º Ten', 'nome': 'TERRA'},
    {'graduacao': '1º Ten', 'nome': 'LEONARDO'}, {'graduacao': '2º Ten', 'nome': 'SOBRAL'},
    {'graduacao': '2º Ten', 'nome': 'MEDEIROS'}, {'graduacao': '2º Ten', 'nome': 'SANCHES'},
    {'graduacao': '2º Ten', 'nome': 'CONSTANTINO'}, {'graduacao': '2º Ten', 'nome': 'PATRINE'},
    {'graduacao': '2º Ten', 'nome': 'SALES'}, {'graduacao': '2º Ten', 'nome': 'ARGUELLES'},
    {'graduacao': '2º Ten', 'nome': 'WELINGTON'}, {'graduacao': '2º Ten', 'nome': 'ANDRÉ'},
    {'graduacao': '2º Ten', 'nome': 'MIRA'}, {'graduacao': '2º Ten', 'nome': 'LUARA'},
    {'graduacao': '2º Ten', 'nome': 'BORGES'}, {'graduacao': '2º Ten', 'nome': 'JÉSSICA'},
    {'graduacao': '2º Ten', 'nome': 'MARIA'}, {'graduacao': '2º Ten', 'nome': 'SANTOS'},
    {'graduacao': '2º Ten', 'nome': 'TIAGO'}, {'graduacao': '2º Ten', 'nome': 'NATÁLIA'},
    {'graduacao': '2º Ten', 'nome': 'VICTORIO'}, {'graduacao': '2º Ten', 'nome': 'RODRIGUES'},
    {'graduacao': '2º Ten', 'nome': 'ABREU'}, {'graduacao': '2º Ten', 'nome': 'XAVIER'},
    {'graduacao': 'ASP', 'nome': 'LUZ'}, {'graduacao': 'ASP', 'nome': 'CARDOSO'},
]

# --- MODELOS DO BANCO DE DADOS ---
comissao_militar = db.Table('comissao_militar',
    db.Column('comissao_id', db.Integer, db.ForeignKey('comissao.id'), primary_key=True),
    db.Column('efetivo_id', db.Integer, db.ForeignKey('efetivo.id'), primary_key=True)
)

class Efetivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graduacao = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(20), default='Ativo')
    ultima_comissao_TEAM = db.Column(db.Date, nullable=True)
    ultima_comissao_TREM = db.Column(db.Date, nullable=True)
    ultima_comissao_PT = db.Column(db.Date, nullable=True)
    ultima_comissao_RANCHO = db.Column(db.Date, nullable=True)
    comissoes = db.relationship('Comissao', secondary=comissao_militar, back_populates='militares')

class Comissao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_nomeacao = db.Column(db.Date, nullable=False)
    escala = db.Column(db.String(50), nullable=False)
    diex = db.Column(db.String(100))
    nup = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Em Andamento')
    militares = db.relationship('Efetivo', secondary=comissao_militar, back_populates='comissoes')

# --- LÓGICA DO SISTEMA ---
def get_militares_ocupados():
    comissoes_em_andamento = Comissao.query.filter_by(status='Em Andamento').all()
    ocupados = set()
    for comissao in comissoes_em_andamento:
        for militar in comissao.militares:
            ocupados.add(militar.nome)
    return ocupados

def calcular_folga(militar, nome_escala):
    data_ultima_comissao = getattr(militar, f'ultima_comissao_{nome_escala.upper()}', None)
    if not data_ultima_comissao: return float('inf')
    return (date.today() - data_ultima_comissao).days

def sugerir_escala(nome_escala, militares_ocupados):
    regras, sugestao, sugeridos = REGRAS_ESCALAS[nome_escala], [], set()
    for categoria, qtd in regras.items():
        graduacoes_na_categoria = [k for k, v in MAPA_CATEGORIA_POSTO.items() if v == categoria]
        candidatos = Efetivo.query.filter(
            Efetivo.status == 'Ativo',
            Efetivo.graduacao.in_(graduacoes_na_categoria),
            ~Efetivo.nome.in_(sugeridos),
            ~Efetivo.nome.in_(militares_ocupados)
        ).all()
        if len(candidatos) < qtd: return None
        candidatos.sort(key=lambda m: calcular_folga(m, nome_escala), reverse=True)
        sugestao.extend(candidatos[:qtd])
        for s in candidatos[:qtd]: sugeridos.add(s.nome)
    return sugestao

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
def index():
    militares_ocupados = get_militares_ocupados()
    sugestoes = {escala: sugerir_escala(escala, militares_ocupados) for escala in REGRAS_ESCALAS}
    return render_template('index.html', sugestoes=sugestoes, escalas=REGRAS_ESCALAS.keys())

@app.route('/nomear/<nome_escala>', methods=['POST'])
def nomear(nome_escala):
    nomes_escalados = request.form.getlist('nomes_escalados')
    diex, nup, data_nomeacao = request.form.get('diex'), request.form.get('nup'), date.today()
    militares_a_escalar = Efetivo.query.filter(Efetivo.nome.in_(nomes_escalados)).all()
    nova_comissao = Comissao(data_nomeacao=data_nomeacao, escala=nome_escala, diex=diex, nup=nup, status='Em Andamento')
    for militar in militares_a_escalar:
        setattr(militar, f'ultima_comissao_{nome_escala.upper()}', data_nomeacao)
        nova_comissao.militares.append(militar)
    db.session.add(nova_comissao)
    db.session.commit()
    flash('Comissão registrada com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/log')
def ver_log():
    comissoes = Comissao.query.order_by(Comissao.data_nomeacao.desc()).all()
    return render_template('log.html', comissoes=comissoes)

@app.route('/log/concluir/<int:comissao_id>', methods=['POST'])
def concluir_log(comissao_id):
    comissao = Comissao.query.get_or_404(comissao_id)
    comissao.status = 'Concluído'
    db.session.commit()
    flash(f"Comissão ID {comissao_id} marcada como 'Concluída'.", 'success')
    return redirect(url_for('ver_log'))

@app.route('/log/editar/<int:comissao_id>', methods=['GET', 'POST'])
def editar_log(comissao_id):
    comissao = Comissao.query.get_or_404(comissao_id)
    if request.method == 'POST':
        comissao.data_nomeacao = datetime.strptime(request.form['data_nomeacao'], '%Y-%m-%d').date()
        comissao.diex = request.form['diex']
        comissao.nup = request.form['nup']
        comissao.status = request.form['status']
        db.session.commit()
        flash(f"Comissão ID {comissao_id} atualizada.", 'success')
        return redirect(url_for('ver_log'))
    return render_template('editar_log.html', comissao=comissao)

@app.route('/efetivo')
def gerenciar_efetivo():
    efetivo = Efetivo.query.order_by(Efetivo.id).all()
    return render_template('efetivo.html', efetivo=efetivo)

@app.route('/efetivo/editar/<int:militar_id>', methods=['GET', 'POST'])
def editar_efetivo(militar_id):
    militar = Efetivo.query.get_or_404(militar_id)
    if request.method == 'POST':
        militar.graduacao = request.form['graduacao']
        militar.nome = request.form['nome']
        militar.status = request.form['status']
        db.session.commit()
        flash('Militar atualizado com sucesso!', 'success')
        return redirect(url_for('gerenciar_efetivo'))
    return render_template('editar_efetivo.html', militar=militar)

@app.route('/efetivo/novo', methods=['GET', 'POST'])
def novo_efetivo():
    if request.method == 'POST':
        novo_militar = Efetivo(graduacao=request.form['graduacao'], nome=request.form['nome'], status='Ativo')
        db.session.add(novo_militar)
        db.session.commit()
        flash('Novo militar adicionado com sucesso!', 'success')
        return redirect(url_for('gerenciar_efetivo'))
    return render_template('editar_efetivo.html', militar=None)

@app.route('/efetivo/excluir/<int:militar_id>', methods=['POST'])
def excluir_efetivo(militar_id):
    militar = Efetivo.query.get_or_404(militar_id)
    if militar.comissoes.filter_by(status='Em Andamento').count() > 0:
        flash('Erro: Não é possível excluir um militar que está em uma comissão em andamento.', 'error')
        return redirect(url_for('gerenciar_efetivo'))
    db.session.delete(militar)
    db.session.commit()
    flash('Militar excluído com sucesso!', 'success')
    return redirect(url_for('gerenciar_efetivo'))

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
with app.app_context():
    db.create_all()
    if Efetivo.query.count() == 0:
        print("Populando o banco de dados com o efetivo inicial...")
        for militar_data in DADOS_INICIAIS_EFETIVO:
            novo_militar = Efetivo(graduacao=militar_data['graduacao'], nome=militar_data['nome'])
            db.session.add(novo_militar)
        db.session.commit()
        print("Banco de dados populado com sucesso.")