import joblib

model = joblib.load("Model.pkl")

print(model)

print("\n============================")
print("Selected Features")
print("============================")

selector = model.named_steps["feature_selection"]

print(selector.get_support())

print(selector.get_feature_names_out())

print("\n============================")
print("Model")
print("============================")

print(model.named_steps["model"])