import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def steady_state_gs(error, tolerance, nx, ny, old_temp):
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    T_gs = np.copy(old_temp)

    # Gauss-Seidel method
    k = 2 * (dx**2 + dy**2) / (dx**2 * dy**2)

    iteration = 1

    # convergence loop
    while error > tolerance:

        for i in range(1, nx - 1):

            for j in range(1, ny - 1):

                term3 = (old_temp[i + 1, j] + T_gs[i - 1, j]) / dx**2
                term4 = (old_temp[i, j + 1] + T_gs[i, j - 1]) / dy**2
                T_gs[i, j] = term3 / k + term4 / k

        # calculates convergence error
        error = np.max(np.abs(old_temp - T_gs))

        # update temp value
        old_temp = np.copy(T_gs)
        iteration += 1

        if iteration % 10:

            # Plotting of results
            plt.figure(2)
            plt.contourf(T_gs, levels=10)
            plt.gca().invert_yaxis()
            plt.colorbar()
            title_text = f'GS iterations = {iteration}'
            plt.title(title_text)
            plt.xlabel('x')
            plt.ylabel('y')
            # control iteration graph speed
            plt.pause(0.05)

            # clears results
            plt.clf()

    return T_gs


# makes grid
nx = 10
ny = 10
T = np.zeros((nx, ny))
old_temp = np.zeros((nx, ny))

# error and tolerance placeholder
error = 100000000000000000000000000
tolerance = .0001

def update_boundary_conditions(*args):
    T[0, :] = top_slider.get()
    T[-1, :] = bottom_slider.get()
    T[:, 0] = left_slider.get()
    T[:, -1] = right_slider.get()
    T[0, 0] = top_left_slider.get()
    T[0, -1] = top_right_slider.get()
    T[-1, 0] = bottom_left_slider.get()
    T[-1, -1] = bottom_right_slider.get()

def run_data():

    # updates T with the slider values
    update_boundary_conditions()

    # function calling
    T_result = steady_state_gs(error, tolerance, nx, ny, T)

    # displays final steady-state
    plt.figure()

    # plots final graph
    plt.contourf(T_result, levels=20)
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.title("Final Temperature Distribution")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.show()

def create_slider(root, label_text, command):
    tk.Label(root, text=label_text).pack()
    slider = tk.Scale(root, from_=0, to=5000, orient=tk.HORIZONTAL, command=command)
    slider.pack()
    return slider

root = tk.Tk()

# sliders to create boundaries
top_slider = create_slider(root, "Top Boundary", update_boundary_conditions)
bottom_slider = create_slider(root, "Bottom Boundary", update_boundary_conditions)
left_slider = create_slider(root, "Left Boundary", update_boundary_conditions)
right_slider = create_slider(root, "Right Boundary", update_boundary_conditions)
top_left_slider = create_slider(root, "Top Left Boundary", update_boundary_conditions)
top_right_slider = create_slider(root, "Top Right Boundary", update_boundary_conditions)
bottom_left_slider = create_slider(root, "Bottom Left Boundary", update_boundary_conditions)
bottom_right_slider = create_slider(root, "Bottom Right Boundary", update_boundary_conditions)

run_button = tk.Button(root, text="Run", command=run_data)
run_button.pack()

root.mainloop()