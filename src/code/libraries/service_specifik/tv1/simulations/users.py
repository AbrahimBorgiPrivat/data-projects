import random
from typing import List, Dict
from faker import Faker
from libraries.packages.upsert_data import upsert_insert, build_client

fake = Faker("da_DK")

REGION_DISTRIBUTION = {
    "Hovedstaden": 0.31,
    "Sjælland": 0.14,
    "Syddanmark": 0.22,
    "Midtjylland": 0.23,
    "Nordjylland": 0.10
}

HOUSEHOLD_SIZE_DISTRIBUTION = {
    1: 0.38,
    2: 0.33,
    3: 0.12,
    4: 0.10,
    5: 0.05,
    6: 0.02
}

CHILD_UNDER5_PROBABILITY = {
    1: 0.00,  # single household
    2: 0.15,
    3: 0.45,
    4: 0.60,
    5: 0.65,
    6: 0.70
}

AGE_GROUPS = ["18-25", "26-40", "41-60", "60+"]
AGE_GROUP_PROB = [0.10, 0.40, 0.35, 0.15]

def pick_region() -> str:
    r = random.random()
    cumulative = 0
    for region, prob in REGION_DISTRIBUTION.items():
        cumulative += prob
        if r <= cumulative:
            return region
    return random.choice(list(REGION_DISTRIBUTION.keys()))

def pick_household_size() -> int:
    r = random.random()
    cumulative = 0
    for size, prob in HOUSEHOLD_SIZE_DISTRIBUTION.items():
        cumulative += prob
        if r <= cumulative:
            return size
    return 2

def has_child_under5(household_size: int) -> bool:
    return random.random() < CHILD_UNDER5_PROBABILITY[household_size]

def pick_age_group() -> str:
    return random.choices(AGE_GROUPS, weights=AGE_GROUP_PROB, k=1)[0]

def assign_segment_id(age_group: str, household_size: int) -> int:
    if household_size >= 5:
        return 7 
    elif age_group in ["18-25"]:
        return 6  
    elif age_group in ["26-40"] and household_size >= 3:
        return 1  
    elif age_group in ["41-60"] and household_size >= 3:
        return 2 
    elif age_group == "60+":
        return 4 
    elif household_size == 1 and age_group in ["26-40", "41-60"]:
        return 5 
    elif age_group in ["26-40"] and household_size <= 3:
        return 8  
    elif age_group in ["26-40"] and household_size == 2:
        return 3 
    else:
        return 5 

def generate_danish_households(upsert_runtime_vars: dict) -> List[Dict[str, str]]:
    client = build_client(
        db_name=upsert_runtime_vars['client']['db_name'],
        username=upsert_runtime_vars['client']['username'],
        password=upsert_runtime_vars['client']['password'],
        server=upsert_runtime_vars['client']['server'],
        port=upsert_runtime_vars['client']['port'],
        db_type=upsert_runtime_vars['client']['db_type']
    )
    n = upsert_runtime_vars.get("number_of_simulations", 1000)
    if upsert_runtime_vars.get("seed") is not None:
        random.seed(upsert_runtime_vars["seed"])
    results: List[Dict[str, str]] = []
    user_id = 1
    while len(results) < n:
        region = pick_region()
        household_size = pick_household_size()
        if not has_child_under5(household_size):
            continue
        age_group = pick_age_group()
        segment_id = assign_segment_id(age_group, household_size)
        results.append({
            "user_id": user_id,
            "age_group": age_group,
            "household_size": household_size,
            "region": region,
            "children_under5": True,
            "segment_id": segment_id
        })
        user_id += 1
    upsert_insert(client=client,
            upsert_runtime_vars=upsert_runtime_vars,
            new_data=results
        )
    return results


