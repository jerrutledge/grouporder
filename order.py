# UPDATE THESE FILE SETTINGS EACH TIME YOU USE THIS SCRIPT
input_file_name = "groupinfo.txt"
performing_groups = ["MI", "UM", "WB", "ACE", "AB", "Committee", "ATone"]
earliest_intermission_time = 42 # shortest accpetable first half (in minutes)

import csv
import pprint
import datetime
import time
import itertools

# has name, group time, all groups that can be placed next to this group
class Group(object):
    """docstring for Group"""
    master_list = []

    def __init__(self, name, strtime, groups):
        self.name = name
        x = time.strptime(strtime,'%M:%S')
        self.time = datetime.timedelta(minutes=x.tm_min,
            seconds=x.tm_sec).total_seconds()
        self.groups = groups
        self.master_list.append(self)
    
def get_group(name):
    for r in Group.master_list:
        if r.name == name:
            return r

with open(input_file_name, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    x = list(reader)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)

for group in x:
    Group(group[1], group[0], group[2:])

# sets = all possible set permutations
sets = itertools.permutations(performing_groups)

first_half_min = 42*60 # calculated from the total show length. 

working_sets = []

# take all sets and check if they're valid
# append all valid sets to the working_sets array
for set_n in sets:
    set_time = 0
    valid = True
    valid = True
    checks = ""
    intermission_at = 0
    intermission_time = 0
    for x in range(0,6):
        grp = get_group(set_n[x])
        set_time += grp.time
        if (set_time >= first_half_min) and (set_time - grp.time <= first_half_min):
            intermission_at = x+1
            intermission_time = set_time
        else:
            next_group = set_n[x+1]
            if next_group in grp.groups:
                # no overlapping members
                checks += grp.name + " next to " + next_group + "\n"
                continue
            else:
                # set is invalid
                valid = False
    if intermission_time > 3360 or intermission_at > 5:
        valid = False
    second_half_time = 5254 - intermission_time
    if valid:
        set_order = list(set_n)
        set_order.insert(intermission_at, 
            "-- {}:{} intermission {}:{} --".format(int(intermission_time/60), 
            int(intermission_time%60), int(second_half_time/60), int(second_half_time%60)))
        working_sets.append(set_order)

pp.pprint(working_sets)

with open("working_sets.txt", "w") as f:
    for set_n in working_sets:
        for item in set_n:
            f.write(item)
        f.write("\n")
