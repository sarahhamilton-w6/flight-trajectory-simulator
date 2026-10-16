import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ---------------------------------
# Vehicle and atmospheric properties
# ---------------------------------

mass = 100.0          # kg
drag_coefficient = 0.5
area = 0.1            # m^2
air_density = 1.225   # kg/m^3
gravity = 9.81        # m/s^2

# ---------------------------------
# Initial flight conditions
# ---------------------------------

initial_speed = 100.0  # m/s
launch_angle = 45.0   # degrees

angle_rad = np.radians(launch_angle)

vx0 = initial_speed * np.cos(angle_rad)
vy0 = initial_speed * np.sin(angle_rad)

# Starting position
x0 = 0.0
y0 = 0.0

# Initial state
initial_state = [x0, y0, vx0, vy0]

# ---------------------------------
# Equations of motion
# ---------------------------------

def equations_of_motion(t, state):

    x, y, vx, vy = state

    speed = np.sqrt(vx**2 + vy**2)

    drag_factor = (
        0.5 * air_density * drag_coefficient * area / mass
    )

    ax = -drag_factor * speed * vx
    ay = -gravity - drag_factor * speed * vy

    return [vx, vy, ax, ay]

print("Physics model initialized successfully!")

# ---------------------------------
# Flight trajectory simulation
# ---------------------------------

# Stop the simulation when the vehicle reaches the ground
def hit_ground(t, state):
    return state[1]

hit_ground.terminal = True
hit_ground.direction = -1

# Solve the equations of motion
solution = solve_ivp(
    equations_of_motion,
    (0, 100),
    initial_state,
    events=hit_ground,
    max_step=0.05
)

# Extract results
time = solution.t
x = solution.y[0]
y = solution.y[1]
vx = solution.y[2]
vy = solution.y[3]

# Calculate total velocity
speed = np.sqrt(vx**2 + vy**2)

# Calculate flight statistics
maximum_altitude = np.max(y)
flight_time = time[-1]
horizontal_range = x[-1]
maximum_speed = np.max(speed)

print("\n--- Flight Simulation Results ---")
print(f"Maximum Altitude: {maximum_altitude:.2f} m")
print(f"Flight Time: {flight_time:.2f} s")
print(f"Horizontal Range: {horizontal_range:.2f} m")
print(f"Maximum Speed: {maximum_speed:.2f} m/s")

# ---------------------------------
# Flight simulation graphs
# ---------------------------------

# Calculate acceleration components
drag_factor = (
    0.5 * air_density * drag_coefficient * area / mass
)

ax = -drag_factor * speed * vx
ay = -gravity - drag_factor * speed * vy

acceleration = np.sqrt(ax**2 + ay**2)


fig, axs = plt.subplots(2, 2, figsize=(12, 9))

# Graph 1: Flight trajectory
axs[0, 0].plot(x, y)
axs[0, 0].set_title("Flight Trajectory")
axs[0, 0].set_xlabel("Horizontal Distance (m)")
axs[0, 0].set_ylabel("Altitude (m)")
axs[0, 0].grid(True)

# Graph 2: Altitude vs Time
axs[0, 1].plot(time, y)
axs[0, 1].set_title("Altitude vs Time")
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("Altitude (m)")
axs[0, 1].grid(True)

# Graph 3: Speed vs Time
axs[1, 0].plot(time, speed)
axs[1, 0].set_title("Speed vs Time")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("Speed (m/s)")
axs[1, 0].grid(True)

# Graph 4: Acceleration vs Time
axs[1, 1].plot(time, acceleration)
axs[1, 1].set_title("Acceleration vs Time")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("Acceleration (m/s**2)")
axs[1, 1].grid(True)

plt.tight_layout()
plt.savefig("flight_simulation_graphs.png", dpi=300)
plt.show()

import csv

with open("trajectory_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "X", "Y", "Z", "Speed", "Acceleration"])

    for i in range(len(time)):
        writer.writerow([
            time[i],
            x[i],
            0,
            y[i],
            speed[i],
            acceleration[i]
        ])

print("Trajectory data exported successfully!")

with open("trajectory.vtk", "w") as file:
    file.write("# vtk DataFile Version 3.0\n")
    file.write("Flight trajectory\n")
    file.write("ASCII\n")
    file.write("DATASET POLYDATA\n")

    file.write(f"POINTS {len(time)} float\n")
    for xi, yi in zip(x, y):
        file.write(f"{xi} 0 {yi}\n")

    file.write(f"LINES 1 {len(time) + 1}\n")
    file.write(f"{len(time)} " + " ".join(map(str, range(len(time)))) + "\n")

    file.write(f"POINT_DATA {len(time)}\n")
    file.write("SCALARS Speed float 1\n")
    file.write("LOOKUP_TABLE default\n")
    for value in speed:
        file.write(f"{value}\n")

print("VTK trajectory exported successfully!")