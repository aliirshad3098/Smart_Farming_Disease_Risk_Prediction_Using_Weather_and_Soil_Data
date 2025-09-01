######################## Import Dependencies ###################

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


################################################################

################# Model Definition #############################

# model = {
#     "lr" : LogisticRegression(),
#     "svm":SVC(),
#     "rf": RandomForestClassifier(),
#     "xgb" : XGBClassifier()
# }


# Dictionary of models for multiclass classification
model = {
    "lr": LogisticRegression(
        solver="lbfgs",           # supports multinomial loss
        multi_class="multinomial",
        max_iter=500,
        C=1.0,
        random_state=42
    ),
    
    

    # "svm": SVC(
    #     kernel="linear",          # simpler kernel for clean data
    #     C=1.0,
    #     probability=True,
    #     decision_function_shape="ovr",  # one-vs-rest for multiclass
    #     random_state=42
    # ),
    
    

    "rf": RandomForestClassifier(
        n_estimators=200,
        max_depth=4,
        n_jobs=-1,
        random_state=42
    ),



    "xgb": XGBClassifier(
        n_estimators=250,
        learning_rate=0.01,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective="multi:softprob",
        num_class=3,
        eval_metric="mlogloss")
}
