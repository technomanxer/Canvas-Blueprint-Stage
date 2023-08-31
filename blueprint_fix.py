import csv

fix_write = []
with open('sis_export.csv', 'r') as sis_export:
    csv_read = csv.DictReader(sis_export)
    fix_write=[x for x in csv_read if 'IC635X0000' in x['short_name']  or 'IC635X0800' in x['short_name']]

#     #math 4 fix
#     read_r = [x for x in csv_read]
#     fix_codes = ["20042Z0900",
# "20042Z090C",
# "20042Z090F",
# "20042Z090G",
# "20042Z090J",
# "20042Z090S",
# "2004AZ0900"]
#     for f in fix_codes:
#         fix_c = [x for x in read_r if f in x['short_name'] and '591288' in x['blueprint_course_id']]
#         fix_write.extend(fix_c)

#     # cte fix

#     read_r = [x for x in csv_read]
#     fix_codes = ['CY032Y0000',
#                  'CY032Y0400']
#     for f in fix_codes:
#         fix_c = [x for x in read_r if f in x['short_name']
#                  and '590430' in x['blueprint_course_id']]
#         fix_write.extend(fix_c)


for x in fix_write:
    x['blueprint_course_id'] = 'dissociate'

with open('fix_blueprint.csv', 'w', newline="") as sis_fix:
    csv_write = csv.DictWriter(sis_fix, fieldnames=fix_write[0].keys())
    csv_write.writeheader()
    csv_write.writerows(fix_write)
