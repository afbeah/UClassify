import os
import io
import PyPDF2
from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

text_generator = pipeline("text-generation", model="gpt2")

# Funções de processamento
def read_txt(file):
    return file.read().decode('utf-8')

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def preprocess_text(text):
    return " ".join(text.split())

def classify_email(text):
    result = classifier(text)[0]

    label = result['label']

    if "positive" in label.lower() or "5 stars" in label:
        return "Produtivo"
    else:
        return "Improdutivo"

def generate_response(classification, email_content):

    if classification == "Produtivo":
        prompt = f"O e-mail a seguir é uma solicitação. Crie uma resposta automática educada confirmando o recebimento e que a equipe responsável irá analisar. E-mail: '{email_content}'"

        response = text_generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        return response.split("E-mail:")[0].strip()

    elif classification == "Improdutivo":
        prompt = f"O e-mail a seguir é uma mensagem que não requer ação. Crie uma resposta automática educada agradecendo a mensagem e informando que ela foi recebida. E-mail: '{email_content}'"

        response = text_generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        return response.split("E-mail:")[0].strip()

    return "Não foi possível gerar uma resposta."

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

if __name__ == '__main__':
    # Para rodar localmente (modo debug)
    # app.run(debug=True)
    
    # Para deploy, use a porta padrão da plataforma
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)