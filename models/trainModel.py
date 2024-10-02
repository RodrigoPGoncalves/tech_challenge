import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import classification_report, roc_curve, auc, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import joblib
import db.db_data as dbData
import os



# Definindo as colunas
continuous_cols = ["age", "introversion_score", "sensing_score", "thinking_score", "judging_score"]
categorical_cols = ["gender","interest"]
others_cols = ["education"]
y_target = ["personality"]

def train_model():
    try:
        df = dbData.get_data_as_dataframe()
        
        le_gender = LabelEncoder()
        le_interest = LabelEncoder()
        le_y = LabelEncoder()
        scaler = MinMaxScaler()
        
        y = preprocess_dataY(df,le_y)
        X = preprocess_dataX(df, le_gender,le_interest,scaler)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf_classifier = RandomForestClassifier(
            n_estimators=200,
            min_samples_split=10,
            min_samples_leaf=4,
            max_depth=20,
            random_state=42)
        rf_classifier_fitted = rf_classifier.fit(X_train, y_train)
        
        save_dir = 'models'
        model_path = os.path.join(save_dir, 'rf_classifier_model.pkl')
        joblib.dump(rf_classifier_fitted, model_path)
        

        return 200, analise_dados_modelo(rf_classifier,
                        X_train,
                        y_train,
                        X_test,
                        y_test,
                        le_y.inverse_transform(y_train["personality"].unique()),
                        X_train.columns)
    except Exception as e:
        return 500, e
        
def predict_any_value(df):
    try:
        save_dir = 'models'
        le_y = joblib.load(os.path.join(save_dir, 'le_y.pkl'))
        model = joblib.load(os.path.join(save_dir, 'rf_classifier_model.pkl'))

        X_predict = preprocess_dataX(df)
        prediction = model.predict(X_predict)
        return 200, le_y.inverse_transform(prediction)
    except Exception as e:
        return 500, e

def analise_dados_modelo(modelo, x_train, y_train, x_test, y_test, targets, nameColums):
    modelo.fit(x_train, y_train)
    predicao = modelo.predict(x_test)
    
    return print_classification_report(y_test, targets, predicao)

def print_classification_report(y_test, targets, predicao):
    report_rf_Small = classification_report(y_test, predicao, target_names=targets, output_dict=True)
    return report_rf_Small

def preprocess_dataY(df,le_y=None):
    y_processed = pd.DataFrame()
    y_processed['personality'] = le_y.fit_transform(df['personality'])
    
    save_dir = 'models'
    joblib.dump(le_y, os.path.join(save_dir, 'le_y.pkl'))
    
    return y_processed

def preprocess_dataX(df, le_gender=None,le_interest=None,scaler=None):
    save_dir = 'models'
    if(le_gender == None):
        le_gender = joblib.load(os.path.join(save_dir, 'le_gender.pkl'))
        le_interest = joblib.load(os.path.join(save_dir, 'le_interest.pkl'))
        scaler = joblib.load(os.path.join(save_dir, 'scaler.pkl'))
    
        X_processed = pd.DataFrame()

        X_processed[categorical_cols[0]] = le_gender.transform(df[categorical_cols[0]].values)
        X_processed[categorical_cols[1]] = le_interest.transform(df[categorical_cols[1]].values)

        normalized_array = scaler.transform(df[continuous_cols])
        X_processed[continuous_cols] = pd.DataFrame(normalized_array, columns=continuous_cols)

        X_processed[others_cols] = df[others_cols]

    else:
        le_gender = joblib.load(os.path.join(save_dir, 'le_gender.pkl'))
        le_interest = joblib.load(os.path.join(save_dir, 'le_interest.pkl'))
        scaler = joblib.load(os.path.join(save_dir, 'scaler.pkl'))
    
        X_processed = pd.DataFrame()

        X_processed[categorical_cols[0]] = le_gender.fit_transform(df[categorical_cols[0]].values)
        X_processed[categorical_cols[1]] = le_interest.fit_transform(df[categorical_cols[1]].values)

        normalized_array = scaler.fit_transform(df[continuous_cols])
        X_processed[continuous_cols] = pd.DataFrame(normalized_array, columns=continuous_cols)

        X_processed[others_cols] = df[others_cols]
        
        #Salva dados de pré processamento
        joblib.dump(le_gender, os.path.join(save_dir, 'le_gender.pkl'))
        joblib.dump(le_interest, os.path.join(save_dir, 'le_interest.pkl'))
        joblib.dump(scaler, os.path.join(save_dir, 'scaler.pkl'))
    
    return X_processed
