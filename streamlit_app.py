import streamlit as st
import pandas as pd
import joblib

# 🔹 Model dosya yolları
model_paths = {
    'Logistic Regression': {
        'SelectKBest': 'models/model_LogisticRegression_SelectKBest.pkl',
        'RFE': 'models/model_LogisticRegression_RFE.pkl',
        'Mutual Information': 'models/model_LogisticRegression_MutualInformation.pkl'
    },
    'Decision Tree': {
        'SelectKBest': 'models/model_DecisionTree_SelectKBest.pkl',
        'RFE': 'models/model_DecisionTree_RFE.pkl',
        'Mutual Information': 'models/model_DecisionTree_MutualInformation.pkl'
    },
    'Random Forest': {
        'SelectKBest': 'models/model_RandomForest_SelectKBest.pkl',
        'RFE': 'models/model_RandomForest_RFE.pkl',
        'Mutual Information': 'models/model_RandomForest_MutualInformation.pkl'
    },
    'SVM': {
        'SelectKBest': 'models/model_SVM_SelectKBest.pkl',
        'RFE': 'models/model_SVM_RFE.pkl',
        'Mutual Information': 'models/model_SVM_MutualInformation.pkl'
    }
}


# 🔸 Özellik setleri
feature_sets = {
    'SelectKBest': ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level',
                    'Heart Rate', 'Gender', 'Systolic', 'Diastolic', 'BMI Category', 'Occupation'],
    'RFE': ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Daily Steps',
            'Heart Rate', 'Gender', 'Systolic', 'Diastolic', 'BMI Category', 'Occupation'],
    'Mutual Information': ['Systolic', 'Diastolic', 'Daily Steps', 'Sleep Duration',
                           'Occupation', 'Age', 'BMI Category', 'Physical Activity Level',
                           'Heart Rate', 'Stress Level']
}

# 🔸 TR-EN etiket eşleşmeleri
label_map = {
    'Age': "Yaş (Age)",
    'Sleep Duration': "Uyku Süresi (Sleep Duration)",
    'Quality of Sleep': "Uyku Kalitesi (Quality of Sleep) (0-10)",
    'Physical Activity Level': "Fiziksel Aktivite (Physical Activity Level)",
    'Heart Rate': "Nabız (Heart Rate)",
    'Daily Steps': "Günlük Adım (Daily Steps)",
    'Systolic': "Büyük Tansiyon (Systolic)",
    'Diastolic': "Küçük Tansiyon (Diastolic)",
    'Stress Level': "Stres Seviyesi (Stress Level)",
    'BMI Category': "BMI Kategorisi",
    'Gender': "Cinsiyet (Gender)",
    'Occupation': "Meslek (Occupation)"
}

# 🔸 Encoding sözlükleri
occupation_options = {
    'Hemşire (Nurse)': 'Nurse',
    'Doktor (Doctor)': 'Doctor',
    'Mühendis (Engineer)': 'Engineer',
    'Avukat (Lawyer)': 'Lawyer',
    'Öğretmen (Teacher)': 'Teacher',
    'Muhasebeci (Accountant)': 'Accountant',
    'Satış Görevlisi (Salesperson)': 'Salesperson',
    'Bilim İnsanı / Yazılım Mühendisi (Scientist / Software Engineer)': 'Scientist',
    'Satış Temsilcisi (Sales Representative)': 'Sales Representative',
    'Yönetici (Manager)': 'Manager'
}

occupation_encoding = {
    'Nurse': 0.19518717,
    'Doctor': 0.18983957,
    'Engineer': 0.1684492,
    'Lawyer': 0.12566845,
    'Teacher': 0.10695187,
    'Accountant': 0.09893048,
    'Salesperson': 0.0855615,
    'Scientist': 0.01069519,  # ortak kullanım
    'Sales Representative': 0.00534759,
    'Manager': 0.0026738
}

bmi_encoding = {'Normal': 0, 'Overweight': 1, 'Obese': 2}
gender_encoding = {'Erkek (Male)': 1, 'Kadın (Female)': 0}

# 🎯 Streamlit Arayüzü
st.title("🛌 Uyku Bozukluğu Tahmini Uygulaması")
model_choice = st.selectbox("🔍 Model Seçin (en iyi model Logistic Regression)", list(model_paths.keys()))
feature_choice = st.selectbox("🧩 Özellik Seti Seçin (en iyi özellik seti SelectKBest)", list(feature_sets.keys()))

# 🔢 Form Girişi
st.subheader("📝 Girdi Verileri")
inputs = {}

for feature in feature_sets[feature_choice]:
    label = label_map.get(feature, feature)

    if feature == "Occupation":
        selected_occ = st.selectbox(label, list(occupation_options.keys()))
        inputs[feature] = occupation_encoding[occupation_options[selected_occ]]

    elif feature == "BMI Category":
        selected_bmi = st.selectbox(label, list(bmi_encoding.keys()))
        inputs[feature] = bmi_encoding[selected_bmi]

    elif feature == "Gender":
        selected_gender = st.selectbox(label, list(gender_encoding.keys()))
        inputs[feature] = gender_encoding[selected_gender]

    elif feature == "Quality of Sleep":
        inputs[feature] = st.number_input(label, min_value=0, max_value=10, step=1)
        
    else:
        # Geri kalan tüm sayısal alanlara negatif sınırı koy
        if feature in ['Age', 'Physical Activity Level', 'Heart Rate',
                       'Daily Steps', 'Stress Level', 'Systolic', 'Diastolic']:
            inputs[feature] = st.number_input(label, min_value=0, step=1)
        else:
            inputs[feature] = st.number_input(label, min_value=0.0, step=0.25)

# 🔍 Tahmin Butonu
if st.button("📊 Tahmin Et"):
    model_data = joblib.load(model_paths[model_choice][feature_choice])
    model = model_data['model']
    expected_features = model_data['features']

    # Girdi verisini sıraya sok
    ordered_inputs = {feat: inputs.get(feat, 0.0) for feat in expected_features}
    input_df = pd.DataFrame([ordered_inputs])

    # Tahmin yap ve göster
    prediction = model.predict(input_df)[0]
    label_map_result = {
       0: 'None (Normal)',
       1: 'Insomnia (Uykusuzluk)',
       2: 'Sleep Apnea (Uyku Apnesi)'
    }
    st.success(f"✅ Tahmin Sonucu: **{label_map_result[prediction]}**")
