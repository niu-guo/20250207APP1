# 导入需要的库
import streamlit as st
import pandas as pd
import joblib

st.header('A Web Calculator to Predict Interstitial Lung Disease in Systemic Lupus Erythematosus Patients')
st.sidebar.header('Variables')




a = st.sidebar.slider("Age (years)", min_value=14, max_value=80, step=1)
b = st.sidebar.selectbox("Pulmonary artery systolic pressure >30mmHg", ("No/Unknown","Yes"))
c = st.sidebar.selectbox("Raynaud’s phenomenon", ("No","Yes"))
d = st.sidebar.selectbox("Platelet count <100*10$^9$/L", ("No","Yes"))
e = st.sidebar.selectbox("Serositis", ("No/Unknown","Yes"))
f = st.sidebar.selectbox("Anti-U1RNP antibodies", ("-","+"))
g = st.sidebar.slider("Disease course (months)", min_value=0, max_value=860, step=1)
h = st.sidebar.slider("SLEDAI-2k", min_value=0, max_value=26, step=1)
i = st.sidebar.selectbox("Anti-Ro52 antibodies", ("-","+"))


# 如果按下按钮
if st.button("Predict"):  # 显示按钮
    # 加载训练好的模型
    model = joblib.load("XGBoost.pkl")
    # 将输入存储DataFrame
    X = pd.DataFrame([[a,b,c,d,e,f,g,h,i]],
                     columns = ['Age ', 'PAH', 'Raynaud\'s phenomenon', 'PLT', 'Serositis',
       'Anti-U1snRNP   ', 'Course', 'SLEDAI', 'Anti-SSARo52   '])

    X = X.replace(["No","No/Unknown","Yes"],
                                [0, 0, 1])
    X = X.replace(["-", "+"],
                  [0, 1])
    # 进行预测
    # prediction = model.predict(X)[0]
    Predict_proba = model.predict_proba(X)[:, 1][0]
    # 输出预测结果
    if  Predict_proba >= 0.197:
        st.subheader(f"Risk grouping in SLE-ILD: High Risk")
    else:
        st.subheader(f"Risk grouping in SLE-ILD: Low Risk")
    st.subheader(f"Probability of SLE-ILD:  {'%.2f' % float(Predict_proba * 100) + '%'}")

