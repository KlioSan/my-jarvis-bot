import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Εδώ συνδέουμε το API Key που πήρες από το Google AI Studio
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Επιλέγουμε το δωρεάν και γρήγορο μοντέλο της Google
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/jarvis', methods=['POST'])
def jarvis_brain():
    data = request.json
    user_voice_text = data.get("text", "") # Εδώ έρχεται το κείμενο από τη φωνή σου
    
    if not user_voice_text:
        return jsonify({"reply": "Hello jarvis is working", "command": "STOP"})

    print(f"Χρήστης: {user_voice_text}")

    # Δίνουμε οδηγίες στο AI πώς να συμπεριφέρεται ως Jarvis
    prompt = f"""
    Είσαι ο Jarvis, ο έξυπνος βοηθός AI ενός ρομπότ. Απάντησε σύντομα και φιλικά στα ελληνικά.
    Αν ο χρήστης σου ζητήσει να κινηθεί (π.χ. προχώρα, πήγαινε μπροστά, στρίψε, σταμάτα), 
    εκτός από την απάντησή σου, πρέπει να αναγνωρίσεις την κίνηση.
    
    Ερώτηση χρήστη: {user_voice_text}
    """

    # Το Gemini απαντάει και ψάχνει στο Google αν χρειαστεί πληροφορία!
    response = model.generate_content(prompt)
    ai_reply = response.text

    # Φιλτράρισμα εντολών για τα μοτέρ του ESP32
    command = "STOP"
    text_lower = user_voice_text.lower()
    if "μπροστά" in text_lower or "προχώρα" in text_lower:
        command = "FORWARD"
    elif "πίσω" in text_lower:
        command = "BACKWARD"
    elif "αριστερά" in text_lower:
        command = "LEFT"
    elif "δεξιά" in text_lower:
        command = "RIGHT"
    elif "σταμάτα" in text_lower or "stop" in text_lower:
        command = "STOP"
    elif "τηλέφωνο" in text_lower or "κάλεσε" in text_lower:
        command = "CALL"
    elif "spotify" in text_lower or "μουσική" in text_lower:
        command = "SPOTIFY"

    # Επιστρέφουμε την απάντηση και την εντολή κίνησης πίσω στο ρομποτάκι
    return jsonify({
        "reply": ai_reply,
        "command": command
    })

if __name__ == '__main__':
    # Ο server τρέχει online
    app.run(host='0.0.0.0', port=port)
