from Suggestions import Suggestions
import pandas as pd
df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")
df_title = pd.read_csv(r'./Movie_Titles.csv', encoding="utf-8")
from flask import Flask, request
app = Flask(__name__)

"""
model=None
def load_model():

    global model
    model = spacy.load("en_core_web_lg")
    return model

if __name__ == "__main__":
    print(("* Loading NLP model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run(debug=True)


@app.route("/predict", methods=["POST"])
def predict():

    if request.method == "POST":
        suggestions = Suggestions(df, df_title, model, "cats")
        return suggestions.display_results()
        #    output=model.predict(data)  #what you want to do with frozen model goes here"""

@app.route("/")
def home():
    return """
    <html><head></head>
    <body>
        <h1>Fuck you and the horse</h1>
        <h3>you rode in on</h3>
        <div>
            <form action="/api/suggest" method="get">
                <label for="q">Query:</label><br>
                <input type="text" id="q" name="q" value=""><br>
            </form>
        </div>
        </body>
    </html>
           """

@app.route("/api/suggest")
def Suggest():
    q = request.args.get('q')
    #suggestions = Suggestions(df, df_title, "cats")
    return q#suggestions.display_results()
    #    output=model.predict(data)  #what you want to do with frozen model goes here"""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

