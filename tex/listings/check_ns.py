x_points = [
	   (1, 1),
	   (-1, 1),
	   (-1, -1),
	   (1, -1)
]
	
	
def M_det(a, b, c, e):
    return a**3 + 2*b*c*e - a*(b**2 + c**2 + e**2)


def M_det_raw(n1, d1, n2, d2, n3, d3, n4, d4):
    l1 = n1 / d1
    l2 = n2 / d2
    l3 = n3 / d3
    l4 = n4 / d4
    a = l1 + l2 + l3 + l4
    b = l1 - l2 - l3 + l4
    c = l1 + l2 - l3 - l4
    e = l1 - l2 + l3 - l4
    return M_det(a, b, c, e)


def make_d_surface(a0, a1, a2):
    return lambda x1, x2: a0 + a1*x1 + a2*x2


def place_observations(d_surface, n):
    d_values = [
    	d_surface(*x_point)
    	for x_point in x_points
    ]
    
    
    max_abs_M_det = -1
    best_placements = []
    for n1 in range(0, n):
        for n2 in range(0, n):
            for n3 in range(0, n):
                if not 1 <= n1 + n2 + n3 <= n:
                    continue
                n4 = n - (n1 + n2 + n3)
                ns = [n1, n2, n3, n4]
                abs_M_det = abs(M_det_raw(
                    n1, d_values[0],
                    n2, d_values[1],
                    n3, d_values[2],
                    n4, d_values[3]
                ))
                if max_abs_M_det < abs_M_det:
                    best_placements = [ns]
                    max_abs_M_det = abs_M_det
                elif abs(max_abs_M_det-abs_M_det)<1e-4:
                    best_placements.append(ns)
    
    return best_placements
    
d_surfaces_params = [
    (40, 0, 0),
    (40, -1, 0),
    (40, -4, 0),
    (40, -8, 0),
    (40, -12, 0),
    (40, -30, 0),
    (40, -39, 0),
    (40, -39.5, 0)
]
    
n = 5

print(f'n = {n}')
for d_surface_params in d_surfaces_params:
    d_surface = make_d_surface(*d_surface_params)
    best_placement = place_observations(d_surface, n)
    print('d(x1, x2) >= {} + {}*x1 + {}*x2'
    	.format(*d_surface_params))
    print('best placements: ', best_placement)