from flask import Flask, render_template, request, jsonify 

from main_agent import stream_graph_updates
from tools.resume_extractor import extract_resume_data
from flask_cors import CORS, cross_origin
app = Flask(__name__, static_url_path='',
                  static_folder='ui/build',
                  template_folder='ui/build')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/query", methods=['POST', 'GET']) 
@cross_origin()
def query_view(): 
    if request.method == 'POST': 
        print('Query processing') 
        prompt = request.form['prompt'] 
        response = stream_graph_updates(prompt) 
        print(response) 

        return jsonify({'response': response}) 
    return render_template('index.html') 


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print('Resume extraction in processing')
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        response = extract_resume_data(file)
        dummy_response= {
            "name": "Bhavesh",
            "skills": ["python", "django"],
            "experience": "5 years",
            "certifications": "No"
            }

        return jsonify({'response': response})
    return render_template('index.html')




@app.route("/ui")
def ui():
    return render_template("index.html")

if __name__ == "__main__": 
    app.run(debug=True) 