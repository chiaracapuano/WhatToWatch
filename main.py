from Suggestions import Suggestions
import pandas as pd
df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")
df_title = pd.read_csv(r'./Movie_Titles_Ratings.csv', encoding="utf-8")
suggestions = Suggestions(df, df_title, "cats")
print(suggestions.display_results())
from flask import Flask, request
app = Flask(__name__)

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

