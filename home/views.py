from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from django.utils.dateparse import parse_date, parse_datetime
from joblib import dump, load
# from keras.layers import LeakyReLU
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import KFold, StratifiedKFold
from collections import Counter
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import collections
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import time
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
# import tensorflow as tf
import imp
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from account.models import Profile
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
warnings.filterwarnings("ignore")
from home.models import Prediction

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 2):
            content = {}
            content['title'] = 'Welcome to Credit Card Fraud Detection'
            content['predictions'] = Prediction.objects.filter(profile_id = int(request.session['account_id'])).order_by('-id')
            return render(request, 'home/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def prediction(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 2):
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
                s_tran_num = tran_num
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
                predict = model.predict([[cc_num, amt, gender, pincode, lati, longi, int(
                    tran_num_str), unix_time, m_lati, m_longi]])

                if predict == 0:
                    content['result'] = 'Not fraud'
                else:
                    content['result'] = 'Is fraud'

                pr = Prediction()
                pr.trans_date_trans_time = date_time_data
                pr.cc_num = cc_num
                pr.amt = amt
                pr.gender = gender
                pr.zipcode = pincode
                pr.lat = lati
                pr.long = longi
                pr.unix_time = unix_time
                pr.merch_lat = m_lati
                pr.merch_long = m_longi
                pr.is_fraud = predict
                pr.trans_num = s_tran_num
                pr.profile = Profile.objects.get(pk = int(request.session['account_id']))
                pr.save()
            return render(request, 'home/predict.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def about(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 2):
            content = {}
            content['title'] = 'About Credit Card Fraud Detection'
            return render(request, 'home/about.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))