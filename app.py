from flask import Flask, request, render_template
import pandas as pd
from decimal import Decimal, getcontext
import math

app = Flask(__name__)

# Set the precision for Decimal operations
getcontext().prec = 28

# Load CSV file into a DataFrame with Decimal type for numbers
csv_file = "ivf_success_formulas.csv"

def decimal_converter(value):
    """
    Converts the given value to Decimal type if possible.
    
    Input: 
        - value (str): The value to convert.
        
    Output: 
        - Decimal: The converted value if valid, else returns the original value.
    """
    try:
        return Decimal(value)
    except:
        return value

df = pd.read_csv(csv_file, converters={
    col: decimal_converter for col in pd.read_csv(csv_file, nrows=0).columns
})

def calculate_bmi(weight, height_feet, height_inches):
    """
    Calculates the BMI using weight and height in feet and inches.

    Input:
        - weight (int or float): The weight of the individual in pounds.
        - height_feet (int): The height in feet.
        - height_inches (int): The height in inches.
    
    Output:
        - Decimal: The calculated BMI value rounded to the appropriate precision.
    """
    total_height_inches = (Decimal(height_feet) * 12) + Decimal(height_inches)
    bmi = (Decimal(weight) / (total_height_inches ** 2)) * 703
    return bmi

def select_formula(egg_source, ivf_cycles, infertility_known):
    """
    Selects the appropriate formula from the CSV data based on the input values.
    
    Input:
        - egg_source (str): The source of the eggs ('donor_eggs' or 'own_eggs').
        - ivf_cycles (str): Whether IVF cycles were previously attempted ('TRUE' or 'FALSE').
        - infertility_known (str): Whether infertility is known ('TRUE' or 'FALSE').

    Output:
        - DataFrame row: The matching formula row from the DataFrame.

    Raises:
        - ValueError: If no matching formula is found.
    """
    if egg_source == "donor_eggs":
        filtered_df = df[
            (df['param_using_own_eggs'] == 'FALSE') &
            (df['param_attempted_ivf_previously'] == 'N/A') &
            (df['param_is_reason_for_infertility_known'] == infertility_known)
        ]
    elif egg_source == "own_eggs":
        filtered_df = df[
            (df['param_using_own_eggs'] == 'TRUE') &
            (df['param_attempted_ivf_previously'] == ivf_cycles) &
            (df['param_is_reason_for_infertility_known'] == infertility_known)
        ]

    if filtered_df.empty:
        raise ValueError("No matching formula found. Please check the input values and CSV data.")
    return filtered_df.iloc[0]

def calculate_success_rate(inputs, formula_row):
    """
    Calculates the IVF success rate based on various factors including age, BMI, and infertility reasons.
    
    Input:
        - inputs (dict): A dictionary containing the user's input values, including:
            - age (int): The age of the individual.
            - bmi (Decimal): The BMI value.
            - prior_pregnancies (str): The number of prior pregnancies ('0', '1', etc.).
            - prior_births (str): The number of prior live births ('0', '1', etc.).
            - reasons (dict): A dictionary indicating whether certain infertility reasons apply (e.g., 'tubal_factor': True/False).
        - formula_row (Series): A row from the DataFrame containing the formula for the calculation.

    Output:
        - Decimal: The calculated IVF success rate in percentage.
    """
    age = Decimal(inputs['age'])
    bmi = Decimal(inputs['bmi'])

    age_component = (
        Decimal(formula_row['formula_age_linear_coefficient']) * age
        + Decimal(formula_row['formula_age_power_coefficient']) * (age ** Decimal(formula_row['formula_age_power_factor']))
    )

    bmi_component = (
        Decimal(formula_row['formula_bmi_linear_coefficient']) * bmi
        + Decimal(formula_row['formula_bmi_power_coefficient']) * (bmi ** Decimal(formula_row['formula_bmi_power_factor']))
    )

    infertility_components = sum([
        Decimal(formula_row[f'formula_{reason}_true_value']) if inputs[reason] else Decimal(0)
        for reason in ['tubal_factor', 'male_factor_infertility', 'endometriosis',
                       'ovulatory_disorder', 'diminished_ovarian_reserve', 'uterine_factor',
                       'other', 'unexplained_infertility']
    ])

    prior_pregnancies = inputs['prior_pregnancies']
    prior_pregnancies = prior_pregnancies.strip()
    pregnancies_component = Decimal(formula_row[f'formula_prior_pregnancies_{prior_pregnancies}_value'])

    prior_births = inputs['prior_births']
    prior_births = prior_births.strip()
    births_component = Decimal(formula_row[f'formula_prior_live_births_{prior_births}_value'])

    score = (
        Decimal(formula_row['formula_intercept']) +
        age_component + bmi_component + infertility_components +
        pregnancies_component + births_component
    )

    success_rate = Decimal(math.exp(float(score))) / (1 + Decimal(math.exp(float(score))))
    return round(success_rate * 100, 2)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Processes the form data, calculates the BMI, selects the appropriate formula,
    and calculates the IVF success rate.
    
    Input:
        - form data (from the user input via POST request).
        
    Output:
        - Rendered HTML ('result.html') with the success rate.
    """
    data = request.form
    age = int(data['age'])
    weight = int(data['weight'])
    height_feet = int(data['height_feet'])
    height_inches = int(data['height_inches'])
    egg_source = data['egg_source']
    ivf_cycles = int(data['ivf_cycles'])
    if ivf_cycles == 0:
        ivf_cycles = 'FALSE'
    else:
        ivf_cycles = 'TRUE'

    # Check if any infertility reason except 'no_reason' is selected
    infertility_known = 'TRUE' if any([
        data.get('reason') != 'no_reason'  # This excludes 'I don’t know/no reason'
    ]) else 'FALSE'

    reasons = ['tubal_factor', 'male_factor_infertility', 'endometriosis',
               'ovulatory_disorder', 'diminished_ovarian_reserve', 'uterine_factor',
               'other', 'unexplained_infertility']

    # Mapping the selected reasons to a dictionary
    reason_map = {reason: reason in data.getlist('reason') for reason in reasons}
    bmi = calculate_bmi(weight, height_feet, height_inches)
    
    inputs = {
        "age": age,
        "bmi": bmi,
        "prior_pregnancies": data['prior_pregnancies'],
        "prior_births": data['prior_births'],
        **reason_map
    }

    # Select the formula based on user input
    formula_row = select_formula(egg_source, ivf_cycles, infertility_known)
    # Calculate success rate
    success_rate = calculate_success_rate(inputs, formula_row)

    return render_template('result.html', success_rate=success_rate)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)