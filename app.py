from flask import Flask, render_template, request, jsonify 

from main_agent import stream_graph_updates

app = Flask(__name__)

@app.route("/query", methods=['POST', 'GET']) 
def query_view(): 
    if request.method == 'POST': 
        print('Query processing') 
        prompt = request.form['prompt'] 
        response = stream_graph_updates(prompt) 
        print(response) 

        return jsonify({'response': response}) 
    return render_template('index.html') 


if __name__ == "__main__": 
    app.run(debug=True) 