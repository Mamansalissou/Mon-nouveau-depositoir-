import os
import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# URL du serveur pour l'envoi du fichier
URL_SERVEUR = "http://192.168.95.114:5000/upload"

# Dictionnaire des plats et des quartiers
plats = {
    'Royal Cheese': 2000,
    'Mc Deluxe': 1500,
    'Mc Bacon': 1000,
    'Big Mac': 3000,
    'Massa de biri': 100
}

quartiers = {
    'Bani Fandou': 2,
    'Koira Tagui': 3,
    'Cité Député': 2,
    'Lazaret': 2,
    'Niamey 2000': 3,
    'Haro Banda': 3
}

# Dossier temporaire pour enregistrer les commandes
DOSSIER_TEMP = "commandes_client"
os.makedirs(DOSSIER_TEMP, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def accueil():
    if request.method == "POST":
        # Récupérer les données du formulaire
        choix_plat = request.form["choix_plat"]
        nombre_plats = int(request.form["nombre_plats"])
        numero_telephone = request.form["numero_telephone"]
        livraison = request.form["livraison"]
        quartier = request.form.get("quartier", "")
        frais_livraison = 0
        distance_km = 0

        # Calcul pour la livraison
        if livraison == "OUI" and quartier:
            distance_km = quartiers.get(quartier, 0)
            frais_livraison = (distance_km // 2) * 500

        total_plat = plats[choix_plat] * nombre_plats + frais_livraison

        # Préparer les données
        commande = {
            "plat": choix_plat,
            "nombre_plats": nombre_plats,
            "total_plat": total_plat,
            "livraison": livraison,
            "quartier": quartier,
            "distance_km": distance_km,
            "frais_livraison": frais_livraison,
            "numero_telephone": numero_telephone,
        }

        # Sauvegarder la commande dans un fichier HTML
        fichier_html = os.path.join(DOSSIER_TEMP, "commande.html")
        with open(fichier_html, mode="w", encoding="utf-8") as file:
            file.write(f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Commande Client</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f9f9f9;
                        color: #333;
                    }}
                    h1 {{
                        text-align: center;
                        color: #444;
                    }}
                    table {{
                        width: 80%;
                        margin: 20px auto;
                        border-collapse: collapse;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    }}
                    th, td {{
                        padding: 12px 15px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f44336;
                        color: white;
                        text-transform: uppercase;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <h1>Résumé de la Commande</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Plat</th>
                            <th>Nombre de plats</th>
                            <th>Total Plat</th>
                            <th>Livraison</th>
                            <th>Quartier</th>
                            <th>Distance (km)</th>
                            <th>Frais Livraison</th>
                            <th>Numéro de Téléphone</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{commande['plat']}</td>
                            <td>{commande['nombre_plats']}</td>
                            <td>{commande['total_plat']} FCFA</td>
                            <td>{commande['livraison']}</td>
                            <td>{commande.get('quartier', 'N/A')}</td>
                            <td>{commande.get('distance_km', '0')}</td>
                            <td>{commande.get('frais_livraison', '0')} FCFA</td>
                            <td>{commande['numero_telephone']}</td>
                        </tr>
                    </tbody>
                </table>
            </body>
            </html>
            """)

        # Envoyer le fichier au serveur
        try:
            with open(fichier_html, "rb") as f:
                response = requests.post(URL_SERVEUR, files={"file": f})
            if response.status_code == 200:
                print("Commande envoyée avec succès :", response.json())
                os.remove(fichier_html)  # Supprimer le fichier localement
            else:
                print("Erreur lors de l'envoi :", response.text)
        except Exception as e:
            print("Erreur de connexion au serveur :", str(e))

        # Afficher le résumé de la commande
        return render_template(
            "resume.html",
            plat=choix_plat,
            nombre_plats=nombre_plats,
            total_plat=total_plat,
            numero_telephone=numero_telephone,
            frais_livraison=frais_livraison,
            distance_km=distance_km,
            quartier=quartier,
        )

    return render_template("index.html", plats=plats, quartiers=quartiers)


if __name__ == "__main__":
    app.run(debug=True, port=5001)