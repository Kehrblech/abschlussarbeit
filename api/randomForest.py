import json
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

#Brauchen verbindung zur db!!! Schließen nicht vergessen 
database_path = 'collected_data.db'
conn = sqlite3.connect(database_path)

#guten panda dataframe wieder nehmen
df = pd.read_sql_query("SELECT * FROM collected_data", conn)

#schließen der db 
conn.close()

#Verweildauer berechnen
def calculate_stay_duration(row):
    times = json.loads(row['times'])
    if times:
        # Verweildauer erster Eintrag
        duration = times[0]['leave'] - times[0]['entry']
        return duration / 1000.0  #ms in sec
    return 0

# extrahieren  meistbesuchten Section
def get_most_visited_section(section_data):
    try:
        sections = json.loads(section_data)
        return max(sections, key=sections.get)
    except:
        return None
# neue spalte coloumn in data frame einefügen 
df['stay_duration'] = df.apply(calculate_stay_duration, axis=1)
df['most_visited_section'] = df['section_visibility'].apply(get_most_visited_section)

#  feature bestimmung
features = ['scroll_percentage', 'stay_duration', 'most_visited_section', 'user_agent']
X = df[features] #feature matrix mit features beschreiben
y = df['next_action']#und target variable bestimmen !!! Also das was wir Predicten wollen

# One-Hot-Encoding für kategoriale Daten  cat=ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['most_visited_section', 'user_agent'])
    ], remainder='passthrough')

X_processed = preprocessor.fit_transform(X)

# Daten in Trainings- und Test auf aufteilen  
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

#RandomForest Modelltraining random_state variable steuert randomness daher 42
model = RandomForestClassifier(random_state=42)# 42 ist der Sinn des Lebens also muss er auch bei Randomness helfen :D 
model.fit(X_train, y_train)
# Feature Importance Analyse
feature_importances = model.feature_importances_

# Feature Namen nach der Transformation
feature_names = preprocessor.get_feature_names_out()

# Erstelle und zeige eine DataFrame mit den Feature Importances
importances_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
# Vorhersagen und Bewertung
y_pred = model.predict(X_test)
# Zeigt ersten paar zeilen Pandas DataFrames
print(df.head())
#Klassifizierungsbericht
print(classification_report(y_test, y_pred))
# Feature-Importance Analyse
print(importances_df.sort_values(by='Importance', ascending=False))

