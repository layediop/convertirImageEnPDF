from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from PIL import Image
import os

app = Flask(__name__)

# Page d'accueil de l'application
@app.route('/')
def index():
    return render_template('index.html')

# Fonction pour convertir l'image PNG en PDF
def convert_to_pdf(image_path, output_path):
    image = Image.open(image_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, 0, 0, pdf.w, pdf.h)
    pdf.output(output_path, "F")

# Route pour gérer le téléchargement de l'image
@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Aucun fichier n'a été téléchargé."

        file = request.files['file']
        if file.filename == '':
            return "Aucun fichier sélectionné."

        if file:
            # Sauvegarde de l'image téléchargée
            image_path = 'static/input.png'  # Chemin où l'image sera sauvegardée
            file.save(image_path)

            # Convertir l'image en PDF
            pdf_output_path = 'static/output.pdf'  # Chemin où le PDF sera sauvegardé
            convert_to_pdf(image_path, pdf_output_path)

            # Supprimer l'image PNG après la conversion
            os.remove(image_path)

            # Télécharger le fichier PDF
            return send_file(pdf_output_path, as_attachment=True)

    return "Erreur lors de la conversion."

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
