def attendance_predictor(attended, total, check_percentage):
    count = 0
    while True:
        if attended / total * 100 >= check_percentage:
            break
        count += 1
        attended += 1
        total += 1
    return count


def bunk_predictor(attended, total, check_percentage):
    count = 0
    while True:
        total += 1
        if attended / total * 100 <= check_percentage:
            break
        count += 1
    return count

