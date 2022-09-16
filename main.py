
from numpy.core.numeric import NaN
import gams
import pandas as pd
from tools import *
import os

BASE_DIR = os.path.abspath('')
ws = gams.workspace.GamsWorkspace(working_directory= BASE_DIR)
db = ws.add_database()

df_hours = pd.read_excel('data_proj2.xlsx', sheet_name='hours')
df_time_conflict = pd.read_excel('data_proj2.xlsx', sheet_name='time_conflict')
df_lecturer = pd.read_excel('data_proj2.xlsx', sheet_name='lecturer')
df_course_info = pd.read_excel('data_proj2.xlsx', sheet_name='course_info')
df_possible_time = pd.read_excel('data_proj2.xlsx', sheet_name='possible_time')
df_course_conflict = pd.read_excel('data_proj2.xlsx', sheet_name='course_conflict')

# initial sets
c_python = initial_set(df_course_info, "course")
c = db.add_set("c", 1)
for info in c_python:
    c.add_record(info)
#print(c_python)
h_python = initial_set(df_hours, "indexes")
h = db.add_set("h", 1)
for info in h_python:
    h.add_record(info)

h1_python = initial_set(df_hours, "indexes")
h1 = db.add_set("h1", 1)
for info in h1_python:
    h1.add_record(info)

l_python = initial_set(df_lecturer, "lecturer")
l = db.add_set("l", 1)
for info in l_python:
    l.add_record(info)

j_python = initial_set(df_course_conflict, "indexes")
j = db.add_set("j", 1)
for info in j_python:
    j.add_record(info)

d_python = [str(i) for i in range(1,6)]
d = db.add_set("d", 1)
for info in d_python:
    d.add_record(info)

# initial paremeter
n_c_python = initial_parameter_1(df_course_info, "course", "number_class")
n = db.add_parameter_dc("n", [c])
for cp in c_python:
    if cp in n_c_python.keys():
        n.add_record(cp).value = int(n_c_python[cp])
    else:
        n.add_record(cp).value = 0
#print(n_c_python)
a_c_l_python = initial_parameter_2(df_course_info, "course", "lecturer")
a = db.add_parameter_dc("a", [c, l])
for cp in c_python:
    for lp in l_python:
        if (cp, lp) in a_c_l_python.keys():
            a.add_record((cp, lp)).value = a_c_l_python[(cp, lp)]
        else:
            a.add_record((cp, lp)).value = 0
#print(a_c_l_python)
t_h_h1_python = initial_parameter_2(df_time_conflict, "time", "conflict")
t = db.add_parameter_dc("t", [h, h1])
for hp in h_python:
    for h1p in h1_python:
        if (hp, h1p) in t_h_h1_python.keys():
            t.add_record((hp, h1p)).value = t_h_h1_python[(hp, h1p)]
        else:
            t.add_record((hp, h1p)).value = 0 
#print(t_h_h1_python)
s_j_c_python = {}
for i in range(len(df_course_conflict.indexes)):
    f = df_course_conflict.course[i].split(",")
    for j in f:
        s_j_c_python[(str(df_course_conflict.indexes[i]),str(j))] = 1
s = db.add_parameter_dc("s", [j, c])
for jp in j_python:
    for cp in c_python:
        if (jp, cp) in s_j_c_python.keys():
            s.add_record((jp, cp)).value = s_j_c_python[(jp, cp)]
        else:
            s.add_record((jp, cp)).value = 0
#print(s_j_c_python)
p_c_h_python = {}
for i in range(len(df_course_info.course)):
    f = df_course_info.valid_time[i].split(",")
    for j in f:
        p_c_h_python[(str(df_course_info.course[i]), str(j))] = 1
#print(p_c_h_python)
p = db.add_parameter_dc("p", [c, h])
for cp in c_python:
    for hp in h_python:
        if (cp, hp) in p_c_h_python.keys():
            p.add_record((cp, hp)).value = 1
        else:
            p.add_record((cp, hp)).value = 0

df_possible_time.fillna(0,inplace=True)
b_l_d_h_python = {}
for i in range(len(df_possible_time.lecturer)):
    for j in range(1, 6):
        if df_possible_time[f"day{j}"][i] == 0:
            continue
        f = df_possible_time[f"day{j}"][i].split(",")
        for k in f:
            b_l_d_h_python[(str(df_possible_time.lecturer[i]), str(j), str(k))] = 1
b = db.add_parameter_dc("b", [l, d, h])
for lp in l_python:
    for dp in d_python:
        for hp in h_python:
            if (lp, dp, hp) in b_l_d_h_python.keys():
                b.add_record((lp, dp, hp)).value = b_l_d_h_python[(lp, dp, hp)]
            else:
                b.add_record((lp, dp, hp)).value = 0

opt = ws.add_options()
opt.defines["gdxincname"] = db.name
m = ws.add_job_from_file("proj2.gms")
m.run(opt, databases = db)

dict_course = {}
for i in range(len(df_course_info.course)):
    dict_course[df_course_info.course[i]] = df_course_info.course_name[i]
dict_lecturer = {}
for i in range(len(df_course_info.course)):
    dict_lecturer[df_course_info.course[i]] = df_course_info.lecturer_name[i]

dict_day = {}
dict_day["1"] = "شنبه"
dict_day["2"] = "یکشنبه"
dict_day["3"] = "دوشنبه"
dict_day["4"] = "سه‌شنبه"
dict_day["5"] = "چهارشنبه"

dict_hour = {}
dict_hour["1"] = "7:45-9:15"
dict_hour["2"] = "9:15-10:45"
dict_hour["3"] = "10:45-12:15"
dict_hour["4"] = "13:30-15:00"
dict_hour["5"] = "15:00-16:30"
dict_hour["6"] = "8:00-10:00"
dict_hour["7"] = "10:00-12:00"
dict_hour["8"] = "13:00-15:00"
dict_hour["9"] = "15:00-17:00"
dict_hour["10"] = "17:00-19:00"

courses = pd.DataFrame(columns=["course_name", "lecturer", "days", "time"], index=range(1,1 + len(df_course_info.course)))
info = []
for rec in m.out_db["delta"]:
    if rec.level == 1:
        l = []
        l.append(dict_course[int(rec.key(0))])
        l.append(dict_lecturer[int(rec.key(0))])
        l.append(dict_day[rec.key(1)])
        l.append(dict_hour[rec.key(2)])
        info.append(l)

for i in range(len(info)):
    courses.at[i+1, "course_name"] = info[i][0]
    courses.at[i+1, "lecturer"] = info[i][1]
    courses.at[i+1, "days"] = info[i][2]
    courses.at[i+1, "time"] = info[i][3]
courses.to_excel('out_put.xlsx')