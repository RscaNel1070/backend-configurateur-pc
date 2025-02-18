import sqlite3

conn = sqlite3.connect("config.db")
cursor = conn.cursor()

# Vérifier si la colonne image_url existe déjà
cursor.execute("PRAGMA table_info(composants)")
columns = [column[1] for column in cursor.fetchall()]

if "image_url" not in columns:
    cursor.execute("ALTER TABLE composants ADD COLUMN image_url TEXT")
    print("✅ Colonne 'image_url' ajoutée avec succès !")
else:
    print("ℹ️ La colonne 'image_url' existe déjà.")

conn.commit()
conn.close()
print("✅ Base de données mise à jour avec succès !")
