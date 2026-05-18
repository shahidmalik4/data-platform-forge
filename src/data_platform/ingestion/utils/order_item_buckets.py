import random

def realistic_num_items():
    buckets = [
        (9, 27),  # 50% probability
        (29, 43),  # 30% probability
        (47, 69)   # 20% probability
    ]
    weights = [0.5, 0.3, 0.2]

    # pick a bucket based on weights
    selected_bucket = random.choices(buckets, weights=weights, k=1)[0]

    # pick a random number within that bucket
    return random.randint(selected_bucket[0], selected_bucket[1])