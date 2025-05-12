import streamlit as st
import pandas as pd
import joblib

# Model dosya yolları
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


# Özellik setleri
# Özellik setleri (kendi belirlediğin sütunlara göre güncellenmiştir)
feature_sets = {
    'SelectKBest': ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Gender'],
    'RFE': ['Age', 'Gender', 'Quality of Sleep', 'Heart Rate', 'Sleep Duration'],
    'Mutual Information': ['Age', 'BMI Category', 'Sleep Duration', 'Daily Steps', 'Physical Activity Level']
}


# TR-EN etiket eşleşmeleri
# Özellik setleri (güncellenmiş)
feature_sets = {
    'SelectKBest': ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Gender'],
    'RFE': ['Age', 'Gender', 'Quality of Sleep', 'Heart Rate', 'Sleep Duration'],
    'Mutual Information': ['Age', 'BMI Category', 'Sleep Duration', 'Daily Steps', 'Physical Activity Level']
}

# TR-EN etiket eşleşmeleri
label_map = {
    'Age': "Yaş (Age)",
    'Sleep Duration': "Uyku Süresi (Sleep Duration)",
    'Quality of Sleep': "Uyku Kalitesi (Quality of Sleep) (0-10)",
    'Physical Activity Level': "Fiziksel Aktivite (Physical Activity Level)",
    'Heart Rate': "Nabız (Heart Rate)",
    'Daily Steps': "Günlük Adım (Daily Steps)",
    'BMI Category': "BMI Kategorisi",
    'Gender': "Cinsiyet (Gender)"
}

# Encoding sözlükleri
bmi_encoding = {'Normal': 0, 'Aşırı Kilolu (Overweight)': 1, 'Obez (Obese)': 2}
gender_encoding = {'Erkek (Male)': 1, 'Kadın (Female)': 0}

# Streamlit Arayüzü
st.title("🛌 Uyku Bozukluğu Tahmini Uygulaması")
model_choice = st.selectbox("🔍 Model Seçin (En iyi model: Random Forest)", list(model_paths.keys()))
feature_choice = st.selectbox("🧩 Özellik Seti Seçin (En iyi set: RFE)", list(feature_sets.keys()))

# Girdi Formu
st.subheader("📝 Girdi Verileri")
inputs = {}

for feature in feature_sets[feature_choice]:
    label = label_map.get(feature, feature)

    if feature == "BMI Category":
        selected_bmi = st.selectbox(label, list(bmi_encoding.keys()))
        inputs[feature] = bmi_encoding[selected_bmi]

    elif feature == "Gender":
        selected_gender = st.selectbox(label, list(gender_encoding.keys()))
        inputs[feature] = gender_encoding[selected_gender]

    elif feature == "Quality of Sleep":
        inputs[feature] = st.number_input(label, min_value=0, max_value=10, step=1)

    elif feature == "Physical Activity Level":
        inputs[feature] = st.number_input(label, min_value=0, max_value=10, step=1)

    else:
        # Diğer tüm sayısal alanlar
        inputs[feature] = st.number_input(label, min_value=0, step=1)

# Tahmin Butonu
if st.button("📊 Tahmin Et"):
    model_data = joblib.load(model_paths[model_choice][feature_choice])
    model = model_data['model']
    expected_features = model_data['features']

    # Sıralı giriş verisi oluştur
    ordered_inputs = {feat: inputs.get(feat, 0.0) for feat in expected_features}
    input_df = pd.DataFrame([ordered_inputs])

    # Tahmin yap
    prediction = model.predict(input_df)[0]
    label_map_result = {
       0: 'None (Normal)',
       1: 'Insomnia (Uykusuzluk)',
       2: 'Sleep Apnea (Uyku Apnesi)'
    }

    st.success(f"✅ Tahmin Sonucu: **{label_map_result[prediction]}**")
