from Suggestions import Suggestions
import pandas as pd
df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")
df_title = pd.read_csv(r'./Movie_Titles.csv', encoding="utf-8")
suggestions = Suggestions(df, df_title, "cats")
print(suggestions.display_results())
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
    suggestions = Suggestions(df, df_title, "cats")

    return suggestions.display_results()


if __name__ == "__main__":
    app.run(debug=True)

