from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import os
from sklearn.externals import joblib
import pandas as pd

# Available Models
clfs = {}

# Generate Flask application
app = Flask(__name__)


@app.route('/api/models/<name>/predict', methods=['POST'])
def predict_api(name):
    """Make a prediction with a model and return the result.

    sample_json = {
        "column_names": ['a', 'b', 'c']
        "values": [
            [1, 4, 9],
            [2, 0, 6],
            [1, 4, 8]
        ]
    }
    """
    json_data = request.get_json()
    X = pd.Series(json_data)
    prediction = clfs[name].predict(X.reshape(1, -1))
    return jsonify(result=prediction.tolist())


@app.route('/api/models/<name>', methods=['PUT'])
def model(name):
    """Load a model into memory."""
    tmp_path = '/tmp/{}.plk'.format(name)

    # Write Model to disk
    with open(tmp_path, 'wb') as f:
        f.write(request.data)

    # This approach will keep all the models in memory
    clfs[name] = joblib.load(tmp_path)

    # Remove from disk
    os.remove(tmp_path)

    return jsonify(status='OK')


@app.route('/models', methods=['GET'])
def list_models():
        """List loaded models."""
        return jsonify(list(clfs.keys()))


@app.route('/models/<name>/predict', methods=['GET'])
def predict(name):
        return 'Dynamic Template Here'


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)