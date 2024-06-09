from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/tree')
def get_tree_data():
    tree_data = [
        {
            "name": "Professor A",
            "attributes": {
                "link": "https://scholar.google.com"
            },
            "children": [
                {
                    "name": "Student A1",
                    "attributes": {
        
                        "link": "https://linkedin.com/in/studenta1"
                    }
                },
                {
                    "name": "Student A2",
                    "attributes": {
                        "link": "https://linkedin.com/in/studenta2"
                    }
                },
            ],
        }
    ]
    return jsonify(tree_data)

if __name__ == "__main__":
    app.run(debug=True)