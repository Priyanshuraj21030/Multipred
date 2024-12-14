from django.shortcuts import HttpResponse, render
from sklearn.preprocessing import StandardScaler
from joblib import load
import pandas as pd

model = load('./ml_models/diabetes_model.joblib')
dataset = pd.read_csv('./ml_models/diabetes.csv')
X = dataset.drop(columns = 'Outcome', axis = 1)
columns_to_drop = ['BP', 'ST', 'INS', 'DPF']
X = X.drop(columns=columns_to_drop)
scaler = StandardScaler()
scaler.fit(X)

model2 = load('./ml_models/breastcancer_model.joblib')
dataset2 = pd.read_csv('./ml_models/breastcancer.csv')
X2 = dataset2.drop(columns = 'Outcome', axis = 1)
columns_to_drop = ['tm', 'sm', 'sym', 'fdm', 'rse', 'tse', 'pse', 'ase', 'sse', 'cse', 'cnse', 'cpse', 'symse', 'fdse', 'rw', 'tw', 'pw', 'aw', 'sw', 'cw', 'cnw', 'cpw', 'symw', 'fdw']
X2 = X2.drop(columns=columns_to_drop)
scaler2 = StandardScaler()
scaler2.fit(X2)

# Views functions
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def bmi(request):
    return render(request, 'bmi.html')

def services(request):
    return HttpResponse("This is Services Page")

def contact(request):
    return HttpResponse("This is Contact Page")

def diabetes(request):
    pg = request.POST.get('pgdb', '')  # Get the posted values or empty strings if not provided
    gl = request.POST.get('gldb', '')
    bm = request.POST.get('bmidb', '')
    age = request.POST.get('agedb', '')
    if request.method == 'POST':
        data = [[pg, gl, bm, age]]
        inp = scaler.transform(data)
        y_pred = model.predict(inp)
        if y_pred[0] == 1:
            result = "Diabetic"
        else:
            result = "Not Diabetic"
    else:
        result = None
    # Pass the form data and result to the template
    return render(request, 'diabetes.html', {'result': result, 'pg': pg, 'gl': gl, 'bm': bm, 'age': age})

def breastcancer(request):
    rm = request.POST.get('rm', '')  # Get the posted values or empty strings if not provided
    pm = request.POST.get('pm', '')
    am = request.POST.get('am', '')
    cm = request.POST.get('cm', '')
    cnm = request.POST.get('cnm', '')
    cpm = request.POST.get('cpm', '')
    if request.method == 'POST':
        data = [[rm, pm, am, cm, cnm, cpm]]
        inp = scaler2.transform(data)
        y_pred = model2.predict(inp)
        if y_pred[0] == 1:
            result = "Melignant"
        else:
            result = "Benign"
    else:
        result = None
    # Pass the form data and result to the template
    return render(request, 'breastcancer.html', {'result': result, 'rm': rm, 'pm': pm, 'am': am, 'cm': cm, 'cnm':cnm, 'cpm':cpm})
