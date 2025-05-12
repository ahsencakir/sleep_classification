
# Uyku Bozukluğu Tahmin Projesi

## 📌 Veri Seti Seçim Nedeni

Bu proje kapsamında uyku bozukluklarını sınıflandırmak için hem gündelik yaşantıdan hem de kalp ritmi, kan basıncı gibi sağlık açısından kapsamlı verilere sahip olduğu için tercih edilmiştir. Bu veri setini seçmemizin başlıca nedenleri şunlardır:

- **Toplum Sağlığı Açısından Önemi:** Uyku bozuklukları hem fiziksel hem zihinsel sağlık üzerinde ciddi etkiler yaratabilir. Bu bozuklukları erken teşhis etmek yaşam kalitesini artırır.
- **Kapsamlı Özellik Seti:** Yaş, nabız, stres seviyesi, tansiyon, BMI, meslek gibi birçok fizyolojik ve yaşam tarzı değişkeni barındırır.
- **Makine Öğrenmesi Uygunluğu:** Hem kategorik hem sayısal veriler içerdiğinden çeşitli modelleme ve ön işleme teknikleriyle entegre çalışmaya uygundur.

---

## ⚙️ Özellik Seçim Yöntemleri

Aşağıdaki üç farklı özellik seçim yöntemi kullanılmış ve performansları karşılaştırılmıştır:

### 1. **SelectKBest (f_classif)**
- ANOVA F-skoruna göre en anlamlı özellikleri seçer.
- Sınıflandırma problemlerine uygundur.
- Basit ve etkili bir yöntemdir.

### 2. **RFE (Recursive Feature Elimination)**
- Model destekli bir yöntemdir.
- Önemsiz özellikleri iteratif olarak eler.
- Genellikle doğruluğu artırır fakat işlem süresi uzundur.

### 3. **Mutual Information**
- Özelliklerin hedef değişkenle olan bilgi kazanımını ölçer.
- Doğrusal olmayan ilişkileri yakalayabilir.
- Uyku süresi, tansiyon ve meslek gibi alanlarda etkili sonuçlar vermiştir.

---

## 🤖 Uygulanan Modeller ve Değerlendirme

| Sıra | Model Adı               | Tür / Yaklaşım              | Açıklama                                                                                                 |
|------|--------------------------|-----------------------------|----------------------------------------------------------------------------------------------------------|
| 1    | **Logistic Regression**  | Lineer / Parametrik         | Basit, hızlı, doğrusal sınırlar çizen ve yorumlaması kolay bir model.                                   |
| 2    | **Decision Tree**        | Karar Ağacı / Kural Bazlı   | İf-else mantığıyla dallanarak çalışır. Yorumu kolaydır fakat overfitting riski taşır.                   |
| 3    | **Random Forest**        | Ensemble / Bagging          | Birden fazla karar ağacını birleştirerek çalışır. Genellikle yüksek doğruluk sağlar.                    |
| 4    | **Support Vector Machine (SVM)** | Margin-Maximizing / Kernel | Sınıflar arasındaki mesafeyi maksimize eder. Karmaşık ayrımlar için uygundur, küçük verilerde etkilidir.|

---

## 📊 Genel Değerlendirme

- Özellik seçimi yöntemleri arasında `Mutual Information` yöntemi özellikle Systolic, Diastolic ve Sleep Duration gibi sağlıkla ilişkili değişkenleri öne çıkarmıştır.
- Random Forest ve Logistic Regression modelleri genellikle en iyi genel doğruluk ve F1 skorunu sağlamıştır.
- SVM karmaşık yapılı sınırlar için etkili olmuş, Decision Tree ise yorumlanabilirliğiyle ön plana çıkmıştır.
- Model performansları `Accuracy`, `Precision`, `Recall` ve `F1-Score` gibi metriklerle karşılaştırılmıştır.

---

## 🚀 Nasıl Çalıştırılır?

### Gereksinimler:
```
streamlit
pandas
scikit-learn
joblib
```

### Kurulum:

```bash
pip install -r requirements.txt
```

### Uygulama Başlatma:

```bash
streamlit run streamlit_app.py
```

---

## 🌐 Canlı Demo
> Hazırladığımız demoyu inceleyebilirsiniz: [Uyku Bozukluğu Tahmin Uygulaması](https://sleepclassification.streamlit.app/)

