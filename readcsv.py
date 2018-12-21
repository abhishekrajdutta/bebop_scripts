import csv
import numpy as np

goals = []
goal = np.array([0.0,0.0,0.0,0.0])

with open('PointsOutputStreamKK01a.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\n')
    line_count = 0
    for row in csv_reader:
    	num = float(row[0])
    	goal[line_count % 3] = num
    	if line_count %3 == 2:
    		goals.append(np.array([goal[0],goal[1],goal[2],0.0]))
    	line_count += 1

for g in goals:
	print g