import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score , confusion_matrix , classification_report
from model_def import model



#-------------------------------------------
#Load Data Set
#-------------------------------------------
df = pd.read_csv("OSBS_datasets/Cleaned_data/disease_prediction_dataset_V4.csv")
print(df.columns)



#------------------------------------------
#Features and Target Selection
#------------------------------------------
features= [col for col in df.columns 
              if all(x not in col for x in ['datetime' ,'Variance' ,'risk_score', 'risk_cluster_kmeans',
       'risk_label', 'risk_label_numeric', 'risk_score_smooth', 'risk_color' , 'TFPrecipBulk' ,'windDirMean'])]

X = df[features]
y = df["risk_label_numeric"]




#--------------------------------------------
#Train Test Split
#--------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)




#---------------------------------------------
#Model Training And Evaluaition
#---------------------------------------------
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

def train_and_evaluate(models, X_train, y_train, X_test, y_test , save_dir="src/Trained_Models"):
    results = {}
    for name, model in models.items():
        print(f"\n===== {name} =====")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        # Accuracy
        train_acc = accuracy_score(y_train, train_pred)
        test_acc = accuracy_score(y_test, test_pred)
        
        print(f"Training Accuracy : {train_acc:.4f}")
        print(f"Testing Accuracy  : {test_acc:.4f}")
        
        # Save results
        results[name] = {
            "train_accuracy": train_acc,
            "test_accuracy": test_acc
        }
        
        
        # Save model with pickle
        model_path = os.path.join(save_dir, f"{name}.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        print(f"Model saved at {model_path}")
        
        
        # Plot confusion matrices
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        fig.suptitle(f"Confusion Matrices for {name}", fontsize=14)
        
        ConfusionMatrixDisplay.from_predictions(y_train, train_pred, ax=axes[0], cmap="Blues")
        axes[0].set_title("Training Data")
        
        ConfusionMatrixDisplay.from_predictions(y_test, test_pred, ax=axes[1], cmap="Blues")
        axes[1].set_title("Testing Data")
        
        plt.tight_layout()
        plt.show()
    
    return results


#-------------------------
#Fucntion Call
#-------------------------
results = train_and_evaluate(model, X_train, y_train, X_test, y_test)
print(results)


