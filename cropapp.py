import streamlit as st

st.title("Welcome to crop App")

N=st.slider("Select N=",0,140)
P=st.slider("Select P=",5,145)
K=st.slider("Select K=",5,205)
emperature=st.slider("Select emperature=",8.8,43.6)
humidity=st.slider("Select humidity=",14.2,99.9)
ph=st.slider("Select ph=",3.5,9.9)
Rainfall=st.slider("Select Rainfall=",20.2,298.5)

import pickle
model=pickle.load(open("crop.pkl","rb"))
if st.button("Predict"):
    prd=model.predict([[N,P,K,emperature,humidity,ph,Rainfall]])
    st.success("The crop is "+ prd[0])

