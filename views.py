from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from urllib import request
from django.http import  JsonResponse
from django.shortcuts import render, redirect
from .models import newuser,student,Contact

from django.contrib import messages


def navbar(request):
    return render(request, 'base.html')




def user_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        pass1 = request.POST['pass1']

        # Check if the Aadhaar number and password match an existing student
        student = newuser.objects.filter(Username=Username, pass1=pass1).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            request.session['student_id'] = student.id
            messages.success(request,"LOGIN SUCCESSFULLY ... ")
            return redirect('userhome')

        messages.success(request,"INVALID ID OR PASSWORD ... ")
        return redirect('user_login')

    # return render(request, 'login.html')
    return render(request,'login.html')




def user_registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if newuser.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('user_registration')
        else:
            newuser(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('user_login')
    else:
         return render(request,'register.html')


def logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')

def userhome(request):
    return render(request,'user_home.html')



def admin_login(request):
    if request.method== 'POST':
        try:
            Userdetailes=student.objects.get(Username=request.POST['Username'], pass1=request.POST['pass1'])
            print("Username=",Userdetailes)
            request.session['Username']=Userdetailes.Username
            messages.success(request,"successfully login")
            return redirect('admin_home')
        except student.DoesNotExist as e:   
            messages.error(request,"Username/ Password Invalied...!")
   
    return render(request,'admin_login.html')


def admin_registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if student.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('admin_registration')
        else:
            student(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('admin_login')
    else:
         return render(request,'admin_register.html')


def admin_logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')



def admin_home(request):
    return render(request,'admin_home.html')




def user_contact(request):
    if request.method=='POST':
        names=request.POST['names']
        email=request.POST['email']
        phone=request.POST['phone']
        desc=request.POST['desc']
        contacts= Contact(names=names,email=email,phone=phone,desc=desc)
        contacts.save()    
        return redirect('user_contact')
    else:
        return render(request,'user_contact.html')


def user_about(request):
    return render(request,'about.html')



def view_user(request):
    form=newuser.objects.all()
    return render(request,'view_user.html' , {'forms':form})


import joblib
import pandas as pd
from django.shortcuts import render

# Features for prediction
features = ['avg_returns', 'volatility', 'risk_adjusted_returns', 'performance_index',
            'expense_ratio', 'rating']

# Sample DataFrame (Replace this with your actual data source)
df = pd.read_csv('models/processed_mutual_funds_data.csv')


def get_recommendations(request):
    if request.method == 'POST':
        horizon = request.POST['horizon']
        risk_profile = request.POST['risk']
        print(horizon, risk_profile)

        # Filter data by risk profile
        filtered_df = df[df['risk_profile_cluster'] == risk_profile]

        # Rank by predicted returns and get top 3
        top_recommendations = filtered_df.sort_values(by='predicted_return', ascending=False).head(3)
        print(top_recommendations)

        # Prepare context for template
        context = {
            'horizon': horizon,
            'risk_profile': risk_profile,
            'recommendations': top_recommendations[['scheme_name', 'predicted_return']]
        }

        return render(request, 'result.html', context)

    return render(request, 'form.html')



from django.shortcuts import render
import numpy as np
import pandas as pd
import pickle

# Load the trained models
model1yr =pickle.load(open('models/xgb_reg_1yr.pkl', 'rb'))
model3yr =pickle.load(open('models/gb_reg_3yr.pkl', 'rb'))
model5yr =pickle.load(open('models/gb_reg_5yr.pkl', 'rb'))

# Load Dataset for Scheme Names
df = pd.read_csv('models/recommendations_processed_mutual_funds_data.csv')
schemes = df['scheme_name']

def input_form(request):
    if request.method == 'POST':
        try:
            # Get Form Data
            features_value = [
                float(request.POST.get('avg_returns', 0)),
                float(request.POST.get('volatility', 0)),
                float(request.POST.get('risk_adjusted_returns', 0)),
                float(request.POST.get('performance_index', 0)),
                float(request.POST.get('expense_ratio', 0)),
                int(request.POST.get('rating', 0))
            ]
            print(features_value)

            features_name = ['avg_returns', 'volatility', 'risk_adjusted_returns', 'performance_index', 'expense_ratio', 'rating']
            df_new = pd.DataFrame([features_value], columns=features_name)

            # Model Predictions
            pred1 = model1yr.predict(df_new)
            pred3 = model3yr.predict(df_new)
            pred5 = model5yr.predict(df_new)

            # Convert float32 to Python float before storing in session
            request.session['pred1'] = round(float(pred1[0]), 2)
            request.session['pred3'] = round(float(pred3[0]), 2)
            request.session['pred5'] = round(float(pred5[0]), 2)

            # Redirect to /result/
            return redirect('result')

        except Exception as e:
            print("Error:", e)  # Debugging
            return render(request, 'form.html', {'error': 'Invalid input data'})

    return render(request, 'form.html')



def result(request):
    if request.method == 'POST':
        year_horizon = int(request.POST['horizon'])  # 1, 3, or 5 years
        risk_profile_cluster = int(request.POST['risk'])  # Conservative (0), Balanced (1), Aggressive (2)

        # Load the pre-processed data
        recommendations = pd.read_csv('models/recommendations_processed_mutual_funds_data.csv')

        # Calculate rank columns before filtering
        for horizon in ['predicted_returns_1yr', 'predicted_returns_3yr', 'predicted_returns_5yr']:
            recommendations[f'rank_{horizon}'] = recommendations.groupby('risk_profile_cluster')[horizon].rank(
                ascending=False)

        # Filter recommendations based on selected year horizon and risk profile
        horizon_column = f'predicted_returns_{year_horizon}yr'
        rank_column = f'rank_{horizon_column}'
        filtered_recommendations = recommendations[
            (recommendations['risk_profile_cluster'] == risk_profile_cluster) &
            (recommendations[rank_column] <= 3)
            ]

        a = filtered_recommendations[['scheme_name', horizon_column, rank_column]].to_dict(
                orient='records')

        values = [list(d.values()) for d in a]

        b_sorted = sorted(values, key=lambda x: x[2])


        # Prepare context for template
        context = {
            'horizon': year_horizon,
            'risk_profile': risk_profile_cluster,
            'b':b_sorted
        }

        return render(request, 'recommendation.html', context)

    context = {
        "pred1": round(float(request.session.get('pred5', 0)), 2),
        "pred3": round(float(request.session.get('pred3', 0)), 2),
        "pred5": round(float(request.session.get('pred1', 0)), 2),
    }
    return render(request, 'result.html', context)

def recommend(request):
    return render(request, 'recommendation.html')
