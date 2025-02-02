import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
import sys


def main():
    data = pd.read_csv(sys.argv[1])
    y = data['city']
    X = data.drop(['city'], axis=1)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    
    svc_model = make_pipeline(
        StandardScaler(),
        SVC(kernel='linear', C=2.0))
    

    svc_model.fit(X_train, y_train)
    print(svc_model.score(X_train, y_train))
    print(svc_model.score(X_valid, y_valid))
    
    unlabelled = pd.read_csv(sys.argv[2])
    X_predict = unlabelled.drop(['city'], axis=1)

    predictions = svc_model.predict(X_predict)
    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
    #df = pd.DataFrame({'truth': y_train,
    #                   'prediction': svc_model.predict(X_train)})
    #print(df[df['truth'] != df['prediction']])
if __name__ == '__main__':
    main()
