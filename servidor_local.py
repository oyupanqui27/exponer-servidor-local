from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def recibir_datos():
    datos = request.json
    print("Datos recibidos:", datos)
    # Aquí puedes guardar los datos o procesarlos

    return jsonify({"status": datos), 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)



