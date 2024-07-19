def calculate_bmr(gender, weight, height, age):
    if gender == 'nam':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_tdee(bmr, intensity):
    activity_factors = {
        'ít vận động': 1.2,
        'vận động nhẹ': 1.375,
        'vận động vừa': 1.55,
        'vận động nặng': 1.725,
        'vận động rất nặng': 1.9
    }
    return bmr * activity_factors[intensity]

def calculate_calories(tdee, goal):
    if goal == 'giảm cân':
        return tdee - 500
    elif goal == 'tăng cân':
        return tdee + 500
    return tdee