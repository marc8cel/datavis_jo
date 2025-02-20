from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Charger les données
def load_sports_data():
    df = pd.read_csv("static/data/events.csv", sep=";")
    categories = {}

    for _, row in df.iterrows():
        category = row["category"]
        sport = row["sport"]
        event = row["event"]

        if category not in categories:
            categories[category] = {}

        if sport not in categories[category]:
            categories[category][sport] = []

        categories[category][sport].append(event)

    # Trier les sports et les événements par ordre alphabétique
    for category in categories:
        categories[category] = dict(sorted(categories[category].items()))
        for sport in categories[category]:
            categories[category][sport].sort()

    return categories

@app.route("/")
def home():
    categories = load_sports_data()

    first_three_sports = {}
    remaining_sports = {}
    for category, sports in categories.items():
        sorted_sports = sorted(sports.keys())  # Trier les clés (sports) par ordre alphabétique
        first_three_sports[category] = sorted_sports[:3]
        remaining_sports[category] = sorted_sports[3:]

    return render_template("filter_sport.html", first_three_sports=first_three_sports, remaining_sports=remaining_sports)

if __name__ == "__main__":
    app.run(debug=True)