from ortools.sat.python import cp_model

# Documentation : https://developers.google.com/optimization/cp/cp_solver?hl=fr
def solve_packing(width, list_rectangles):
        model = cp_model.CpModel()
        n = len(list_rectangles)

        max_lenght = sum(l for _, l in list_rectangles)

        x = [model.new_int_var(0, width, f'x{i}') for i in range(n)]
        y = [model.new_int_var(0, max_lenght, f'y{i}') for i in range(n)]
        r = [model.NewBoolVar(f'r{i}') for i in range(n)]

        # Dimensions en fonction de la rotation
        lst_widths = []
        lst_heights = []
        for i, (w, h) in enumerate(list_rectangles):
            lst_widths.append(model.NewIntVar(0, width, f'width{i}'))
            lst_heights.append(model.NewIntVar(0, max_lenght, f'height{i}'))
            model.Add(lst_widths[i] == w).OnlyEnforceIf(r[i].Not())
            model.Add(lst_widths[i] == h).OnlyEnforceIf(r[i])
            model.Add(lst_heights[i] == h).OnlyEnforceIf(r[i].Not())
            model.Add(lst_heights[i] == w).OnlyEnforceIf(r[i])

        # Variable à minimiser : hauteur du grand rectangle
        H = model.NewIntVar(0, max_lenght, 'H')
        for i in range(n):
            model.Add(x[i] + lst_widths[i] <= width)
            model.Add(y[i] + lst_heights[i] <= H)

        # Pas de chevauchement
        for i in range(n):
            for j in range(i + 1, n):
                x_intervals = []
                y_intervals = []

                for i in range(n):
                    x_int = model.NewIntervalVar(x[i], lst_widths[i], x[i] + lst_widths[i], f'x_int{i}')
                    y_int = model.NewIntervalVar(y[i], lst_heights[i], y[i] + lst_heights[i], f'y_int{i}')
                    x_intervals.append(x_int)
                    y_intervals.append(y_int)

                model.AddNoOverlap2D(x_intervals, y_intervals)

        model.Minimize(H)

        # Solve
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            solution = {
                "hauteur": solver.Value(H),
                "positions": [
                    {
                        "rect": i,
                        "x": solver.Value(x[i]),
                        "y": solver.Value(y[i]),
                        "rotated": solver.Value(r[i]),
                        "w": solver.Value(lst_widths[i]),
                        "h": solver.Value(lst_heights[i])
                    }
                    for i in range(n)
                ]
            }
            return solution
        else:
            return {"hauteur": None, "positions": None}
