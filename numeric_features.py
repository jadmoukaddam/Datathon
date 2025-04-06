import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple


def calculate_effective_experience(jobs: List[Tuple[int, int]]) -> int:
    """
    Calculates effective work experience in years, avoiding double-counting overlapping years.

    Args:
        jobs: List of (start_year, end_year) tuples. None as end_year means the job is current.

    Returns:
        Total number of unique working years across all jobs.
    """
    worked_years = set()
    for start, end in jobs:
        if start is None:
            continue
        end = end if end is not None else 2025
        worked_years.update(range(start, end))
    return len(worked_years)


def extract_numeric_features(full_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Extracts numeric features from a list of client dictionaries.

    Args:
        full_data: List of dictionaries, each representing a client with nested data.

    Returns:
        A pandas DataFrame containing engineered numeric features.
    """

    # total AUM
    aum_vec = [np.sum(list(client['client_profile']['aum'].values())) for client in full_data]

    # total property value
    property_value_vec = [client['client_profile']['aum']['real_estate_value'] for client in full_data]
    #number of propertis owned
    property_count_vec = [len(client['client_profile']['real_estate_details']) for client in full_data]

    # total value inherited
    inheritance_vec = [client['client_profile']['aum']['inheritance'] for client in full_data]

    # client's savings
    savings_vec = [client['client_profile']['aum']['savings'] for client in full_data]

    # how many different jobs did the client have
    job_count_vec = [len(client['client_profile']['employment_history']) for client in full_data]

    # Compute property-to-cash ratio with zero-division handling
    property_to_cash_vec = [
        prop_value / (total_value - prop_value) if (total_value - prop_value) != 0 else -float('inf')
        for prop_value, total_value in zip(property_value_vec, aum_vec)
    ]
    max_ratio = np.max(property_to_cash_vec)
    property_to_cash_vec = [max_ratio if value == -float("inf") else value for value in property_to_cash_vec]

    # Inheritance / (inheritance + savings), safe against zero-division
    inheritance_to_cash_vec = [
        inheritance / (inheritance + saving) if (inheritance + saving) != 0 else 0
        for inheritance, saving in zip(inheritance_vec, savings_vec)
    ]

    # Salary & experience metrics
    current_salary_vec = []
    max_salary_vec = []
    total_work_experience_vec = []
    effective_work_experience_vec = []

    for client in full_data:
        emp_hist = client['client_profile']['employment_history']
        salary = 0
        max_salary = 0

        if len(emp_hist) == 0:
            total_work_experience = 0
            effective_work_experience = 0
        
        else:
            year_history = []
            min_start = np.inf
            max_end = -np.inf
            for job in emp_hist:
                if max_salary < job['salary']:
                    max_salary = job['salary']

                start, end = job['start_year'], job['end_year']
                year_history.append((start, end))

                if end is None:
                    salary += job['salary']
                    end = 2025

                if start < min_start:
                    min_start = start
                if end > max_end:
                    max_end = end

            total_work_experience = max_end-min_start
            effective_work_experience = calculate_effective_experience(year_history)

        total_work_experience_vec.append(total_work_experience)
        effective_work_experience_vec.append(effective_work_experience)
        current_salary_vec.append(salary)
        max_salary_vec.append(max_salary)

    # Savings per active work year
    saving_per_annum_vec = [
        saving / work_exp if work_exp != 0 else saving
        for saving, work_exp in zip(savings_vec, effective_work_experience_vec)
    ]

    # Current salary compared to max salary seen in career
    salary_to_max_salary_vec = [
        salary / max_salary if max_salary != 0 else 0
        for salary, max_salary in zip(current_salary_vec, max_salary_vec)
    ]

    # Construct final DataFrame
    df_numeric = pd.DataFrame({
        'aum': aum_vec,
        'property_value': property_value_vec,
        'num_properties': property_count_vec,
        'inheritance_value': inheritance_vec,
        'savings_value': savings_vec,
        'num_jobs': job_count_vec,
        'current_salary': current_salary_vec,
        'max_salary': max_salary_vec,
        'property_to_cash_ratio': property_to_cash_vec,
        'inheritance_to_cash_ratio': inheritance_to_cash_vec,
        'total_work_experience': total_work_experience_vec,
        'effective_work_experience': effective_work_experience_vec,
        'saving_per_annum': saving_per_annum_vec,
        'salary_to_max_salary_ratio': salary_to_max_salary_vec
    })

    return df_numeric
