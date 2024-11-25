import streamlit as st
from PIL import Image
import re
import sqlite3 
import pickle
import bz2
import os
import pandas as pd



#database
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()



def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''      
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://img.freepik.com/premium-photo/spring-grain-concept-agriculture-healthy-eating-organic-food-generative-ai_58409-32489.jpg");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()



menu = ["Home","Login","SignUp","Contact US"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
        """
        <h2 style="color: Black; text-align: center;">Welcome to Crop Recommendation</h2>
        <br>
        <p style="text-align: justify; font-size: 18px; color: black;">
            The Indian economy is heavily contributed to by agriculture. Most Indian farmers rely on their instincts to decide the crop to be sown at a particular time of the year. 
            They do not realize that the crop output is circumstantial and heavily dependent on the present-day weather and soil conditions. A single uninformed decision by the farmer 
            can have undesirable consequences on the economic conditions of the region, as well as mental and financial impacts on the farmer himself.
            Applying systematic Machine Learning models can effectively help alleviate this issue. The dataset used in the project is built by combining datasets of India's rainfall, 
            climate, and soil. Machine learning models will be applied to the dataset to identify the most accurate model for recommending a crop based on the farm's location. 
            This recommendation will help Indian farmers make informed decisions about the crops. Parameters such as the farm's location, sowing season, soil properties, and climate 
            will be considered for the recommendation.
        </p>
        """,
        unsafe_allow_html=True
    )

    
if choice=="Login":
    st.markdown(
        """
        <h2 style="color:Black">Login Section</h2>
        """
        ,unsafe_allow_html=True)
    Email = st.text_input("Email")
    Password = st.text_input("Password",type="password")
    b1=st.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu1 = ["Weather","Soil","Both"]
                    choice1 = st.selectbox("Select Parameters",menu1)
                    menu2 = ["VotingClassifier"] #["K-Nearest Neighbors", "SVM", "Decision Tree", "Random Forest", "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)
                    if choice1=="Weather":
                        temp=float(st.slider('temp Value', 8.0, 44.0))
                        Hum=float(st.slider('Humidity Value', 14.0, 100.0))
                        Rain=float(st.slider('rainfall Value', 20.0, 299.0))
                        b2=st.button("Recommend")
                        sfile = bz2.BZ2File('All Model Weather', 'r')
                        model=pickle.load(sfile)
                        le=pickle.load(open('le Weather.pkl', 'rb'))
                        tdata=[temp,Hum,Rain]
                        
    
                    if choice1=="Soil":
                        N=float(st.slider('N Value', 0.0, 140.0))
                        P=float(st.slider('P Value', 5.0, 145.0))
                        K=float(st.slider('K Value', 5.0, 205.0))
                        Ph=float(st.slider('ph Value', 3.5, 10.0))
                        b2=st.button("Recommand")
                        sfile = bz2.BZ2File('All Model Soil', 'r')
                        model=pickle.load(sfile)
                        le=pickle.load(open('le Soil.pkl', 'rb'))
                        tdata=[N,P,K,Ph]
                        
                    if choice1=="Both":
                        N=float(st.slider('N Value', 0.0, 140.0))
                        P=float(st.slider('P Value', 5.0, 145.0))
                        K=float(st.slider('K Value', 5.0, 205.0))
                        temp=float(st.slider('temp Value', 8.0, 44.0))
                        Hum=float(st.slider('Humidity Value', 14.0, 100.0))
                        Ph=float(st.slider('ph Value', 3.5, 10.0))
                        Rain=float(st.slider('rainfall Value', 20.0, 299.0))
                        b2=st.button("Recommand")
                        sfile = bz2.BZ2File('All Model', 'r')
                        model=pickle.load(sfile)
                        le=pickle.load(open('le.pkl', 'rb'))
                        tdata=[N,P,K,temp,Hum,Ph,Rain]
                        
                    if b2:
                        fruits=['banana','pomegranate','mango','grapes','watermelon','muskmelon','apple','orange','papaya','coconut',]
                        beans=['cotton','jute','maize']
                        pulses=['rice','chikpea','kidneybeans','pigeonpeas','mothbeans','mungbeans','blackgram','lentil',]
                        coffee=['coffee']
                        # if choice2=="K-Nearest Neighbors":
                        #     test_prediction = model[0].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)
                        # if choice2=="SVM":
                        #     test_prediction = model[1].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)                  
                        # if choice2=="Decision Tree":
                        #     test_prediction = model[2].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)
                        # if choice2=="Random Forest":
                        #     test_prediction = model[3].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)
                        # if choice2=="Naive Bayes":
                        #     test_prediction = model[4].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)
                        # if choice2=="ExtraTreesClassifier":
                        #     test_prediction = model[5].predict([tdata])
                        #     label=le.inverse_transform(test_prediction)
                        #     query=label[0]
                        #     if query in fruits:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Jarvi seeds PVT.LTD'],
                        #                   "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                        #                   "Contact": ['91-98796 86866']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     elif query in beans:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Mineral & General Co. Ltd'],
                        #                   "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                        #                   "Contact": ['91-7701989669']                                          
                        #                 }
                        #         st.dataframe(data)
                        #     elif query in pulses:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                        #                   "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                        #                   "Contact": ['+91-9081789111']                                          
                        #                 }
                        #         st.dataframe(data)

                        #     else:
                        #         data = {
                        #                   "Recommend Crops": [label[0]],
                        #                   "Agent Name": ['BHARAT COFFEE DEPOT'],
                        #                   "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                        #                   "Contact": ['+91-9924481590']                                          
                        #                 }
                        #         st.dataframe(data)
                        if choice2=="VotingClassifier":
                            test_prediction = model[6].predict([tdata])
                            label=le.inverse_transform(test_prediction)
                            query=label[0]
                            if query in fruits:
                                data = {
                                          "Recommend Crops": [label[0]],
                                          "Agent Name": ['Jarvi seeds PVT.LTD'],
                                          "Adress": ['Jarviseeds, Opp. Water Tank At Post : Bharadia, Taluka-Valiya, Dist-Bharuch, Gujarat, India-393135'],
                                          "Contact": ['91-98796 86866']                                          
                                        }
                                st.dataframe(data)

                            elif query in beans:
                                data = {
                                          "Recommend Crops": [label[0]],
                                          "Agent Name": ['Mineral & General Co. Ltd'],
                                          "Adress": ['512, Ganesh Glory, Near BSNL Office, Jagatpur Road, Sarkhej - Gandhinagar Hwy, Ahmedabad, Gujarat 382470'],
                                          "Contact": ['91-7701989669']                                          
                                        }
                                st.dataframe(data)
                            elif query in pulses:
                                data = {
                                          "Recommend Crops": [label[0]],
                                          "Agent Name": ['Yagna Agro Industries Pvt. Ltd'],
                                          "Adress": ['456, 457/1, Purshottam Pura Road, Naika, Gujarat 387550'],
                                          "Contact": ['+91-9081789111']                                          
                                        }
                                st.dataframe(data)

                            else:
                                data = {
                                          "Recommend Crops": [label[0]],
                                          "Agent Name": ['BHARAT COFFEE DEPOT'],
                                          "Adress": ['opposite Rajdhani Hotel, Parkar Wada, Dandia Bazar, Babajipura, Vadodara, Gujarat 390001'],
                                          "Contact": ['+91-9924481590']                                          
                                        }
                                st.dataframe(data)
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           
if choice=="SignUp":
    st.markdown(
        """
        <h2 style="color:Black">SignUp Section</h2>
        """
        ,unsafe_allow_html=True)
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")
                       
            else:
                
                st.warning("Not Valid Mobile Number")
        else:
        
            
            st.warning("Pass Does Not Match")
            
        

if choice=="Contact US":
    import numpy as np
    st.subheader("Contact US Section\n\n\n")
    image1 = Image.open('1 jpg.jpeg')
    image2 = Image.open('2 jpg.jpg')
    image3 = Image.open('3 jpg.jpg')
    image4 = Image.open('4 jpg.jpg')
    st.image([image1.resize((150, 200)),np.ones([150,20]),image2.resize((150, 200)),np.ones([150,20]),image3.resize((150, 200)),np.ones([200,20]),image4.resize((150, 200))])    
    #st.text("<    "+"Hetvi             Devanshi               Riya	          Drashti >")
     
