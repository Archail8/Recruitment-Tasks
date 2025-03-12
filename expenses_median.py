"""
Calculate median of expenses till first Sunday (included) of each month.
(ex. for 2023-09 and 2023-10 those days are 1, 2, 3 Sep and 1 Dec).

Solution should be split into two functions:

solution1 → Unoptimised solution (draft)

solution2 → Optimised solution using one of the below methods:

priority queues
quick select
quick sort

Solution should match the below pseudocode:

expenses = {
    "2023-01": {
        "01": {
            "food": [ 22.11, 43, 11.72, 2.2, 36.29, 2.5, 19 ],
            "fuel": [ 210.22 ]
        },
        "09": {
            "food": [ 11.9 ],
            "fuel": [ 190.22 ]
        }
    },
    "2023-03": {
        "07": {
            "food": [ 20, 11.9, 30.20, 11.9 ]
        },
        "04": {
            "food": [ 10.20, 11.50, 2.5 ],
            "fuel": []
        }
    },
    "2023-04": {}
};

func solution1(expenses) {
    result = null;
    // ...
    return result;
}
func solution2(expenses) {
    result = null;
    // ...
    return result;
}
"""

import datetime
import random

# Remarks:
# - Returning null for improper input data is commonly perceived bad practice (as null will break something down
#   the pipeline, masking the actual issue). Throwing an exception would be much better.
# - Test data provided does not cover enough edge cases to define proper handing of, for example,
#   different date formats.
# - I am fully aware that quicksort in solution2 can have complexity of O(n^2) in cae of unlucky pivots. I am also
#   aware of existence of pivot choosing algorythm. Yet requirements did not mention anything about it, as well as
#   did not prohibit usage of statistics.median(), so ....

expenses = {
    "2023-01": {
        "01": {
            "food": [22.11, 43, 11.72, 2.2, 36.29, 2.5, 19],
            "fuel": [210.22]
        },
        "09": {
            "food": [11.9],
            "fuel": [190.22]
        }
    },
    "2023-03": {
        "07": {
            "food": [20, 11.9, 30.20, 11.9]
        },
        "04": {
            "food": [10.20, 11.50, 2.5],
            "fuel": []
        }
    },
    "2023-04": {}
}


def solution1(expenses: dict) -> float:
    """Find median, complexity : O(n log n)"""
    result = None
    if is_input_data_valid(expenses):
        expenses_sorted = sorted(simplify_input_data(expenses))
        if len(expenses_sorted) % 2 == 1:
            result = expenses_sorted[len(expenses_sorted) // 2]
        else:
            result = (expenses_sorted[int(len(expenses_sorted) / 2) - 1] +
                      expenses_sorted[int(len(expenses_sorted) / 2)]) / 2

    return result


def solution2(expenses: dict) -> float:
    """Find median via quickselect, average complexity : O(n). Quickselect appears to be a consensual recommendation
    among researched sources and as such has been chosen,"""
    result = None
    if is_input_data_valid(expenses):
        result = quickselect_median(simplify_input_data(expenses))

    return result


def is_input_data_valid(expenses: dict) -> bool:
    """Check data for basic malformations, like invalid date or non-numeric expense."""
    is_valid = False
    try:
        for year_month, expenses_per_day in expenses.items():
            next_month = datetime.datetime(*[int(a) for a in year_month.split('-')], 28) - datetime.timedelta(days=4)
            last_day = next_month - datetime.timedelta(days=next_month.day)
            for day, expense_categories in expenses_per_day.items():
                if int(day) > last_day.day:
                    return False
                else:
                    for value in expense_categories.values():
                        if not all(isinstance(e, (int, float)) for e in value):
                            return False

        is_valid = True
    except:
        pass

    return is_valid


def simplify_input_data(expenses: dict) -> list:
    """Concatenate all expenses recorded up to (including) first Sunday of the month into single list."""
    simplified_input_data = list()
    for year_month, expenses_per_day in expenses.items():
        first_sunday = get_first_sunday(year_month)
        for day, expense_categories in expenses_per_day.items():
            if int(day) <= first_sunday:
                for value in expense_categories.values():
                    simplified_input_data.extend(value)

    return simplified_input_data


def quickselect_median(l: list, pivot_fn=random.choice) -> float:
    if len(l) % 2 == 1:
        return quickselect(l, len(l) // 2, pivot_fn)
    else:
        return 0.5 * (quickselect(l, int(len(l) / 2) - 1, pivot_fn) +
                      quickselect(l, int(len(l) / 2), pivot_fn))


def get_first_sunday(year_month: str) -> int:
    first_sunday = 1 + (6 - datetime.datetime(*[int(a) for a in year_month.split('-')], 1).weekday())

    return first_sunday


def quickselect(l: list, k: int, pivot_fn) -> float:
    """
    Select the kth element in l (0 based)
    :param l: List of numerics
    :param k: Index
    :param pivot_fn: Function to choose a pivot, defaults to random.choice
    :return: The kth element of l
    """
    if len(l) == 1:
        assert k == 0
        return l[0]

    pivot = pivot_fn(l)

    lows = [el for el in l if el < pivot]
    highs = [el for el in l if el > pivot]
    pivots = [el for el in l if el == pivot]

    if k < len(lows):
        return quickselect(lows, k, pivot_fn)
    elif k < len(lows) + len(pivots):
        return pivots[0]
    else:
        return quickselect(highs, k - len(lows) - len(pivots), pivot_fn)


if __name__ == "__main__":
    print(solution1(expenses))
    print(solution2(expenses))
