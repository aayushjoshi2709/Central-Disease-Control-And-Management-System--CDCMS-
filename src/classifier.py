from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression())
    ])
def fit_data(disease_symptoms):
    X_train = []
    y_train = []
    for disease, symptoms in disease_symptoms.items():
        for symptom in symptoms:
            X_train.append(symptom)
            y_train.append(disease)    
    pipeline.fit(X_train, y_train)
def build_model():
    joblib.dump(pipeline, 'pipeline.pkl')

