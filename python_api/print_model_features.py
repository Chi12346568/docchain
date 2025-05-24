import joblib

clf_diagnostic = joblib.load("modele_diagnostic.pkl")
clf_disease = joblib.load("modele_maladie.pkl")

# Print the classes the model can predict
print("Classes for modele_maladie.pkl:", clf_disease.classes_)

# print feature names as they are like in fit time
print(clf_disease.feature_names_in_)