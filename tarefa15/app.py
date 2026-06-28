from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import datetime
import os
import re

load_dotenv()

os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

app.debug = True

app.secret_key = os.getenv("SECRET_KEY", "desenvolvimento_chave_segura")

SUAP_BASE_URL = 'https://suap.ifrn.edu.br'

oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    api_base_url=f'{SUAP_BASE_URL}/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'{SUAP_BASE_URL}/o/token/',
    authorize_url=f'{SUAP_BASE_URL}/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)

def obter_dados_navbar():
    token = session.get('suap_token')
    if not token:
        return None

    try:
        resposta = oauth.suap.get('rh/meus-dados')
        if resposta.status_code == 200:
            dados_suap = resposta.json()
            nome_usuario = dados_suap.get('nome') or dados_suap.get('nome_completo') or "Usuário SUAP"
            foto_relativa = dados_suap.get('url_foto')
            
            if foto_relativa:
                foto_completa = f"{SUAP_BASE_URL.rstrip('/')}/{foto_relativa.lstrip('/')}"
                
            else:
                foto_completa = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                
            return {
                'nome': nome_usuario,
                'matricula': dados_suap.get('matricula'),
                'avatar': foto_completa
            }

        return None

    except Exception:

        return None

@app.route('/')
def index():
    user_nav = obter_dados_navbar()
    if user_nav:
        return redirect(url_for('perfil'))

    return render_template('index.html', user_data=None)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.suap.authorize_redirect(redirect_uri)

@app.route('/login/authorized')
def auth():
    try:
        token = oauth.suap.authorize_access_token()
        session['suap_token'] = token
        return redirect(url_for('perfil'))

    except Exception:

        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
    user_nav = obter_dados_navbar()
    if not user_nav:
        return redirect(url_for('index'))
    resposta = oauth.suap.get('rh/meus-dados')
    dados_completos = resposta.json()

    return render_template(
        'perfil.html', 
        user_data=user_nav, 
        dados=dados_completos, 
        suap_url=SUAP_BASE_URL
    )

@app.route('/boletim')
def boletim():
    user_nav = obter_dados_navbar()
    if not user_nav:
        return redirect(url_for('index'))
    
    ano_selecionado = request.args.get("ano", default="2026")
    
    boletim_dados = []
    totais = {"aulas_totais": 0, "aulas_dadas": 0, "faltas": 0, "frequencia_media": "100%"}

    
    try:
        resposta_boletim = oauth.suap.get(f"ensino/meu-boletim/{ano_selecionado}/1/")
        if resposta_boletim.status_code != 200:
            resposta_boletim = oauth.suap.get(f"ensino/meu-boletim/{ano_selecionado}/1")

        if resposta_boletim.status_code == 200:
            dados_retornados = resposta_boletim.json()
            if isinstance(dados_retornados, dict) and "results" in dados_retornados:
                boletim_dados = dados_retornados["results"]

            else:
                boletim_dados = dados_retornados

            if boletim_dados:
                c_h_total = 0
                aulas_dadas_total = 0
                faltas_total = 0
                soma_frequencias = 0
                total_materias = 0

                for m in boletim_dados:
                    ch_texto = str(m.get('carga_horaria', '0'))
                    ch_num = int(re.search(r'\d+', ch_texto).group()) if re.search(r'\d+', ch_texto) else 0
                    aulas_texto = str(m.get('numero_aulas_realizadas', '0'))
                    aulas_num = int(re.search(r'\d+', aulas_texto).group()) if re.search(r'\d+', aulas_texto) else 0
                    faltas_texto = str(m.get('numero_faltas', '0'))
                    faltas_num = int(re.search(r'\d+', faltas_texto).group()) if re.search(r'\d+', faltas_texto) else 0
                    c_h_total += ch_num
                    aulas_dadas_total += aulas_num
                    faltas_total += faltas_num

                    freq_texto = str(m.get('percentual_frequencia', '100')).replace(',', '.')
                    freq_match = re.search(r'[\d\.]+', freq_texto)
                    freq_num = float(freq_match.group()) if freq_match else 100.0

                    soma_frequencias += freq_num
                    total_materias = total_materias + 1

                    
                media_freq = (soma_frequencias / len(boletim_dados)) if boletim_dados else 100.0
                totais = {
                    "aulas_totais": f"{c_h_total} aulas",
                    "aulas_dadas": aulas_dadas_total,
                    "faltas": faltas_total,
                    "frequencia_media": f"{media_freq:.2f}%".replace('.', ',')
                }

    except Exception as e:
        print(f"Erro no processamento do Boletim: {e}")

    return render_template(
        'boletim.html', 
        user_data=user_nav, 
        boletim=boletim_dados, 
        totais=totais,
        ano_selecionado=int(ano_selecionado)
    )

if __name__ == "__main__":

    app.run()