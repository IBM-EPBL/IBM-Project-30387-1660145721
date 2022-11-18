from flask import Flask,render_template,request,jsonify
import pickle
import flask
from flask import request, render_template
from flask_cors import CORS
import requests
import Parser


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "jkAhUKPLY7AtlKYFkyOhX0MAD3gBP5NPuWH1c5lsCASQ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": 'jkAhUKPLY7AtlKYFkyOhX0MAD3gBP5NPuWH1c5lsCASQ', "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)

# User Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predictPage():
    return render_template('predict.html',result = "Provide URL for Prediction")

@app.route('/about')
def aboutPage():
    return render_template('about.html')

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def y_predict():
    url = request.form["URL"]
    print("Given url : ",url)
    X = Parser.main(url)# X = [[-1,-1,-1,1,-1,1,1,1,1,1,1,-1,-1,1,0,-1,-1,-1,0,1,1,1,1,1,1,1,1,1,1,-1]]
    # y = np.array(X)
    # NOTEd: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['having_IPhaving_IP_Address','URLURL_Length','Shortining_Service','having_At_Symbol','double_slash_redirecting','Prefix_Suffix','having_Sub_Domain','SSLfinal_State','Domain_registeration_length','Favicon','port','HTTPS_token','Request_URL','URL_of_Anchor','Links_in_tags','SFH','Submitting_to_email','Abnormal_URL','Redirect','on_mouseover','RightClick','popUpWidnow','Iframe','age_of_domain','DNSRecord','web_traffic','Page_Rank','Google_Index','Links_pointing_to_page','Statistical_report']], "values": X }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/416e4500-9b96-4a40-bb86-894472582f4c/predictions?version=2022-11-16', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print(predict)

    print("Final prediction :",predict)
    if(predict == -1):
        return render_template('sitepred.html', result="You are Safe :) Given URL is Not a Phishing Website")
    else:
        return render_template('sitepred.html', result="Be Safe ⚠ Given URL is a Phishing Website")

    # showing the prediction results in a UI# showing the prediction results in a UI
    # return render_template('predict.html', result = "Posted")


if __name__ == '__main__' :
    app.run(debug= True)











# print(response_scoring)
#     predictions = response_scoring.json()
#     predict = predictions['predictions'][0]['values'][0][0]
#     print("Final prediction :",predict)
    
    # showing the prediction results in a UI# showing the prediction results in a UI
    # return render_template('predict.html', predict=predict)






# Redirected to the Prediction Page to check the URL
# @app.route('/predict')
# def predict():
    # return render_template('Predict.html')

# Page with the Predicted Results
# @app.route('/resultPrediction',methods=['POST'])
# def res_pred():
    # url = request.from['URL']
    # checkPrediction = inputScript.main(url)
    # Prediction = model.predict(checkPrediction)
    # print(Prediction)
    # output = Prediction[0]
    
    # -1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,-1,0,1,1,1,1,-1,-1,-1,-1,1,1,-1