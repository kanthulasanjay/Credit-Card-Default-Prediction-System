import joblib

model = joblib.load("best_model.pkl")

print("Pipeline Steps:")
print(model.named_steps.keys())

preprocessor = model.named_steps["preprocessor"]

print("\nExpected Features:")
print(preprocessor.feature_names_in_)