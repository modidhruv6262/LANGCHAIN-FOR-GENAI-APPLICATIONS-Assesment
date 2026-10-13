from pathlib import Path
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

np.random.seed(42)
n_samples = 150

distance_km = np.random.uniform(1.0, 15.0, n_samples)
num_items = np.random.randint(1, 10, n_samples)
rain_flag = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])

delivery_time_min = (
    10.0 +
    2.5 * distance_km +
    1.8 * num_items +
    8.0 * rain_flag +
    np.random.normal(0, 2.0, n_samples)
)

X = np.column_stack([distance_km, num_items, rain_flag])
y = delivery_time_min

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
print(f"Model Training Complete. Test Set RMSE: {rmse:.4f} minutes")

model_filename = "delivery_model.joblib"
joblib.dump(model, model_filename)

file_size_kb = Path(model_filename).stat().st_size / 1024.0
print(f"Model saved to '{model_filename}' successfully. File size: {file_size_kb:.2f} KB")

reloaded_model = joblib.load(model_filename)

test_sample = np.array([[5.5, 3, 1]])
orig_pred = model.predict(test_sample)[0]
reloaded_pred = reloaded_model.predict(test_sample)[0]

print(f"Original Model Prediction: {orig_pred:.2f} min")
print(f"Reloaded Model Prediction: {reloaded_pred:.2f} min")

if np.isclose(orig_pred, reloaded_pred):
    print("Verification Result: PASS")
else:
    print("Verification Result: FAIL")
