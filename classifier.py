
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

TRAIN_DATA = [
    ("MV BLUE STAR OPEN GABES BULK CARRIER DWT", "TONNAGE"),
    ("OPEN VESSEL AVAILABLE", "TONNAGE"),
    ("LOAD PORT DISCHARGE PORT LAYCAN", "CARGO_VC"),
    ("IRON SLAG IN BULK", "CARGO_VC"),
    ("DELIVERY REDELIVERY DURATION TCT", "CARGO_TC"),
    ("1 TCT WITH GRAINS", "CARGO_TC"),
]

texts = [x[0] for x in TRAIN_DATA]
labels = [x[1] for x in TRAIN_DATA]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

model.fit(texts, labels)

def classify_email(email_text):
    return str(model.predict([email_text])[0])
