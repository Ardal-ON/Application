# Automotive Predictive Maintenance Application

A machine learning-powered application for monitoring and predicting car conditions with a user-friendly GUI interface.

## Features

- **Machine Learning Models**: Trains and evaluates multiple ML algorithms to predict engine conditions
- **Interactive GUI**: Modern Flet-based interface for real-time monitoring
- **Maintenance Predictions**: Intelligent recommendations for component maintenance

## Project Structure

```
application/
├── app.py                    # Main GUI application entry point
├── assets/                   # Static assets
│   └── Car.png               # Car image for GUI
├── data/                     # Dataset storage
│   └── engine_data.csv       # Engine health dataset
├── gui/                      # GUI application components
│   ├── __init__.py           # Package initialization
│   ├── Dashboard.py          # Dashboard with monitoring charts
│   ├── Home.py               # Home page interface
│   ├── Maintenance.py        # Maintenance recommendations page
│   └── Model.py              # ML model interface and predictions
├── models/                   # Trained ML models
│   ├── best_model.pkl        # Best performing model
│   ├── model_metadata.json   # Model information
│   └── scaler.pkl            # Feature scaler
├── train_model.py            # ML training pipeline
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
├── uv.lock                   # UV dependency lock file
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd application
   ```

2. **Set up Python environment**
   ```bash
   # Using uv (recommended)
   uv venv
   uv pip install -r requirements.txt
   
   # Or using pip
   python -m venv venv
   pip install -r requirements.txt
   ```

## Usage

### Training the Model

Before using the GUI application, you need to train the machine learning model:

```bash
uv run train_model.py
# or
python train_model.py
```

This will:
- Load and preprocess the engine data
- Train multiple ML algorithms (Logistic Regression, Decision Tree, Random Forest, etc.)
- Evaluate and compare model performances
- Save the best performing model to `models/best_model.pkl`

### Running the GUI Application

After training the model, launch the graphical interface:

```bash
uv run app.py
# or
python app.py
```

This opens the Car Condition Monitor application with three main sections:

#### 🏠 **Home Page**
- Parameter value inputs and controls

#### 📊 **Dashboard**
- Performance metrics overview

#### 🔧 **Maintenance**
- Maintenance recommendations
- Suggested maintenance schedules

## Model Details

The application trains and evaluates the following machine learning models:

| Model | Description |
|-------|-------------|
| **Logistic Regression** | Linear classification with probability outputs |
| **Decision Tree** | Tree-based decisions with max depth = 6 |
| **Random Forest** | Ensemble of trees with max depth = 10 |
| **K-Neighbors** | Distance-based classification |
| **Gaussian Naive Bayes** | Probabilistic classifier (often best performer) |
| **SVM** | Support Vector Machine with balanced class weights |

## Dataset

The dataset used for model training and evaluation is available on [Kaggle: Automotive Vehicles Engine Health Dataset](https://www.kaggle.com/datasets/parvmodi/automotive-vehicles-engine-health-dataset/data).

### Input Features

The model uses the following engine parameters:

- **Engine RPM**: Revolutions per minute
- **Lub Oil Pressure**: Lubrication oil pressure
- **Fuel Pressure**: Fuel system pressure 
- **Coolant Pressure**: Cooling system pressure 
- **Lub Oil Temperature**: Oil temperature 
- **Coolant Temperature**: Coolant temperature

### Output

- **Engine Condition**: Binary classification (0 = Needs Maintenance, 1 = Good Condition)