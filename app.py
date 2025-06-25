from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import stripe

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

stripe.api_key = 'sk_live_YOUR_SECRET_KEY_HERE'  # <-- Replace with your Stripe secret key

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.json
        email = data.get('email')
        amount = data.get('amount', 500)  # default to 500 cents ($5)

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
            receipt_email=email,
        )

        return jsonify({'clientSecret': intent.client_secret})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server running on http://localhost:5000")
    app.run(port=5000, debug=True)
