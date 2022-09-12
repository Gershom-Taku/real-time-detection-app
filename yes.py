from asyncore import write
import pyrebase
from datetime import datetime
import importlib
from turtle import left, right
from click import style
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie
from sympy import N
from PIL import Image
import base64
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import numpy as np
import cv
import plotly.express as px
import io 
import pickle
import torch
import csv
import os
import sklearn

# Configuration Key
#firebaseConfig = {
 #   'apiKey': " ",
  #  'authDomain': " ",
   # 'projectId': " ",
    #'databaseURL': " ",
    #'#storageBucket': " ",
    #'m#essagingSenderId': "",
    #'appId': " ",
    #'measurementId': " "
#}
st.set_page_config(page_title="WELCOME TO All IN ONE APP", page_icon=":tada:", layout='wide')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html= True)  
local_css("style/style.css")

html_temp = """
        <div style = "background-color:royalblue;padding:10px;border-radius:30px;width :auto;">
        <h1 style = "color:white;text-align:center;font-size:40px;">All IN ONE DETECTION SOFTWARE APPLICATION </h1>
        </div>
        """
components.html(html_temp)

A,B = st.columns(2)
with A:
    st.write("Test your self and share your experience with others here!")
    
    st.success("It's fortunate to discover your self that you are health and safe🆗")
    st.warning("If you discover that you have been affected,please consult a doctor or hear from others here throuh their experiences and moments!🧑‍⚕️")
     
    
    with B:
        lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_6qyxpnwe.json")
        st_lottie(lottie_coding,height= 300,key = "care")

firebaseConfig = {
  'apiKey': "AIzaSyD8HUrdIhoZoBuHjs36oQsqzexAb_N5jMs",
  'authDomain': "all-in-one-detection-app.firebaseapp.com",
  'projectId': "all-in-one-detection-app",
  'databaseURL':"https://all-in-one-detection-app-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "all-in-one-detection-app.appspot.com",
  'messagingSenderId': "643426977084",
  'appId': "1:643426977084:web:8349da1abceb4c837f8a39",
  'measurementId': "G-VL0MLCR1YH"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
with st.sidebar:
 lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_6qyxpnwe.json")
 st_lottie(lottie_coding,height= 150,key = "caring")


st.sidebar.title("多动能一体检测用程序/All In One  Detection App")
#st.title("多动能一体检测用程序/All In One  Detection App")
  
# Authentication
choice = st.sidebar.selectbox('登录:login/注册:Signup', ['Login', 'Sign up'])
#choice = st.selectbox('登录:login/注册:Signup', ['Login', 'Sign up'])

   
# Obtain User Input for email and password
email = st.sidebar.text_input('输入邮件/Please enter your email address📩')
password = st.sidebar.text_input('输入密码/Please enter your password🔐', type='password')
#email = st.text_input('输入邮件/Please enter your email address')
#password = st.text_input('输入密码/Please enter your password', type='password')



# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
    'Please input your app name', value='Default')
    submit = st.sidebar.button('注册/Create my account🧾')
   # handle = st.text_input(
    #'Please input your app handle name', value='Default')
    #submit = st.button('注册/Create my account')


    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('注册成功/Your account is created suceesfully!📩')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + handle)
        st.info('通过登录下拉列表和选择登录/Login via login drop down selection🔑')

# Login Block
if choice == 'Login':
    login = st.sidebar.checkbox('登录/Login')
    #login = st.checkbox('登录/Login')

    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.write("---")
        bio = st.radio('Explore Now:', ['Home Page🏛️','Profile And Moments👨','Settings And Customization⚙️','Contact Us Page🤝','Self Test Page🩺'])

        # SETTINGS PAGE
        if bio == '设置和自己定义/Settings And Customization':
            # CHECK FOR IMAGE
            nImage = db.child(user['localId']).child("Image").get().val()
            # IMAGE FOUND
            if nImage is not None:
                # We plan to store all our image under the child image
                Image = db.child(user['localId']).child("Image").get()
                for img in Image.each():
                    img_choice = img.val()
                    # st.write(img_choice)
                    st.image(img_choice)
                    exp = st.beta_expander('改变图像/Change Bio and Image')
                # User plan to change profile picture
                with exp:
                    newImgPath = st.text_input('输入图像的完整路径/Enter full path of your profile image')
                    upload_new = st.button('上装/Upload')
                    if upload_new:
                        uid = user['localId']
                        fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                        db.child(user['localId']).child("Image").push(a_imgdata_url)
                        st.success('成功/Success!')
                        # IF THERE IS NO IMAGE
            else:
                st.info("No profile picture yet")
                newImgPath = st.text_input('输入图像的完整路径/Enter full path of your profile image')
                upload_new = st.button('上装/Upload')
                if upload_new:
                    uid = user['localId']
                    # Stored Initated Bucket in Firebase
                    fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                    # Get the url for easy access
                    a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                    # Put it in our real time database
                    db.child(user['localId']).child("Image").push(a_imgdata_url)
        # HOME PAGE
        elif bio == 'Home':
            st.write("---")
            col1, col2 = st.columns(2)

        # col for Profile picture
            with col1:
                nImage = db.child(user['localId']).child("Image").get().val()
                if nImage is not None:
                    val = db.child(user['localId']).child("Image").get()
                    for img in val.each():
                        img_choice = img.val()
                        st.image(img_choice, use_column_width=True)
                    else:
                        st.info("还没有个人资料图片/No profile picture yet. Go to Edit Profile and choose one!")

                        post = st.text_input("分享或发布你当前的心情/shouShare and Post Your Current Mood!", max_chars=100)
                        add_post = st.button('Share Posts')
                    if add_post:
                      now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                post = {'Post:': post,
                        'Timestamp': dt_string}
                results = db.child(user['localId']).child("Posts").push(post)
                st.balloons()

        # This coloumn for the post Display
            with col2:

                all_posts = db.child(user['localId']).child("Posts").get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                        # st.write(Posts.key()) # Morty
                        st.code(Posts.val(), language='')
        # WORKPLACE FEED PAGE
        else:
            all_users = db.get()
            res = []
            # Store all the users handle name
            for users_handle in all_users.each():
                k = users_handle.val()["Handle"]
                res.append(k)
            # Total users
                nl = len(res)
            st.write('Number Of Users In Use Of The App: ' + str(nl))

            # Allow the user to choose which other user he/she wants to see
            choice = st.selectbox('Friends In Circle', res)
            push = st.button('Show Profile/显示配置文件')

            # Show the choosen Profile
            if push:
                for users_handle in all_users.each():
                    k = users_handle.val()["Handle"]
                    if k == choice:
                        lid = users_handle.val()["ID"]

                        handlename = db.child(lid).child("Handle").get().val()

                        st.markdown(handlename, unsafe_allow_html=True)

                        nImage = db.child(lid).child("Image").get().val()
                        if nImage is not None:
                            val = db.child(lid).child("Image").get()
                            for img in val.each():
                                img_choice = img.val()
                                st.image(img_choice)
                            else:
                                st.info("还没有个人资料图片/No profile picture yet. Go to Edit Profile and choose one!")

                        # All posts
                        all_posts = db.child(lid).child("Posts").get()
                        if all_posts.val() is not None:
                            for Posts in reversed(all_posts.each()):
                                st.code(Posts.val(), language='')

        if bio == "Contact Us Page":
            st.write("----")
            #st.title(f"you have selected{selected}")
            st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Cooper Black'; color: blue;} 
                        </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Get in touch with All in one detection app members:</p>', unsafe_allow_html=True)
            contact_form = """
                     <input type = "hidden" name = " _capture" value = "false">
                     <form action="https://formsubmit.co/chototakudzwa8@gmail.com" method="POST">
                     <input type="text" name="name" placeholder = "Your name" required>
                     <input type="email" name="email" placeholder = "Your email" required>
                     <input type = "text" name = "company" placeholder = "Your company" required >
                     <textarea  name = "message" placeholder = "Enter message" required></textarea>
                     <button type="submit">Send</button>
                </form>

                     """

            st.markdown(contact_form, unsafe_allow_html=True)
          
#-----------------------------------------------------------------------------------------------------
        if bio == 'Self Test Page':
                        st.write("---")
                # loading the saved models

                        diabetes_model = pickle.load(
                          open(r'C:\Users\ADMIN\Desktop\app\diabetes_model.sav','rb'))


                        heart_disease_model = pickle.load(
                           open(r'C:\Users\ADMIN\Desktop\app\heart_disease_model.sav','rb'))


                        parkinsons_model = pickle.load(
                           open(r'C:\Users\ADMIN\Desktop\app\parkinsons_model.sav','rb'))

# sidebar for navigation
                        
                        bio = option_menu(menu_title=None ,options=

                                 ['Diabetes Prediction',
                                 'Heart Disease Prediction',
                                 'Parkinsons Prediction'],
                                 icons=['activity', 'heart', 'person'],
                                 default_index=0,orientation="horizontal")

                        styles={
                           "container ": {"padding": "0!important", "background-color": "white"},
                           "icon": {"color": "orange", "font-size": "25px"},
                           "nav-link": {
                            "font-size": "25px",
                            "text-align": "left",
                            "margin": "0px",
                             "--hover-color": "#eee",

                             },
                             "nav-link-selected": {"background-color": "blue"},
                               }
                            

                                   

# Diabetes Prediction Page
                        if (bio == 'Diabetes Prediction'):

    # page title
                              st.title('糖尿病的机器学习检测/Machine Learning Based Detection For Diabetes')

    # getting the input data from the user
                              col1, col2, col3 = st.columns(3)

                              with col1:
                                Pregnancies = st.text_input('Number of Pregnancies')

                              with col2:
                                  Glucose = st.text_input('Glucose Level')

                              with col3:
                                  BloodPressure = st.text_input('Blood Pressure value')

                              with col1:
                                 SkinThickness = st.text_input('Skin Thickness value')

                              with col2:
                                Insulin = st.text_input('Insulin Level')

                              with col3:
                                 BMI = st.text_input('BMI value')

                              with col1:
                                   DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

                              with col2:
                                    Age = st.text_input('Age of the Person')

    # code for Prediction
                                    diab_diagnosis = ''

    # creating a button for Prediction

                              if st.button('Diabetes Test Result/查结果'):
                                diab_prediction = diabetes_model.predict(
                                 [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

                                if (diab_prediction[0] == 1):
                                   diab_diagnosis = '这个人受到影响/The person is diabetic'
                                   st.warning(diab_diagnosis)
                                else:
                                   diab_diagnosis = '这个人没受到影响/The person is not diabetic'
                                   st.success(diab_diagnosis)

# Heart Disease Prediction Page
                        if (bio == 'Heart Disease Prediction'):

    # page title
                                st.title('基于机器学习的心脏病预测/Heart Disease Prediction based on Machine Learning')

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                         age = st.text_input('Age')

                                with col2:
                                    sex = st.text_input('Sex')

                                with col3:
                                     cp = st.text_input('Chest Pain types')

                                with col1:
                                     trestbps = st.text_input('Resting Blood Pressure')

                                with col2:
                                    chol = st.text_input('Serum Cholestoral in mg/dl')

                                with col3:
                                      fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

                                with col1:
                                      restecg = st.text_input('Resting Electrocardiographic results')

                                with col2:
                                    thalach = st.text_input('Maximum Heart Rate achieved')

                                with col3:
                                        exang = st.text_input('Exercise Induced Angina')

                                with col1:
                                   oldpeak = st.text_input('ST depression induced by exercise')

                                with col2:
                                    slope = st.text_input('Slope of the peak exercise ST segment')

                                with col3:
                                    ca = st.text_input('Major vessels colored by flourosopy')

                                with col1:
                                       thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
                                       heart_diagnosis = ''

    # creating a button for Prediction

                                if st.button('Heart Disease Test Result'):
                                    heart_prediction = heart_disease_model.predict(
                                    [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

                                    if (heart_prediction[0] == 1):
                                       heart_diagnosis = '这个人受到影响/The person is having heart disease'
                                       st.warning(heart_diagnosis)
                                    else:
                                       heart_diagnosis = '这个人没受到影响/The person does not have any heart disease'
                                       st.success(heart_diagnosis)

# Parkinson's Prediction Page
                        if (bio == "Parkinsons Prediction"):

    # page title
                                st.title("基于机器学习的帕金森病预测/Parkinson's Disease Prediction Based On Machine Learning")

                                col1, col2, col3, col4, col5 = st.columns(5)

                                with col1:
                                      fo = st.text_input('MDVP:Fo(Hz)')

                                with col2:
                                    fhi = st.text_input('MDVP:Fhi(Hz)')

                                with col3:
                                        flo = st.text_input('MDVP:Flo(Hz)')

                                with col4:
                                   Jitter_percent = st.text_input('MDVP:Jitter(%)')

                                with col5:
                                           Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

                                with col1:
                                   RAP = st.text_input('MDVP:RAP')

                                with col2:
                                    PPQ = st.text_input('MDVP:PPQ')

                                with col3:
                                   DDP = st.text_input('Jitter:DDP')

                                with col4:
                                    Shimmer = st.text_input('MDVP:Shimmer')

                                with col5:
                                           Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

                                with col1:
                                         APQ3 = st.text_input('Shimmer:APQ3')

                                with col2:
                                       APQ5 = st.text_input('Shimmer:APQ5')

                                with col3:
                                       APQ = st.text_input('MDVP:APQ')

                                with col4:
                                             DDA = st.text_input('Shimmer:DDA')

                                with col5:
                                        NHR = st.text_input('NHR')

                                with col1:
                                   HNR = st.text_input('HNR')

                                with col2:
                                       RPDE = st.text_input('RPDE')

                                with col3:
                                           DFA = st.text_input('DFA')

                                with col4:
                                  spread1 = st.text_input('spread1')

                                with col5:
                                         spread2 = st.text_input('spread2')

                                with col1:
                                    D2 = st.text_input('D2')

                                with col2:
                                    PPE = st.text_input('PPE')

    # code for Prediction
                                    parkinsons_diagnosis = ''

    # creating a button for Prediction
                                if st.button("Parkinson's/Brain Test Result"):
                                      parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                                                           Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE,
                                                           DFA, spread1, spread2, D2, PPE]])

                                      if (parkinsons_prediction[0] == 1):

                                       parkinsons_diagnosis = "这个人受到影响/The person has Parkinson's/Brain disease"
                                       st.warning(parkinsons_diagnosis)
                                      else:
                                       parkinsons_diagnosis = "这个人没受到影响/The person does not have Parkinson's/Brain disease"
                                       st.success(parkinsons_diagnosis)


#-----------------------------------------------------------------------------------------------------------
lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bsPjV4.json")
lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_P2uXE5.json")

st.write("------")
footer="""<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color:#5486ea ;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed and Built By 赵多多Takudzwa Gershom Choto <a style='display: block; text-align: center;' href="https://github.com/TakudzwaChoto" target="_blank">人工智能研究@遵义师范学院 </a></p>
</div>

"""
st.markdown(footer,unsafe_allow_html=True)
          
                   