import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import sys


def main():
    data = pd.read_csv(sys.argv[1])
    y = data['city']
    X = data.drop(['city'], axis=1)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    
    #knn_model = make_pipeline(
    #    StandardScaler(),
    #    KNeighborsClassifier(n_neighbors=20))
    #rf_model = make_pipeline(
    #    StandardScaler(),
    #    RandomForestClassifier(n_estimators=50,
    #                           max_depth=6, min_samples_leaf=12)
    #)
    svc_model = make_pipeline(
        StandardScaler(),
        SVC(kernel='linear', C=2.0))
    
    #knn_model.fit(X_train, y_train)
    #print("Knn")
    #print(knn_model.score(X_train, y_train))
    #print(knn_model.score(X_valid, y_valid))

    #rf_model.fit(X_train, y_train)
    #print("Random forest")
    #print(rf_model.score(X_train, y_train))
    #print(rf_model.score(X_valid, y_valid))

    svc_model.fit(X_train, y_train)
    print("SVC")
    print(svc_model.score(X_train, y_train))
    print(svc_model.score(X_valid, y_valid))
    
    unlabelled = pd.read_csv(sys.argv[2])
    X_predict = unlabelled.drop(['city'], axis=1)
    #print(knn_model.predict(X_predict))
    #print(rf_model.predict(X_predict))
    #print(svc_model.predict(X_predict))
    predictions = svc_model.predict(X_predict)
    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
    #df = pd.DataFrame({'truth': y_valid,
    #                   'prediction': svc_model.predict(X_valid)})
    #print(df[df['truth'] != df['prediction']])
if __name__ == '__main__':
    main()
