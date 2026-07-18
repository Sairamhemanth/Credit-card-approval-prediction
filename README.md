# Credit Card Approval Prediction

## Overview
This project is a Machine Learning web application that predicts whether a credit card application is likely to be approved based on user-provided information. The application uses a trained ML model with business rule validation and provides detailed reasoning for approval or rejection decisions.

## Features
- Predicts credit card approval status
- User-friendly web interface
- Machine Learning-based prediction
- Business rule validation
- Responsive dashboard
- Input validation
- Detailed approval/rejection reasons
- Fast prediction results
- Confidence scores

## Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **ML Libraries:** Scikit-learn, Pandas, NumPy
- **Model Serialization:** Joblib
- **Deployment:** Gunicorn

## Project Structure

```
credit-card-approval-prediction/
│
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment config
├── README.md                       # Project documentation
├── Models/                         # Pre-trained ML models
│   ├── card_model.joblib         # Trained classifier model
│   ├── label_encoders.pkl        # Categorical encoders
│   ├── scaler.pkl                # Feature scaler
│   └── feature_names.pkl         # Feature names
├── Dataset/                        # Training dataset
├── templates/                      # HTML templates
│   ├── index.html                # Home page
│   ├── prediction.html           # Prediction form
│   └── result.html               # Results page
├── static/                         # CSS and JavaScript
│   ├── style.css                 # Styling
│   └── script.js                 # Frontend logic
└── credit-card-documentation/     # Project documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Sairamhemanth/credit-card-approval-prediction.git
cd credit-card-approval-prediction
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## How to Use

1. **Open the Application:** Launch the Flask server and navigate to the home page
2. **Fill the Form:** Enter the required applicant details including:
   - Personal Information (Age, Gender, Family Status)
   - Financial Information (Income, Employment Years)
   - Asset Information (Car, Realty ownership)
   - Contact Details (Phone, Email, Work Phone)
3. **Submit:** Click the "Predict" button
4. **View Results:** The application will display:
   - Approval/Rejection status
   - Confidence score
   - Reasons for the decision
   - Recommendations for improvement (if rejected)

## Machine Learning Model

The credit card approval prediction model:
- Uses supervised learning classification
- Incorporates business rule validation
- Applies feature scaling and encoding
- Provides probability scores
- Generates explainable predictions

### Model Pipeline
1. **Input Validation:** Business rules check
2. **Feature Engineering:** Transform input features
3. **Encoding:** Convert categorical variables
4. **Scaling:** Normalize numerical features
5. **Prediction:** ML model inference
6. **Decision Making:** Generate approval/rejection with reasons

## Prediction Factors

The model considers:
- **Age:** Minimum 18 years required
- **Income:** Minimum annual income threshold
- **Employment:** Minimum 1 year employment required
- **Family:** Income-to-family-member ratio
- **Dependents:** Number of children and family members
- **Assets:** Car and realty ownership status
- **Contact:** Mobile and work phone verification

## Future Improvements

- User authentication and account management
- Database integration for application history
- Explainable AI (SHAP/LIME) for model transparency
- Cloud deployment (AWS, Google Cloud, Heroku)
- Model performance improvements and retraining
- API endpoints for third-party integration
- Advanced analytics and reporting dashboard
- Multi-language support

## Deployment

### Local Deployment
```bash
python app.py
```

### Heroku Deployment
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Docker Deployment
```bash
docker build -t credit-card-app .
docker run -p 5000:5000 credit-card-app
```

## API Documentation

### Routes

- **GET `/`** - Home page
- **GET `/prediction`** - Prediction form page
- **POST `/predict`** - Submit prediction request

### Request Format (POST /predict)
```json
{
  "AGE": 35,
  "CODE_GENDER": "M",
  "FLAG_OWN_CAR": "Y",
  "FLAG_OWN_REALTY": "Y",
  "CNT_CHILDREN": 2,
  "AMT_INCOME_TOTAL": 300000,
  "NAME_INCOME_TYPE": "Employed",
  "NAME_EDUCATION_TYPE": "Secondary",
  "NAME_FAMILY_STATUS": "Married",
  "NAME_HOUSING_TYPE": "House/Apartment",
  "YEARS_EMPLOYED": 5,
  "FLAG_MOBIL": 1,
  "FLAG_WORK_PHONE": 0,
  "FLAG_PHONE": 1,
  "FLAG_EMAIL": 1,
  "OCCUPATION_TYPE": "Managers",
  "CNT_FAM_MEMBERS": 4
}
```

## Troubleshooting

### Model Not Found Error
- Ensure the `Models/` directory contains all required `.joblib` and `.pkl` files
- Download pre-trained models if missing

### Port Already in Use
```bash
# Use a different port
python app.py --port 5001
```

### Template Not Found
- Verify `templates/` directory exists
- Check template file names match the render_template() calls

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=.
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Author

**Sairamhemanth**
- GitHub: [@Sairamhemanth](https://github.com/Sairamhemanth)

## Acknowledgments

- Original concept and implementation by Arsheen Khanam
- UCI Machine Learning Repository for dataset inspiration
- Flask and scikit-learn communities

## Support

For issues, questions, or suggestions, please:
- Open a GitHub issue
- Contact the author
- Check the documentation folder

---

**Last Updated:** July 2026
