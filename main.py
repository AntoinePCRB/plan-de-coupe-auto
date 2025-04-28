from utils.packing_solver import solve_packing

if __name__ == "__main__":
    width = 10
    lst_rectangles = [(3, 4), (5, 2), (6, 3), (2, 2), (4, 5)]

    solution = solve_packing(width, lst_rectangles)
    print("Hauteur minimale trouvée :", solution["hauteur"])
    print("Placement :", solution["positions"])