import joblib

print("Starting test...")   # ✅ debug

model = joblib.load("model/model_pipeline.joblib")

print("Model loaded")       # ✅ debug
print(type(model))
print(model)

print("Prediction 1:", model.predict(["Free internship apply now"]))
print("Prediction 2:", model.predict(["I have submitted my assignment"]))