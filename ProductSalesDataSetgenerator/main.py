import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime

# To set display of 100 rows for easier checking of Data Frame
pd.set_option('display.max_columns', None)


# Initialize Faker and set seeds for reproducibility
fake = Faker('en_PH')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Constants
RECORD_COUNT = 11350
YEARS = [2020, 2021, 2022, 2023, 2024]
PROVINCES_CITIES = {
    'Metro Manila': ['Makati', 'Taguig', 'Pasig', 'Manila', 'Quezon City'],
    'Cavite': ['Bacoor', 'Dasmariñas', 'Imus'],
    'Laguna': ['Calamba', 'San Pedro', 'Santa Rosa'],
    'Batangas': ['Batangas City', 'Lipa', 'Tanauan'],
    'Rizal': ['Antipolo', 'Taytay', 'Cainta'],
    'Bulacan': ['Malolos', 'Meycauayan', 'San Jose del Monte'],
    'Pangasinan': ['Dagupan', 'Urdaneta', 'Mangaldan', 'San Fabian', 'San Carlos']
}

BRANDS_SEGMENTS = {
    'Nike': {'Men': 0.4, 'Women': 0.4, 'Kids': 0.2},
    'Adidas': {'Men': 0.5, 'Women': 0.3, 'Kids': 0.2},
    'Puma': {'Men': 0.3, 'Women': 0.5, 'Kids': 0.2},
    'Uniqlo': {'Men': 0.2, 'Women': 0.5, 'Kids': 0.3},
    'H&M': {'Men': 0.5, 'Women': 0.4, 'Kids': 0.1},
    'Lee': {'Men': 0.4, 'Women': 0.4, 'Kids': 0.2},
    'Gap': {'Men': 0.3, 'Women': 0.5, 'Kids': 0.2}

}

SEGMENT_CATEGORIES = {
    'Men': ['Shirts', 'T-Shirts', 'Polos', 'Outwear', 'Jeans', 'Hoodies & Sweatshirts', 'Pants', 'Shorts',
            'Underwear & Lounge wear'],
    'Women': ['Tops', 'Dresses', 'Shorts', 'Skirts', 'Pants', 'Leggings', 'Jeans', 'Jacket & Coats',
              'Lingerie & Lounge wear'],
    'Kids': ['Tops', 'Shirts', 'Polos', 'Hoodies & Sweatshirts', 'Jacket & Coats', 'Dresses', 'Pants', 'Leggings',
             'Jeans', 'Shorts', 'Sleepwear', 'Underwear'],
}

RATINGS = {
    'Poor': 0.03,
    'Unsatisfactory': 0.06,
    'Satisfactory': 0.17,
    'Very Satisfactory': 0.39,
    'Outstanding': 0.35
}


# Custom probability functions
def generate_transaction_id():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))


def generate_transaction_date():
    years = [2020, 2021, 2022, 2023, 2024]
    probabilities = [0.1, 0.15, 0.18, 0.35, 0.22]
    chosen_year = np.random.choice(years, p=probabilities)

    # Today's date
    today = datetime.today()
    if chosen_year == today.year:
        start_date = pd.to_datetime(f'{chosen_year}-01-01')
        end_date = pd.to_datetime(today)
    else:
        start_date = pd.to_datetime(f'{chosen_year}-01-01')
        end_date = pd.to_datetime((f'{chosen_year}-12-31'))

    random_days = np.random.randint(0, (end_date-start_date).days + 1)
    random_date = start_date + pd.Timedelta(days= random_days)
    return random_date.date()


def random_gender():
    return random.choices(['Female', 'Male'], weights=[0.68, 0.32])[0]


def random_age():
    age_ranges = [(18, 25), (26, 33), (34, 41), (42, 50)]
    age_prob = [0.33, 0.42, 0.18, 0.07]
    select_range = np.random.choice(len(age_ranges), p=age_prob)
    return np.random.randint(age_ranges[select_range][0], age_ranges[select_range][1] + 1)


def generate_price(SEGMENT_CATEGORY):
    if BRANDS_SEGMENTS in ['Shirts', 'T-Shirts', 'Polos', 'Tops', 'Dresses', 'Pants']:
        return random.randint(2000, 3000)
    elif BRANDS_SEGMENTS in ['Outwear', 'Jeans', 'Hoodies & Sweatshirts', 'Jacket & Coats', 'Leggings', 'Jeans', 'Skirts']:
        return random.randint(1500, 3000)
    else:
        return random.randint(900, 1500)


def random_qty():
    qty_range = [(1, 3), (4, 7), (8, 10)]
    qty_prob = [0.68, 0.16, 0.16]
    select_range = np.random.choice(len(qty_range), p=qty_prob)
    return np.random.randint(qty_range[select_range][0], qty_range[select_range][1] + 1)

def generate_return(rating):
    if rating in ['Poor', 'Unsatisfactory']:
        # Probability of 66% of return
        return np.random.choice(['Yes', 'No'], p=[0.66, 0.34])
    else:
        return 'No'


# Generate Data Set
data = []
for _ in range(RECORD_COUNT):
    transaction_id = generate_transaction_id()
    transaction_date = generate_transaction_date()
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random_gender()
    age = random_age()
    province = random.choice(list(PROVINCES_CITIES.keys()))
    city = random.choice(PROVINCES_CITIES[province])
    brand = random.choice(list(BRANDS_SEGMENTS.keys()))
    segment = np.random.choice(list(BRANDS_SEGMENTS[brand].keys()), p=list(BRANDS_SEGMENTS[brand].values()))
    category = random.choice(SEGMENT_CATEGORIES[segment])
    price = generate_price(segment)
    qty_purchase = random_qty()
    product_amount = price * qty_purchase
    rating = np.random.choice(list(RATINGS.keys()), p=list(RATINGS.values()))
    did_return = generate_return(rating)


    row = {
        'Transaction ID': transaction_id,
        'Transaction Date': transaction_date,
        'Customer First Name': first_name,
        'Customer Last Name': last_name,
        'Gender': gender,
        'Age': age,
        'Province': province,
        'City': city,
        'Brand': brand,
        'Segment': segment,
        'Brand Category': category,
        'Price': price,
        'Qty Item': qty_purchase,
        'Total Amount': product_amount,
        'Rating': rating,
        'Returned': did_return
    }

    data.append(row)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('product_sales_data.csv', index=False)

print("Dataset generated and saved as 'product_sales_data.csv'.")
print(df)
