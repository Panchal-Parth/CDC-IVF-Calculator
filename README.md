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
