import os
from flask import Flask, request, jsonify

app = Flask(_name_)

# Dossier où les fichiers envoyés seront enregistrés
DOSSIER_UPLOAD = "uploads"
os.makedirs(DOSSIER_UPLOAD, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier n'a été envoyé"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"message": "Aucun fichier sélectionné"}), 400
    
    # Enregistrer le fichier sur le serveur
    file_path = os.path.join(DOSSIER_UPLOAD, file.filename)
    file.save(file_path)

    # Confirmation de l'enregistrement
    return jsonify({"message": "Fichier reçu et enregistré avec succès", "file_path": file_path}), 200

if _name_ == "_main_":
    app.run(debug=True, port=5000)