from flask import Flask, send_from_directory, jsonify

# Create an instance
app = Flask(__name__, static_folder="Frontend/src")

# Flask API endpoint
@app.route('/api/data')
def get_data():
    return jsonify({'data': 'Your data here'})


# {fetch('http://localhost:5000/api/data')
#             .then(response => response.json())
#             .then(data => console.log(data))
#             }


if __name__ == '__main__':
    app.run(debug=True)