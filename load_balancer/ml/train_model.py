import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

print("[1/4] Generating synthetic training data (5000 samples)...  ✓")

# Generate synthetic training data
data = []

for _ in range(5000):
    cpu1 = np.random.randint(10, 90)
    cpu2 = np.random.randint(10, 90)
    cpu3 = np.random.randint(10, 90)

    conn1 = np.random.randint(0, 50)
    conn2 = np.random.randint(0, 50)
    conn3 = np.random.randint(0, 50)

    # Weighted score: CPU contributes 60%, connections contribute 40%
    loads = [
        0.6 * cpu1 + 0.4 * conn1,
        0.6 * cpu2 + 0.4 * conn2,
        0.6 * cpu3 + 0.4 * conn3
    ]

    best_server = np.argmin(loads)

    data.append([
        cpu1, conn1,
        cpu2, conn2,
        cpu3, conn3,
        best_server
    ])

data = np.array(data)

X = data[:, :-1]
y = data[:, -1]

print("[2/4] Splitting into train/test sets (80/20)...             ✓")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("[3/4] Training Random Forest classifier...                  ✓")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("[4/4] Evaluating model performance...")
accuracy = model.score(X_test, y_test)
print(f"      Test Accuracy: {accuracy:.2f} ({accuracy * 100:.0f}%)")

# Save model to the same directory as this script
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
joblib.dump(model, model_path)

print(f"\nModel trained and saved to {model_path}")