# CarDekho---Car-Price-Prediction

## Overview
This project implements a machine learning-based car price prediction system that helps users estimate the price of used cars based on various features. The system uses a Random Forest model trained on comprehensive car listing data from multiple cities in India.

## Key Features
- Data processing and cleaning pipeline for car listing data
- Advanced feature engineering and selection
- Random Forest model with optimized hyperparameters
- Interactive Streamlit web interface
- Support for multiple cities and car specifications
- Real-time price predictions

## Technical Stack
- Python 3.10.9
- pandas
- scikit-learn
- PyCaret
- Streamlit
- Seaborn/Matplotlib for visualization

## Project Structure
```
├── dataset/               # Raw Excel files with car data
├── car_dheko_app/        
│   ├── model/            # Trained models and encoders
│   │   ├── model.pkl     # Trained Random Forest model
│   │   ├── label_encoders.pkl
│   │   └── *.txt        # Feature value mappings
│   └── app.py           # Streamlit application
├── car_dheko.ipynb      # Main notebook with model development
└── fulldata.csv         # Processed dataset
```

## Features Used for Prediction
1. Transmission Type
2. Model Year
3. Gear Box
4. City
5. Insurance Validity
6. Number of Owners
7. Kilometers Driven
8. Body Type
9. Mileage
10. Fuel Type

## Model Performance
- The system uses a Random Forest Regressor optimized through GridSearchCV
- Features strong R² score on test data
- Handles various car specifications and conditions

## Installation & Setup
1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:
```bash
cd car_dheko_app
streamlit run app.py
```

## Data Preprocessing
- Handles missing values and outliers
- Converts price formats (Lakh/Crore to absolute values)
- Normalizes numerical features
- Encodes categorical variables
- Removes irrelevant features

## Model Development Process
1. Data cleaning and standardization
2. Feature selection based on correlation and importance
3. Model comparison using PyCaret
4. Hyperparameter optimization using GridSearchCV
5. Final model evaluation and deployment

## Usage
1. Launch the Streamlit application
2. Input car specifications:
   - Select transmission type
   - Enter model year
   - Choose gear box type
   - Select city
   - Provide insurance validity
   - Enter other specifications
3. Get instant price prediction in Lakhs

## Future Improvements
- Integration with real-time market data
- Support for more cities and regions
- Enhanced feature engineering
- Model retraining pipeline
- UI/UX improvements

## Contributors
- [s kaarthikk vishwa]
