import os
import io
import PyPDF2
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Inicializa client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def classify_email(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Classifique como 'Produtivo' ou 'Improdutivo'."},
                {"role": "user", "content": f"Classifique: {text[:2000]}"}
            ],
            max_tokens=10,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro OpenAI: {e}")
        return "Erro na Classificação"

def generate_response(classification, email_content):
    try:
        if classification == "Produtivo":
            prompt_content = f"O e-mail a seguir é uma solicitação. Crie uma resposta automática educada confirmando o recebimento e que a equipe responsável irá analisar. E-mail: '{email_content}'"
        else:
            prompt_content = f"O e-mail a seguir é uma mensagem que não requer ação. Crie uma resposta automática educada agradecendo a mensagem e informando que ela foi recebida. E-mail: '{email_content}'"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_content}],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro OpenAI: {e}")
        return "Erro na Geração de Resposta"

# Rotas do Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_content = ""

    if 'email_content' in request.form:
        email_content = request.form['email_content']
    elif 'email_file' in request.files:
        file = request.files['email_file']
        if file.filename.endswith('.txt'):
            email_content = read_txt(file)
        elif file.filename.endswith('.pdf'):
            email_content = read_pdf(file)
        else:
            return jsonify({'error': 'Formato de arquivo não suportado.'}), 400
    else:
        return jsonify({'error': 'Nenhum conteúdo de e-mail ou arquivo fornecido.'}), 400

    processed_text = preprocess_text(email_content)

    classification = classify_email(processed_text)
    suggested_response = generate_response(classification, processed_text)

    return jsonify({
        'classification': classification,
        'suggested_response': suggested_response
    })

@app.route('/health')
def health_check():
    try:
        # Teste simples da API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Diga 'OK'"}],
            max_tokens=5,
            temperature=0.0
        )
        return jsonify({"status": "healthy", "openai": "working"})
    except Exception as e:
        return jsonify({"status": "error", "openai": str(e)}), 500

