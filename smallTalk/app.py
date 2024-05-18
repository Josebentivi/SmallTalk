from flask import Flask, render_template, request, redirect, jsonify, session
from openai import OpenAI as GPT
from datetime import timedelta
import os
from time import sleep

chave = "Coloque sua chaven"
#openai.api_key = chave
os.environ["OPENAI_API_KEY"] = chave

app = Flask(__name__)
porta = 5000
#tempo de permanencia da sessão
app.secret_key = "textoSecreto"
app.permanent_session_lifetime = timedelta(days=5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/historico')
def historico():
    return render_template('historico.html')

@app.route('/treinamento')
def treinamento():
    return render_template('treinamento.html')

@app.route('/personalizado')
def personalizado():
    return render_template('personalizado.html')

@app.route('/detalhes', methods=["POST","GET"])
def detalhes():
    sleep(1)
    audio_file= open('uploaded_audio.mp3', "rb")
    transcript = GPT().audio.transcriptions.create(model="whisper-1",file=audio_file)
    transcricao = transcript.text.encode().decode()
    session["transcrição"] = transcricao
    comparacao = "A clareza da comunicação é um fator determinante na conquista da confiança, que por sua vez, é fundamental na construção da credibilidade. A credibilidade é fator essencial do êxito do orador"
    transcricaoComparada = transcricao.replace(".","").replace(",","").split(" ")
    exercicio = comparacao.replace(".","").replace(",","").split(" ")
    nota = 0
    if len(transcricaoComparada)>len(exercicio):
        for i in range(len(exercicio)):
            if exercicio[i] == transcricaoComparada[i] or exercicio[i] == transcricaoComparada[i+1]:
                nota+=1
            elif len(transcricaoComparada)>len(exercicio)+1:
                if exercicio[i] == transcricaoComparada[i+2]:
                    nota+=1
    else:
        for i in range(len(transcricaoComparada)) or exercicio[i] == transcricaoComparada[i-1]:
            if exercicio[i] == transcricaoComparada[i]:
                nota+=1
            elif len(transcricaoComparada)>len(exercicio)-3:
                if exercicio[i] == transcricaoComparada[i-2]:
                    nota+=1
    nota=nota/len(exercicio)
    return render_template('exercicio_historico.html',transcricao=transcricao,nota=round(nota*100,2),exercicio=comparacao)

@app.route('/exercicio')
def exercicio():
    return render_template('fazer_exercicio.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        # Salve o arquivo, processe ou faça algo com ele
        audio_file.save('uploaded_audio.mp3')
    else:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=porta)