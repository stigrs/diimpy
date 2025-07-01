# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

from openpyxl import load_workbook

def analyze_influence(model, sheet_name="Analyze_influence"):
    """Analyze dependencies and influence gains."""
    #
    # Output is written to existing datafile (xslx).
    #
    wb = load_workbook(model.config["datafile"])
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)

    header = ["function", "delta", "delta_overall", "rho", "rho_overall"]
    ws.append(header)

    delta = model.dependency()
    delta_overall = model.overall_dependency()
    rho = model.influence()
    rho_overall = model.overall_influence()

    for f, d, do, r, ro in zip(model.infra, delta, delta_overall, rho, rho_overall):
        ws.append([f, d, do, r, ro])

    wb.save(filename=model.config["datafile"])

def analyze_interdependency(model, sheet_name="Analyze_interdependency"):
    """Analyze first-, second- and third-order interdependencies."""
    #
    # Output is written to existing datafile (xslx).
    #
    wb = load_workbook(model.config["datafile"])
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)

    header = ["i", "j", "max(aij)", "i", "j", "max(aij^2)", "i", "j", "max(aij^3)"]
    ws.append(header)

    first = model.max_nth_order_interdependency(1)
    second = model.max_nth_order_interdependency(2)
    third = model.max_nth_order_interdependency(3)

    for i in range(len(model)):
        row = [
            first[i][0],
            first[i][1],
            first[i][2],
            second[i][0],
            second[i][1],
            second[i][2],
            third[i][0],
            third[i][1],
            third[i][2],
        ]
        ws.append(row)

    wb.save(filename=model.config["datafile"])
