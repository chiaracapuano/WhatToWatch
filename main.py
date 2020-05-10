import Suggestions
import pandas as pd
df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")
df_title = pd.read_csv(r'./Movie_Titles.csv', encoding="utf-8")
suggestions = Suggestions(df, df_title, "cats")
print(suggestions)

"""from flask import Flask
import Sugestions
app = Flask(__name__)


@app.route("/")
def home():

    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)"""

