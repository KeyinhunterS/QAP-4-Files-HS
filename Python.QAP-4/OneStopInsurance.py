# Description: This program is for the One Stop Insurance company to enter can calculate new insurance policy information for its customers.
# Author: Hunter Saunders
# Date(s): 2024-07-20/2024-07-25

# Define required libraries.
import datetime
import FormateValues as FV
import sys
import time

# Define program constants.
NEXT_POLICY_NUMBER = 1944
BASIC_PREMIUM = 869.00
DISCOUNT_PER_CAR = 0.25
COST_EXTRA_LIABILITY = 130.00
COST_GLASS_COVERAGE = 86.00
COST_LOANER_CAR = 58.00
HST_RATE = 0.15
PROCESSING_FEE = 39.99

# List of valid provinces for validation
VALID_PROVINCES = ['ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL']

f = open("Insurance.dat","r")

def ProgressBar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    # Generate and display a progress bar with % complete at the end.
 
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

for InsurRecord in f:

# Function to calculate premium for multiple cars
 def calculate_total_premium(num_cars):
    total_premium = BASIC_PREMIUM + (num_cars - 1) * (BASIC_PREMIUM * (1 - DISCOUNT_PER_CAR))
    return total_premium

# Function to calculate extra costs based on options
def calculate_extra_costs(num_cars, extra_liability, glass_coverage, loaner_car):
    extra_cost = 0
    if extra_liability == 'Y':
        extra_cost += num_cars * COST_EXTRA_LIABILITY
    if glass_coverage == 'Y':
        extra_cost += num_cars * COST_GLASS_COVERAGE
    if loaner_car == 'Y':
        extra_cost += num_cars * COST_LOANER_CAR
    return extra_cost

# Function to calculate total cost including HST
def calculate_total_cost(premium, extra_cost):
    total_premium = premium + extra_cost
    hst = total_premium * HST_RATE
    total_cost = total_premium + hst
    return total_cost

# Function to calculate monthly payment details
def calculate_monthly_payment(total_cost, payment_method, down_payment=None):
    if payment_method == 'Full':
        monthly_payment = total_cost / 8
        down_payment_amount = 0
    elif payment_method == 'Monthly':
        monthly_payment = (total_cost + PROCESSING_FEE) / 8
        down_payment_amount = 0
    elif payment_method == 'Down Pay':
        down_payment_amount = down_payment
        monthly_payment = (total_cost - down_payment_amount + PROCESSING_FEE) / 8
    
    return monthly_payment, down_payment_amount

# Function to display claims
def display_claims(claims):
    print("\nPrevious Claims:")
    print("Claim #   Claim Date   Amount")
    print("---------------------------------")
    for claim in claims:
        print("{:<9} {:<12} {}".format(claim['claim_number'], claim['claim_date'].strftime('%Y-%m-%d'), FV(claim['claim_amount'])))

# Function to input customer data
def input_customer_data():
    first_name = input("Enter customer's first name: ").strip().title()
    last_name = input("Enter customer's last name: ").strip().title()
    address = input("Enter customer's address: ").strip()
    city = input("Enter customer's city: ").strip().title()
    province = input("Enter customer's province (2-letter code): ").strip().upper()
    while province not in VALID_PROVINCES:
        province = input("Invalid province code. Please enter a valid 2-letter province code: ").strip().upper()
    postal_code = input("Enter customer's postal code: ").strip().upper()
    phone_number = input("Enter customer's phone number: ").strip()

    num_cars = int(input("Enter number of cars being insured: "))
    extra_liability = input("Extra liability coverage (Y/N): ").strip().upper()
    glass_coverage = input("Glass coverage (Y/N): ").strip().upper()
    loaner_car = input("Loaner car coverage (Y/N): ").strip().upper()

    payment_method = input("Payment method (Full/Monthly/Down Pay): ").strip().title()
    if payment_method == 'Down Pay':
        down_payment = float(input("Enter the down payment amount: "))
    else:
        down_payment = None

    return {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'province': province,
        'postal_code': postal_code,
        'phone_number': phone_number,
        'num_cars': num_cars,
        'extra_liability': extra_liability,
        'glass_coverage': glass_coverage,
        'loaner_car': loaner_car,
        'payment_method': payment_method,
        'down_payment': down_payment
    }

# Function to input claims data
def input_claims():
    claims = []
    while True:
        claim_number = input("Enter claim number (or type 'done' to finish): ").strip()
        if claim_number.lower() == 'done':
            break
        claim_date = datetime.datetime.strptime(input("Enter claim date (YYYY-MM-DD): "), '%Y-%m-%d')
        claim_amount = float(input("Enter claim amount: "))
        claims.append({
            'claim_number': claim_number,
            'claim_date': claim_date,
            'claim_amount': claim_amount
        })
    return claims

# Main program execution
def main():
    # Input customer data
    customer_data = input_customer_data()

    # Input claims data
    claims_data = input_claims()

    # Calculate premium and extra costs
    premium = calculate_total_premium(customer_data['num_cars'])
    extra_cost = calculate_extra_costs(customer_data['num_cars'],
                                       customer_data['extra_liability'],
                                       customer_data['glass_coverage'],
                                       customer_data['loaner_car'])

    # Calculate total cost including HST
    total_cost = calculate_total_cost(premium, extra_cost)

    # Calculate monthly payment details
    monthly_payment, down_payment = calculate_monthly_payment(total_cost,
                                                              customer_data['payment_method'],
                                                              customer_data['down_payment'])
    print()
 
    TotalIterations = 30 # The more iterations, the more time is takes.
    Message = "Saving Data ..."
 
    for i in range(TotalIterations + 1):
        time.sleep(0.1)  # Simulate some work
        ProgressBar(i, TotalIterations, prefix=Message, suffix='Complete', length=50)
 
    print()
 
 
    print()
    print("information has been successfully saved to Insurance.dat...")
    print()

    # Display receipt
    print("\n--- Insurance Policy Receipt ---")
    print("Customer Name: {} {}".format(customer_data['first_name'], customer_data['last_name']))
    print("Address: {}, {}, {} {}".format(customer_data['address'], customer_data['city'], customer_data['province'], customer_data['postal_code']))
    print("Phone Number: {}".format(customer_data['phone_number']))
    print("Number of Cars Insured: {}".format(customer_data['num_cars']))
    print("Extra Liability Coverage: {}".format(customer_data['extra_liability']))
    print("Glass Coverage: {}".format(customer_data['glass_coverage']))
    print("Loaner Car Coverage: {}".format(customer_data['loaner_car']))
    print("Payment Method: {}".format(customer_data['payment_method']))
    if down_payment:
        print("Down Payment: {}".format(FV(down_payment)))
    print("\nInsurance Premium (Pre-tax): {}".format(FV(premium)))
    print("Extra Costs: {}".format(FV(extra_cost)))
    print("Total Cost (Including HST): {}".format(FV(total_cost)))
    print("\nMonthly Payment: {}".format(FV(monthly_payment)))
    print()

    # Display claims
    display_claims(claims_data)
    # Update next policy number
    global NEXT_POLICY_NUMBER
    NEXT_POLICY_NUMBER += 1
    
f.close()

