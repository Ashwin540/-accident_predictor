# train_model.py

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib

# Step 1: Simulate a dataset (replace this with real data if available)
np.random.seed(42)
data = pd.DataFrame({
    'vehicle_count': np.random.randint(10, 100, 1000),
    'avg_speed': np.random.normal(40, 10, 1000),
    'visibility': np.random.uniform(0.1, 1.0, 1000),
    'weather': np.random.choice([0, 1], 1000),         # 0: Clear, 1: Rainy
    'road_condition': np.random.choice([0, 1], 1000),  # 0: Good, 1: Slippery
    'accident_prone': np.random.choice([0, 1], 1000, p=[0.7, 0.3])  # 0: Safe, 1: Accident-prone
})

# Step 2: Prepare features and target
X = data.drop('accident_prone', axis=1)
y = data['accident_prone']

# Step 3: Train the GBM (XGBoost) model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

# Step 4: Save the trained model
joblib.dump(model, 'gbm_accident_model.pkl')

print("✅ Model trained and saved as 'gbm_accident_model.pkl'")
