from flask import Flask, jsonify, abort, make_response, request
from controller import Controller

app = Flask(__name__)

@app.route('/create_structure', methods=['GET'])
def create_structure():
    ctrl = Controller()
    ctrl.create_db_structure_with_data()
    return jsonify({"result": 'ok'})

# Save all the algo models to disk
# http://127.0.0.1:5000/save_models/popular,bias,topn,itemitem,useruser,biasedmf,implicitmf,funksvd
@app.route('/save_models/<algos>', methods=['GET'])
def save_models(algos):
    ctrl = Controller()
    ctrl.save_models(algos)
    return jsonify({"result": 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')