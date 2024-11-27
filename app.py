from flask import Flask, render_template, request, jsonify 

from main_agent import stream_graph_updates
from tools.resume_extractor import extract_resume_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/query", methods=['POST', 'GET']) 
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
        import pdb
        pdb.set_trace()
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        response = extract_resume_data(file)

        return jsonify({'response': response})
    return render_template('index.html')


if __name__ == "__main__": 
    app.run(debug=True) 