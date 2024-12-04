# IVF Success Rate Calculator

This Flask application calculates the success rate of IVF (In Vitro Fertilization) based on various factors such as age, BMI, infertility reasons, and previous IVF cycles. The application uses a CSV file (`ivf_success_formulas.csv`) that contains formulas for calculating the success rate based on user input.

## Features

- **BMI Calculation**: Calculates BMI from the user's weight and height.
- **Formula Selection**: Selects an appropriate formula based on egg source, IVF cycles, and known infertility reasons.
- **IVF Success Rate Calculation**: Calculates the success rate using the selected formula and user inputs.

## Requirements

- Python 3.x
- Flask
- Pandas
- Decimal
- math

## Installation

### 1. Clone the repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/Panchal-Parth/CDC-IVF-Calculator.git
```

### 2. Install Dependencies
```
pip3 install Flask
pip3 install pandas
```

### 3. Set Up CSV File
Ensure you have the ivf_success_formulas.csv file in the root directory of your project. This file contains the formulas used for the calculation.

### 4. Run the Flask Application
Run the Flask app using the following command:
```
python3 app.py
```
By default, the app will run on http://0.0.0.0:8080

### 5. Access the Application
Open your browser and go to http://localhost:8080 to access the IVF success rate calculator.

## Usage
### Input Fields
Age: Enter the age of the person undergoing IVF.
Weight: Enter the weight of the person (in pounds).
Height: Enter the height in feet and inches.
Egg Source: Select whether the egg source is "Donor Eggs" or "Own Eggs".
IVF Cycles: Enter the number of IVF cycles attempted previously.
Infertility Reason(s): Select one or more reasons for infertility, or choose "I don’t know/no reason".
Prior Pregnancies: Enter the number of prior pregnancies.
Prior Live Births: Enter the number of prior live births.

### Output
After submitting the form, the application will display the calculated IVF success rate based on the entered data.
