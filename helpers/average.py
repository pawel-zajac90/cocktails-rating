def average(sum_of_ratings, ratings):
    try:
        avg = sum_of_ratings / len(ratings)
    except ZeroDivisionError:
        avg = 0
    return avg