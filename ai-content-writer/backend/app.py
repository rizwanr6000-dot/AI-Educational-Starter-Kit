"""
AI Content Writer - Flask Backend
----------------------------------
Serves the frontend and exposes a /generate API endpoint.
The endpoint receives a content_type (article, blog, linkedin, email, report)
plus a topic/brief from the user, routes it to the matching generator
module, and returns AI-generated text formatted for that content type.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

from generators import article, blog, linkedin, email as email_gen, report

load_dotenv()

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# Maps the dropdown value coming from the frontend to a generator module
GENERATORS = {
    "article": article.generate,
    "blog": blog.generate,
    "linkedin": linkedin.generate,
    "email": email_gen.generate,
    "report": report.generate,
}


@app.route("/")
def home():
    """Serve the single-page frontend."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Expected JSON body:
    {
        "content_type": "article" | "blog" | "linkedin" | "email" | "report",
        "topic": "short description of what to write about",
        "tone": "professional" | "casual" | "persuasive" | ... (optional),
        "extra_instructions": "any extra notes" (optional)
    }
    """
    data = request.get_json(force=True) or {}

    content_type = (data.get("content_type") or "").strip().lower()
    topic = (data.get("topic") or "").strip()
    tone = (data.get("tone") or "professional").strip()
    extra_instructions = (data.get("extra_instructions") or "").strip()

    if not topic:
        return jsonify({"error": "Please provide a topic or brief."}), 400

    generator_fn = GENERATORS.get(content_type)
    if not generator_fn:
        return jsonify({
            "error": f"Unknown content_type '{content_type}'. "
                     f"Valid options: {', '.join(GENERATORS.keys())}"
        }), 400

    try:
        result_text = generator_fn(topic=topic, tone=tone, extra_instructions=extra_instructions)
        return jsonify({"content_type": content_type, "output": result_text})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
