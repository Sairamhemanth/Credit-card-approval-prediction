from flask import Flask, render_template, request
import pandas as pd
import joblib

# ============================================================
# Flask App Initialization
# ============================================================

app = Flask(__name__)

# ============================================================
# Load Trained Model and Preprocessing Objects
# ============================================================

model = joblib.load("Models/card_model.joblib")
label_encoders = joblib.load("Models/label_encoders.pkl")
scaler = joblib.load("Models/scaler.pkl")
feature_names = joblib.load("Models/feature_names.pkl")


# ============================================================
# Home Page
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# Banking Eligibility Rules
# ============================================================

def check_business_rules(form):

    reasons = []

    recommendation = ""

    age = float(form["AGE"])

    income = float(form["AMT_INCOME_TOTAL"])

    years = float(form["YEARS_EMPLOYED"])

    children = int(form["CNT_CHILDREN"])

    family = float(form["CNT_FAM_MEMBERS"])

    income_type = form["NAME_INCOME_TYPE"]


    # --------------------------------------------------------
    # Rule 1
    # --------------------------------------------------------

    if age < 18:

        reasons.append("Applicant must be at least 18 years old.")

    # --------------------------------------------------------
    # Rule 2
    # --------------------------------------------------------

    if income < 120000:

        reasons.append(
            "Annual income is below the minimum requirement (₹1,20,000)."
        )

    # --------------------------------------------------------
    # Rule 3
    # --------------------------------------------------------

    if years < 1:

        reasons.append(
            "At least one year of employment is required."
        )

    # --------------------------------------------------------
    # Rule 4
    # --------------------------------------------------------

    if children > 3 and income < 200000:

        reasons.append(
            "Income is low compared to the number of children."
        )

    # --------------------------------------------------------
    # Rule 5
    # --------------------------------------------------------

    if family > 7 and income < 300000:

        reasons.append(
            "Large family size with insufficient income."
        )

    # --------------------------------------------------------
    # Rule 6
    # --------------------------------------------------------

    income_per_member = income / family

# Minimum recommended income per family member: ₹30,000/year
    if income_per_member < 30000:

        reasons.append(
            "Income per family member is below the recommended level (₹30,000 per year)."
        )

    # --------------------------------------------------------
    # Rule 7
    # --------------------------------------------------------

    if income_type == "Student" and income < 150000:

        reasons.append(
            "Student applicants require a higher annual income."
        )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if len(reasons) > 0:

        recommendation = (
            "Improve the above financial conditions before "
            "reapplying for a credit card."
        )

        return False, reasons, recommendation

    else:

        reasons.append(
            "Applicant satisfies all banking eligibility rules."
        )

        recommendation = (
            "Proceed to Machine Learning evaluation."
        )

        return True, reasons, recommendation
    # ============================================================
# Prediction
# ============================================================

#@app.route("/predict", methods=["POST"])
@app.route("/prediction")
def prediction():
    return render_template("prediction.html")
@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # Read Form Inputs
        # ----------------------------------------------------

        age = float(request.form["AGE"])
        years_employed = float(request.form["YEARS_EMPLOYED"])

        data = {

            "CODE_GENDER": request.form["CODE_GENDER"],

            "FLAG_OWN_CAR": request.form["FLAG_OWN_CAR"],

            "FLAG_OWN_REALTY": request.form["FLAG_OWN_REALTY"],

            "CNT_CHILDREN": int(request.form["CNT_CHILDREN"]),

            "AMT_INCOME_TOTAL": float(request.form["AMT_INCOME_TOTAL"]),

            "NAME_INCOME_TYPE": request.form["NAME_INCOME_TYPE"],

            "NAME_EDUCATION_TYPE": request.form["NAME_EDUCATION_TYPE"],

            "NAME_FAMILY_STATUS": request.form["NAME_FAMILY_STATUS"],

            "NAME_HOUSING_TYPE": request.form["NAME_HOUSING_TYPE"],

            "DAYS_BIRTH": -(age * 365),

            "DAYS_EMPLOYED": -(years_employed * 365),

            "FLAG_MOBIL": int(request.form["FLAG_MOBIL"]),

            "FLAG_WORK_PHONE": int(request.form["FLAG_WORK_PHONE"]),

            "FLAG_PHONE": int(request.form["FLAG_PHONE"]),

            "FLAG_EMAIL": int(request.form["FLAG_EMAIL"]),

            "OCCUPATION_TYPE": request.form["OCCUPATION_TYPE"],

            "CNT_FAM_MEMBERS": float(request.form["CNT_FAM_MEMBERS"])

        }

        # ----------------------------------------------------
        # Business Rule Checking
        # ----------------------------------------------------

        eligible, reasons, recommendation = check_business_rules(request.form)
        if not eligible:

            failed_rules = len(reasons)

            if failed_rules == 1:
                confidence = 60

            elif failed_rules == 2:
                confidence = 68

            elif failed_rules == 3:
                confidence = 75

            elif failed_rules == 4:
                confidence = 82

            else:
                confidence = 90

            return render_template(

                "result.html",

                prediction="Credit Card Not Approved ❌",

                confidence=confidence,

                reasons=reasons,

                recommendation=recommendation

            )

        
             

        # ----------------------------------------------------
        # Convert to DataFrame
        # ----------------------------------------------------

        input_df = pd.DataFrame([data])

        # ----------------------------------------------------
        # Encode Categorical Columns
        # ----------------------------------------------------

        for column, encoder in label_encoders.items():

            value = input_df.loc[0, column]

            if value not in encoder.classes_:

                return render_template(

                    "result.html",

                    prediction=f"Invalid value for {column}",

                    confidence=0,

                    reasons=["Unexpected input value received."],

                    recommendation="Please submit the form again."

                )

            input_df[column] = encoder.transform(input_df[column])

        # ----------------------------------------------------
        # Arrange Features
        # ----------------------------------------------------

        input_df = input_df[feature_names]

        # ----------------------------------------------------
        # Scale Features
        # ----------------------------------------------------

        input_scaled = scaler.transform(input_df)
                # ----------------------------------------------------
        # Machine Learning Prediction
        # ----------------------------------------------------

        prediction = model.predict(input_scaled)[0]

        probabilities = model.predict_proba(input_scaled)[0]

        approval_probability = float(probabilities[1])

        rejection_probability = float(probabilities[0])
        

        # ----------------------------------------------------
        # Generate Decision
        # ----------------------------------------------------

        ml_reasons = []

        if prediction == 1:

            result = "Credit Card Approved ✅"

            confidence = round(min(max(approval_probability * 100, 80), 99), 2)
            ml_reasons.append("Applicant passed all eligibility rules.")

            if years_employed >= 5:
                ml_reasons.append("Stable employment history.")

            elif years_employed >= 2:
                ml_reasons.append("Good employment stability.")

            else:
                ml_reasons.append("Employment requirement satisfied.")

            if data["AMT_INCOME_TOTAL"] >= 500000:
                ml_reasons.append("Excellent annual income.")

            elif data["AMT_INCOME_TOTAL"] >= 300000:
                ml_reasons.append("Good annual income.")

            else:
                ml_reasons.append("Income satisfies minimum requirement.")

            if data["CNT_CHILDREN"] == 0:
                ml_reasons.append("No financial dependency from children.")

            elif data["CNT_CHILDREN"] <= 2:
                ml_reasons.append("Family responsibilities are manageable.")

            ml_reasons.append(
                "Machine Learning model predicts low credit risk."
            )

            recommendation = (
                "Applicant can proceed for document verification "
                "and further banking procedures."
            )

        else:

            result = "Credit Card Not Approved ❌"

            confidence = round(min(max(rejection_probability * 100, 50), 75), 2)

            if years_employed < 2:
                ml_reasons.append(
                    "Employment history is relatively short."
                )

            if data["AMT_INCOME_TOTAL"] < 250000:
                ml_reasons.append(
                    "Annual income is comparatively low."
                )

            if data["CNT_CHILDREN"] >= 3:
                ml_reasons.append(
                    "Higher financial responsibility due to children."
                )

            if data["CNT_FAM_MEMBERS"] >= 6:
                ml_reasons.append(
                    "Large family size increases financial burden."
                )

            ml_reasons.append(
                "Machine Learning model predicts higher credit risk."
            )

            recommendation = (
                "Improve employment stability and financial profile "
                "before applying again."
            )

        # ----------------------------------------------------
        # Render Result
        # ----------------------------------------------------

        return render_template(

            "result.html",

            prediction=result,

            confidence=confidence,

            reasons=ml_reasons,

            recommendation=recommendation

        )

    # --------------------------------------------------------
    # Exception Handling
    # --------------------------------------------------------

    except ValueError:

        return render_template(

            "result.html",

            prediction="Invalid numeric input.",

            confidence=0,

            reasons=[
                "One or more numeric fields contain invalid values."
            ],

            recommendation="Please verify the entered values."

        )

    except Exception as e:

        return render_template(

            "result.html",

            prediction="System Error",

            confidence=0,

            reasons=[
                str(e)
            ],

            recommendation="Please contact the administrator."

        )


# ============================================================
# Run Flask Application
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
