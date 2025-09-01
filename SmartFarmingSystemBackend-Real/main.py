from fastapi import FastAPI
from pydantic import BaseModel , Field
import pickle
import numpy as np
import os

########################
#Load the model
########################  
   
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR , "xgbModel.pkl")
SCALER_PATH = os.path.join(BASE_DIR , "scaler.pkl")


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)
    
    
########################
#Define Input Schema
########################


class InputData(BaseModel):
    
    soilCO2concentrationMean: float = Field(..., ge=0, le=10, description="Average soil CO₂ concentration (ppm), typically 0–10")
    soilTempMean: float = Field(..., ge=-10, le=50, description="Average soil temperature in °C, typically -10–50")
    VSWCMean: float = Field(..., ge=0, le=1, description="Volumetric soil water content, ratio between 0–1")
    VSICMean: float = Field(..., ge=0, le=1, description="Volumetric soil inorganic carbon, ratio between 0–1")
    windSpeedMean: float = Field(..., ge=0, le=50, description="Average wind speed in m/s, typically 0–50")
    RHMean: float = Field(..., ge=0, le=100, description="Relative humidity (%), between 0–100")
    tempRHMean: float = Field(..., ge=-20, le=50, description="Average air temperature (°C), typically -20–50")
    dewTempMean: float = Field(..., ge=-20, le=30, description="Dew point temperature (°C), typically -20–30")

    # Minimum values
    soilCO2concentrationMinimum: float = Field(..., ge=0, le=10, description="Minimum soil CO₂ concentration (ppm)")
    soilTempMinimum: float = Field(..., ge=-10, le=50, description="Minimum soil temperature (°C)")
    VSWCMinimum: float = Field(..., ge=0, le=1, description="Minimum soil water content")
    VSICMinimum: float = Field(..., ge=0, le=1, description="Minimum soil inorganic carbon")
    windSpeedMinimum: float = Field(..., ge=0, le=50, description="Minimum wind speed (m/s)")
    RHMinimum: float = Field(..., ge=0, le=100, description="Minimum relative humidity (%)")
    tempRHMinimum: float = Field(..., ge=-20, le=50, description="Minimum air temperature (°C)")
    dewTempMinimum: float = Field(..., ge=-20, le=30, description="Minimum dew temperature (°C)")

    # Maximum values
    soilCO2concentrationMaximum: float = Field(..., ge=0, le=10, description="Maximum soil CO₂ concentration (ppm)")
    soilTempMaximum: float = Field(..., ge=-10, le=50, description="Maximum soil temperature (°C)")
    VSWCMaximum: float = Field(..., ge=0, le=1, description="Maximum soil water content")
    VSICMaximum: float = Field(..., ge=0, le=1, description="Maximum soil inorganic carbon")
    windSpeedMaximum: float = Field(..., ge=0, le=50, description="Maximum wind speed (m/s)")
    RHMaximum: float = Field(..., ge=0, le=100, description="Maximum relative humidity (%)")
    tempRHMaximum: float = Field(..., ge=-20, le=50, description="Maximum air temperature (°C)")
    dewTempMaximum: float = Field(..., ge=-20, le=30, description="Maximum dew temperature (°C)")

    # Derived / engineered features
    wind_sin: float = Field(..., ge=-1, le=1, description="Sine transform of wind direction, -1 to 1")
    wind_cos: float = Field(..., ge=-1, le=1, description="Cosine transform of wind direction, -1 to 1")
    TFPrecip_flag: int = Field(..., ge=0, le=1, description="Precipitation flag, 0 or 1")
    VPD: float = Field(..., ge=0, le=5, description="Vapor pressure deficit (kPa), typically 0–5")

    # Lag features
    soilTempMean_lag1h: float = Field(..., ge=-10, le=50, description="Soil temperature (°C) lagged by 1 hour")
    soilTempMean_lag2h: float = Field(..., ge=-10, le=50, description="Soil temperature (°C) lagged by 2 hours")
    VSWCMean_lag1h: float = Field(..., ge=0, le=1, description="Soil water content lagged by 1 hour")
    VSWCMean_lag2h: float = Field(..., ge=0, le=1, description="Soil water content lagged by 2 hours")
    soilCO2concentrationMean_lag1h: float = Field(..., ge=0, le=10, description="Soil CO₂ concentration lagged by 1 hour")
    soilCO2concentrationMean_lag2h: float = Field(..., ge=0, le=10, description="Soil CO₂ concentration lagged by 2 hours")
    VPD_lag1h: float = Field(..., ge=0, le=5, description="Vapor pressure deficit (kPa) lagged by 1 hour")
    VPD_lag2h: float = Field(..., ge=0, le=5, description="Vapor pressure deficit (kPa) lagged by 2 hours")


###########################################
#Initialize FastApi
###########################################

app = FastAPI(
    title="Smart Farming System FastAPI", version = "1.0"
)



############################################
#Health Check EndPoint
############################################

@app.get("/")
def home():
    return {"message" : "API is running. Go to /docs for Swagger UI"}
    
    
    

############################################
#Prediction EndPoint
############################################

@app.post("/predict")
def predict(data: InputData):
    try:
        # Convert input into the correct order
        features = np.array([[
            data.soilCO2concentrationMean,
            data.soilTempMean,
            data.VSWCMean,
            data.VSICMean,
            data.windSpeedMean,
            data.RHMean,
            data.tempRHMean,
            data.dewTempMean,
            data.soilCO2concentrationMinimum,
            data.soilTempMinimum,
            data.VSWCMinimum,
            data.VSICMinimum,
            data.windSpeedMinimum,
            data.RHMinimum,
            data.tempRHMinimum,
            data.dewTempMinimum,
            data.soilCO2concentrationMaximum,
            data.soilTempMaximum,
            data.VSWCMaximum,
            data.VSICMaximum,
            data.windSpeedMaximum,
            data.RHMaximum,
            data.tempRHMaximum,
            data.dewTempMaximum,
            data.wind_sin,
            data.wind_cos,
            data.TFPrecip_flag,
            data.VPD,
            data.soilTempMean_lag1h,
            data.soilTempMean_lag2h,
            data.VSWCMean_lag1h,
            data.VSWCMean_lag2h,
            data.soilCO2concentrationMean_lag1h,
            data.soilCO2concentrationMean_lag2h,
            data.VPD_lag1h,
            data.VPD_lag2h
        ]])

        # Apply scaling
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)

        # If classifier with proba
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features_scaled).tolist()
            return {"prediction": int(prediction[0]), "probabilities": probabilities}

        return {"prediction": int(prediction[0])}

    except Exception as e:
        return {"error": str(e)}   
    
