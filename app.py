# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:52:43 2021

@author: karan
"""
from flask import Flask,render_template,request
import numpy as np
import pandas as pd 
import pickle
import jsonify
import requests

app=Flask(__name__)
model=pickle.load(open("model.pkl","rb"))

@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    if request.method=='POST':
        Year=float(request.form["Year"])
        present_price=float(request.form["Showroom Price"])
        kms_driven=int(request.form["Killometers Drived"])
        owner=int(request.form["owner"])
        fuel_type_petrol=request.form['Fuel Type']
        if fuel_type_petrol=='Petrol':
            fuel_type_petrol=1
            fuel_type_diesel=0
        elif fuel_type_petrol=='Diesel':
            fuel_type_petrol=0
            fuel_type_diesel=1
        else:
            fuel_type_petrol=0
            fuel_type_diesel=0
        seller_type=request.form['Seller Type']
        if seller_type=='Individual':
            seller_type=1
        else:
            seller_type=0
        
        transmission_type=request.form['Transmission']
        if transmission_type=='Manual':
            transmission_type=1
        else:
            transmission_type=0
        data=np.array([[Year,present_price,kms_driven,owner,fuel_type_diesel,
                    fuel_type_petrol,seller_type,transmission_type]])
        price=model.predict(data)[0]

        if price<0:
            return render_template("index.html",
            prediction_text="You can not sell this car")
        else:
            return render_template("index.html",
            prediction_text=f"You can sell this car for {round(price,2)} lakh")
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run()