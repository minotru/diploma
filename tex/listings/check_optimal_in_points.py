import math
import numpy as np

x_from = -1
x_to = 1
h = 0.1
n = int((x_to - x_from) / h)

def d_134(x1, x2):
	return 2 - x1 + 3*x2 - 2*x1*x2 + 
		1.5*x1**2 + 2.5*x2**2

def d_234(x1, x2):
	return 2 + 2*x1 + 2*x2 + 
		x1*x2 +1.5*(x1**2) + 1.5*(x2**2) 

def d_123(x1, x2):
	return 2 + 3*x1 - x2 - 2*x1*x2 +
		2.5*x1**2 + 1.5*x2**2

def d_124(x1, x2):
	return 2 - x1 + 3*x2 - 2*x1*x2 +
		1.5*x1^2 + 2.5*x2^2

d = d_134

def make_point(i, j):
	return (x_from + i*h, x_from + j*h)

def M(x):
	matrix = np.zeros((3, 3))
	for i in range(3):
	v = [[1, x[i][0], x[i][1]]]
	d_i = d(x[i][0], x[i][1])
	matrix += (1/d_i) * np.matmul(np.transpose(v), v)
	return matrix

def test(d):
	max_points = []
	max_M_det = float('-inf')
	eps = 10e-6
	
	for i1 in range(0, n + 1):
		for j1 in range(0, n + 1):
			for i2 in range(0, n + 1):
				for j2 in range(0, n + 1):
					for i3 in range(0, n + 1):
						for j3 in range(0, n + 1):
							x1 = make_point(i1, j1)
							x2 = make_point(i2, j2)
							x3 = make_point(i3, j3)
							
							M_det=abs(
								np.linalg.det(M([x1, x2, x3]))
							)
							if M_det > max_M_det:                          
								max_M_det = M_det
								max_points = [x1, x2, x3]
	
		print(max_points, max_M_det)
	
	print('Plan 1, 2, 3')
	test(d_123)
	print('Plan 1, 2, 4')
	test(d_124)
	print('Plan 1, 3, 4')
	test(d_134)
	print('Plan 2, 3, 4')
	test(d_234)