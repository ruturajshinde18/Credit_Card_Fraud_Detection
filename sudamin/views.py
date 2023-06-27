from django.utils.dateparse import parse_date, parse_datetime
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import time
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import imp
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from account.models import Profile
import os
from sklearn.pipeline import Pipeline
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import numpy as np 
import pandas as pd 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA, TruncatedSVD
import time
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import collections
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, accuracy_score, classification_report
from collections import Counter
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix
from joblib import dump, load

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Welcome to Credit Card Fraud Detection'
            return render(request, 'admin/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def dataset(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Build model from dataset'
            content['lr_acc'] = '0'
            content['rfc_acc'] = '0'
            content['svc_acc'] = '0'
            if request.method == 'POST':
                df = pd.read_csv(str(BASE_DIR) + '/dataset/dataset.csv')
                df = df.drop("Unnamed: 0", axis=1)
                # print(df.shape[0])
                # print(df['is_fraud'].unique())
                # print(df['is_fraud'].value_counts())

                vectorizer = CountVectorizer(analyzer=lambda x: x)
                df['trans_num'] = vectorizer.fit_transform(df['trans_num']).toarray()

                df.drop(['trans_date_trans_time', 'category', 'merchant', 'first', 'last', 'city', 'street', 'state', 'city_pop', 'job', 'dob'], axis=1, inplace=True)

                df['gender'] = df['gender'].map({'M': 1, 'F': 0})

                # print(df.head())
                features = [
                    'cc_num',
                    'amt',
                    'gender',
                    'zip',
                    'lat',
                    'long',
                    'trans_num',
                    'unix_time',
                    'merch_lat',
                    'merch_long',
                ]
                X = df[features]
                y = df['is_fraud']

                # print(X.shape[0])
                # print(y.shape[0])

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

                # # Random Forest Classifier
                rfc = RandomForestClassifier()
                rfc.fit(X_train, y_train)
                dump(rfc, str(BASE_DIR) + '/model/modelRFC.pkl')
                y_pred_rfc = rfc.predict(X_test)
                content['y_pred_rfc'] = y_pred_rfc
                rfc_acc = accuracy_score(y_test, y_pred_rfc)
                content['rfc_acc'] = rfc_acc


                messages.success(request, "Model build done.")
            return render(request, 'admin/dataset.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def prediction(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Prediction from Admin'
            content['result'] = ''
            if request.method == 'POST':
                cc_num = float(request.POST['cc_num'])
                amt = float(request.POST['amt']) / 82
                gender = float(request.POST['gender'])
                pincode = float(request.POST['pincode'])
                date_time = request.POST['date_time']
                lati = float(request.POST['lati'])
                longi = float(request.POST['longi'])
                m_lati = float(request.POST['m_lati'])
                m_longi = float(request.POST['m_longi'])
                tran_num = request.POST['tran_num']
                # Load the model
                model = load(str(BASE_DIR) + '/model/modelRFC.pkl')

                date_time_data = parse_datetime(date_time)
                # print('-----------')
                # print(date_time_data)
                # print('-----------')
                unix_time = time.mktime(date_time_data.timetuple())

                vectorizer = CountVectorizer(analyzer=lambda x: x)
                tran_num = vectorizer.fit_transform([tran_num]).toarray()
                tran_num_i = tran_num[0].astype(np.int64)
                tran_num_str = str(tran_num_i)
                tran_num_str = tran_num_str.lstrip('[').rstrip(']')
                tran_num_str = tran_num_str.replace(" ", "")
                # print(f"String is {tran_num_str}")
                predict = model.predict([[cc_num, amt, gender, pincode, lati, longi, int(tran_num_str), unix_time, m_lati, m_longi]])

                if predict == 0:
                    content['result'] = 'Not fraud'
                else:
                    content['result'] = 'Is fraud'
            return render(request, 'admin/predict.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))