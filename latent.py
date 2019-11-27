# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 23:13:30 2019

@author: Koushik
"""
import numpy as np
from numpy import *
import time
import math
import matplotlib.pyplot as plt
filename = 'ratings.data'
n = 0 #users
m = 0 #items
file = open(filename,'r')
for line in file:
    ind = line.split()
    temp_n = int(ind[0])
    temp_m = int(ind[1])
    if temp_n > n:
        n = temp_n
    if temp_m > m:
        m = temp_m
file.close()
k = 20
lam = 0.2
eta = 0.005
iter = 50
p = random.rand(n,k)*sqrt(5.0/k)
q = random.rand(m,k)*sqrt(5.0/k)
obj = empty(iter)
error = 0
minerror = 100000000
Ratings = np.zeros((n + 1, m + 1))

# Reading file
with open("ratings.data", "r") as data_file:
	for line in data_file:
		line_values = line.split("\t")
		a = int(line_values[0])
		b = int(line_values[1])
		Ratings[a][b] = float(line_values[2])
data_file.close()
start_time = time.time()
for num in range(iter):
    print(num)
    file = open(filename,'r')
    for line in file:
        ind = line.split()
        u = int(ind[0])-1
        i = int(ind[1])-1
        r = int(ind[2])
        eps = 2*(r-dot(q[i,],p[u,]))
        temp_q = q[i,] + eta*(eps*p[u,]-2*lam*q[i,])
        temp_p = p[u,] + eta*(eps*q[i,]-2*lam*p[u,])
        q[i,] = temp_q
        p[u,] = temp_p
    file.close()
    error = 0
    file = open(filename,'r')
    for line in file:
        ind = line.split()
        u = int(ind[0])-1
        i = int(ind[1])-1
        r = int(ind[2])
        error += (r-dot(q[i,],p[u,]))**2
    file.close()
    error = error + lam*(sum(p**2)+sum(q**2))
    obj[num] = error
    print(error)
    if (error< minerror):
        minerror = error
    else:
        break


print(p.shape, q.shape)
new_Ratings = p@q.T

squared_error_sum = 0
mean_absolute_error = 0
number_of_predictions = 0

for i in range(len(Ratings)-1):
	for j in range(len(Ratings[i])-1):
		if(Ratings[i][j] != 0):
			squared_error_sum += (Ratings[i][j] - new_Ratings[i][j]) ** 2
			mean_absolute_error += abs(Ratings[i][j] - new_Ratings[i][j])
			number_of_predictions += 1

# Root mean square error
rmse = math.sqrt(squared_error_sum / float(number_of_predictions))
mae = mean_absolute_error / float(number_of_predictions)
print("Time for Latent : " + str(time.time() - start_time))
print("RMSE: " + str(rmse))
print("MAE: " + str(mae))
   
    

