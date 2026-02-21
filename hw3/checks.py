#!/usr/bin/env python3
import csv
import sys
from math import sqrt

MISSING = "?"

def mean(xs):
    return sum(xs) / len(xs) if xs else 0

def sd(xs):
    if not xs:
        return 0
    mu = mean(xs)
    return sqrt(sum((x - mu) ** 2 for x in xs) / len(xs))

def pearson(xs, ys):
    if not xs or not ys:
        return 0
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs)
    dy = sum((y - my) ** 2 for y in ys)
    if dx == 0 or dy == 0:
        return 0
    return num / sqrt(dx * dy)

def load_rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def numeric_columns(rows):
    cols = rows[0].keys()
    return [c for c in cols if c != "class!"]

def to_float_column(rows, col):
    xs = []
    for r in rows:
        if r[col] != MISSING:
            xs.append(float(r[col]))
    return xs

def print_feature_results(features):
    print(len(features))
    for f in sorted(features):
        print(f)

def print_case_results(rows):
    print(len(rows))
    for r in sorted(rows):
        print(r)

# ----------------------------------------------------------------------
# A – Identical features
# ----------------------------------------------------------------------

def check_A(path):
    rows = load_rows(path)
    cols = numeric_columns(rows)

    # TODO: group columns with identical values across all rows
    identical = set()

    print_feature_results(identical)

# ----------------------------------------------------------------------
# B – Correlated features
# ----------------------------------------------------------------------

def check_B(path):
    rows = load_rows(path)
    cols = numeric_columns(rows)

    # TODO: compute Pearson correlations for all column pairs
    correlated = set()

    print_feature_results(correlated)

# ----------------------------------------------------------------------
# C – Outlier features
# ----------------------------------------------------------------------

def check_C(path):
    rows = load_rows(path)
    cols = numeric_columns(rows)

    # TODO: detect features with ≥1 extreme value
    outlier_cols = set()

    print_feature_results(outlier_cols)

# ----------------------------------------------------------------------
# D – Features with conflicting values
# ----------------------------------------------------------------------

def check_D(path):
    rows = load_rows(path)

    # TODO: detect columns involved in violated derived constraints
    bad_features = set()

    print_feature_results(bad_features)

# ----------------------------------------------------------------------
# E – Features with implausible values
# ----------------------------------------------------------------------

def check_E(path):
    rows = load_rows(path)

    # TODO: detect columns with ≥1 implausible value
    bad_features = set()

    print_feature_results(bad_features)

# ----------------------------------------------------------------------
# G – Outlier cases
# ----------------------------------------------------------------------

def check_G(path):
    rows = load_rows(path)
    stds = {}
    means = {}

    for col in rows[0]:
        vals = []
        for row in rows:
            if row[col] != '?' and col != "class!":
                vals.append(float(row[col]))
        stds[col] = sd(vals)
        means[col] = mean(vals)

    bad_rows = set()

    for i, row in enumerate(rows):
        for col in means:
            val = row[col]
            if val == MISSING or col == "class!":
                continue
            if stds[col] == 0:
                continue

            if abs(float(val) - means[col]) > 3 * stds[col]:
                bad_rows.add(i+2)
                break

    print_case_results(bad_rows)

# ----------------------------------------------------------------------
# H – Inconsistent cases
# ----------------------------------------------------------------------

def check_H(path):
    rows = load_rows(path)
    
    row_features = {}

    for row in rows:
        key = (
            row["HEIGHT"], row["LENGHT"], row["WIDTH"], row["AREA"], row["ECCEN"],
            row["P_BLACK"], row["P_AND"], row["MEAN_TR"], row["BLACKPIX"],
            row["BLACKAND"], row["WB_TRANS"], row["DATASET_ID"]
        )
        try:
            row_features[key].append(row["class!"])
        except:
            row_features[key] = [row["class!"]]

    bad_rows = set()
    for i, row in enumerate(rows):
        key = (
            row["HEIGHT"], row["LENGHT"], row["WIDTH"], row["AREA"], row["ECCEN"],
            row["P_BLACK"], row["P_AND"], row["MEAN_TR"], row["BLACKPIX"],
            row["BLACKAND"], row["WB_TRANS"], row["DATASET_ID"]
        )

        if len(row_features[key]) > 1:
            bad_rows.add(i+2)

    print_case_results(bad_rows)

# ----------------------------------------------------------------------
# I – Class-conditional outlier cases
# ----------------------------------------------------------------------

def check_I(path):
    rows = load_rows(path)
    
    classes = set(row["class!"] for row in rows)

    stds = {}
    means = {}

    for col in rows[0]:
        if col == "class!":
            continue
    
        means[col] = {}
        stds[col] = {}

        for cls in classes:
            vals = []
            for row in rows:
                if row["class!"] == cls and row[col] != MISSING:
                    vals.append(float(row[col]))

            if len(vals) > 0:
                means[col][cls] = mean(vals)
                stds[col][cls] = sd(vals)
            else:
                means[col][cls] = 0
                stds[col][cls] = 0

    bad_rows = set()

    for i, row in enumerate(rows):
        cls = row["class!"]

        for col in means:
            val = row[col]

            if val == MISSING:
                continue

            if stds[col][cls] == 0:
                continue

            if abs(float(val) - means[col][cls]) > 3 * stds[col][cls]:
                bad_rows.add(i + 2)  # +2 for header + 1-based indexing
                break

    print_case_results(bad_rows)

# ----------------------------------------------------------------------
# J – Cases with conflicting feature values
# ----------------------------------------------------------------------

def check_J(path):
    rows = load_rows(path)

    bad_rows = []
    for i, r in enumerate(rows):
        needed = ['HEIGHT','LENGHT','AREA','ECCEN',
                  'P_BLACK','P_AND','BLACKPIX','BLACKAND']
        if any(r[c] == MISSING for c in needed):
            continue

        h   = float(r['HEIGHT']);  l  = float(r['LENGHT'])
        a   = float(r['AREA']);    e  = float(r['ECCEN'])
        pb  = float(r['P_BLACK']); pa = float(r['P_AND'])
        bpx = float(r['BLACKPIX']); ba = float(r['BLACKAND'])

        if (a != h * l
            or (h > 0 and abs(e - l/h) > 0.01)
            or (a > 0 and abs(pb - bpx/a) > 0.001)
            or (a > 0 and abs(pa - ba/a)  > 0.001)):
            bad_rows.append(i + 2)

    print(len(bad_rows))
    for r in bad_rows:
        print(r)

# ----------------------------------------------------------------------
# K – Cases with implausible values
# ----------------------------------------------------------------------

def check_K(path):
    rows = load_rows(path)

    bad_rows = set()

    for i, row in enumerate(rows):

        if MISSING in row.values():
            bad_rows.add(i + 2)
            continue

        height   = float(row["HEIGHT"])
        length   = float(row["LENGHT"])
        width    = float(row["WIDTH"])
        area     = float(row["AREA"])
        blackpix = float(row["BLACKPIX"])
        blackand = float(row["BLACKAND"])
        wb_trans = float(row["WB_TRANS"])
        mean_tr  = float(row["MEAN_TR"])
        eccen    = float(row["ECCEN"])
        p_black  = float(row["P_BLACK"])
        p_and    = float(row["P_AND"])
        cls      = int(row["class!"])
    
        if any(v <= 0 for v in [
            height, length, width, area,
            blackpix, blackand, wb_trans,
            mean_tr, eccen
        ]):
            bad_rows.add(i + 2)
            continue

        if not (1 <= cls <= 5):
            bad_rows.add(i + 2)
            continue

        if blackpix > blackand:
            bad_rows.add(i + 2)
            continue

        if not (0 <= p_black <= 1) or not (0 <= p_and <= 1):
            bad_rows.add(i + 2)
            continue
    
    print_case_results(bad_rows)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 checks.py <A–M> <data.csv>")

    target = sys.argv[1]
    path   = sys.argv[2]

    dispatch = {
        "A": check_A,
        "B": check_B,
        "C": check_C,
        "D": check_D,
        "E": check_E,
        "G": check_G,
        "H": check_H,
        "I": check_I,
        "J": check_J,
        "K": check_K,
    }

    if target not in dispatch:
        sys.exit(f"Unknown target: {target}")

    dispatch[target](path)
