from sympy import *
import numpy as np


# points
x_points_arr = [
    [1, 1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [-1, 1, -1],
]
x_points = {
    i: x_point
    for i, x_point in zip(range(1, 9), x_points_arr)
}

# function to build a plan
def build_plan_in_points(points, points_id):
    points = np.array(points)
    
    N = 3
    n_points = 3

    d_names = [
        f'd{point_id}' for point_id in points_id
    ]
    d1, d2, d3 = symbols(d_names)
    d = Matrix([d1, d2, d3])
    X = Matrix(MatrixSymbol('X', N, n_points)).T
    
    M = Matrix.zeros(N)
    for i in range(n_points):
        M +=  X[:, i] * X[:, i].T / d[i]
        
    a, b, c, e = symbols('a b c e')
    x0, x1, x2 = symbols('x0 x1 x2')

    M_abc = Matrix([
        [a, b, c],
        [b, a, e],
        [c, e, a]
    ]) / 3

    M_abc_inv = M_abc.inverse_ADJ()

    x = Matrix([x0, x1, x2])

    df =  x.T * M_abc_inv * x / 3
    df.simplify()
    
    X_subs_map = {
        X[i, j]: points[j, i]
        for i in range(n_points)
        for j in range(n_points)
    }
    
    M_exact = M.subs(X_subs_map)
    
    abc_subs_map = {
        'a': M_exact[0, 0],
        'b': M_exact[0, 1],
        'c': M_exact[0, 2],
        'e': M_exact[1, 2]
    }
    
    df_exact = df.subs(abc_subs_map)
    df_exact.simplify()
    df_exact = df_exact[0]
    df_exact = df_exact.collect(['x0', 'x1', 'x2'])
    
    return df_exact

    
def prove_eq_in_points(d, points, points_id):
    for point_id, point in zip(points_id, points):
        subs_map = dict(zip(['x0', 'x1', 'x2'], point))
        print(f'd(x{point_id}) =', d.subs(subs_map))


plans_points_ids = [
    [1, 2, 3],
    [1, 2, 4],
    [1, 3, 4],
    [2, 3, 4]
]

if __name__ == '__main__':
    for plan_id, points_id in enumerate(plans_points_ids):
        plan_points = [
            x_points[point_id]
            for point_id in points_id
        ]
    
        d = build_plan_in_points(plan_points, points_id)
        
        print(f'plan #{plan_id + 1}:')
        print('d(x0, x1, x2) >= ', d)
        
        print('prove that equal in points:')
        prove_eq_in_points(d, plan_points, points_id)
        
        print()

