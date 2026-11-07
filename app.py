from flask import Flask, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase Initialize කිරීම
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/get-posts", methods=["GET"])
def get_posts():
  try:
    posts_ref = db.collection("posts")
    docs = posts_ref.stream()

    posts_list = []
    for doc in docs:
      post_data = doc.to_dict()

      created_at = post_data.get("createdAt", "")
      if hasattr(created_at, "strftime"):
        created_at_str = created_at.strftime("%B %d, %Y")
      else:
        created_at_str = str(created_at)

      posts_list.append({
          "title": str(post_data.get("title", "")),
          "content": str(post_data.get("desc", "")),
          "url": str(post_data.get("link", "")),
          "author": str(post_data.get("author", "")),
          "category": str(post_data.get("category", "")),
          "badge": str(post_data.get("badge", "")),
          "date": created_at_str,
      })
    return jsonify({"success": True, "posts": posts_list})
  except Exception as e:
    print("Error:", e)
    return jsonify({"success": False, "posts": []})


if __name__ == "__main__":
  app.run(debug=True, port=5000)