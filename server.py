from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autoriser React à accéder au backend

DB_FILE = "config.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

# ✅ Récupérer tous les composants
@app.route("/composants", methods=["GET"])
def get_composants():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM composants")
    composants = [{"id": row[0], "nom": row[1], "categorie": row[2], "socket": row[3], "prix": row[4], "image_url": row[5]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(composants)

# ✅ Ajouter un composant avec image
@app.route("/composants", methods=["POST"])
def add_composant():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO composants (nom, categorie, socket, prix, image_url) VALUES (?, ?, ?, ?, ?)",
                   (data["nom"], data["categorie"], data["socket"], data["prix"], data["image_url"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Composant ajouté"}), 201

# ✅ Supprimer un composant
@app.route("/composants/<int:id>", methods=["DELETE"])
def delete_composant(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM composants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Composant supprimé"}), 200

# ✅ Modifier un composant (y compris l’image)
@app.route("/composants/<int:id>", methods=["PUT"])
def update_composant(id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE composants 
        SET nom = ?, categorie = ?, socket = ?, prix = ?, image_url = ? 
        WHERE id = ?
    """, (data["nom"], data["categorie"], data["socket"], data["prix"], data["image_url"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Composant mis à jour"}), 200

# ✅ Récupérer les composants compatibles (ex: Carte Mère compatible avec un CPU)
@app.route("/composants/compatibles", methods=["GET"])
def get_compatibles():
    socket = request.args.get("socket")
    categorie = request.args.get("categorie")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM composants WHERE socket = ? AND categorie = ?", (socket, categorie))
    composants = [{"id": row[0], "nom": row[1], "categorie": row[2], "socket": row[3], "prix": row[4], "image_url": row[5]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(composants)

if __name__ == "__main__":
    app.run(debug=True)
