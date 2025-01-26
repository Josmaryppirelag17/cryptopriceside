from flask import Flask, render_template, request
import requests

app = Flask(__name__)

COINCAP_BASE_URL = "https://api.coincap.io/v2/assets/"

@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_crypto():
    """Buscar criptomoneda y mostrar resultados"""
    crypto_name = request.form.get('crypto_name').lower()

    if not crypto_name:
        return render_template('error.html', message="Por favor, ingresa el nombre de una criptomoneda.")

    # Solicitud a CoinCap API
    url = f"{COINCAP_BASE_URL}{crypto_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("data", {})
        if data:
            name = data.get("name", "Nombre no disponible")
            price = float(data.get("priceUsd", 0.0))
            price_usd = f"${price:,.2f}"  # Formato de precio con comas
            return render_template('result.html', name=name, price=price_usd)
        else:
            return render_template('error.html', message="No se encontraron resultados para esa criptomoneda.")
    else:
        return render_template('error.html', message="Hubo un error al conectarse con CoinCap. Intenta más tarde.")

if __name__ == '__main__':
    app.run(debug=True)
