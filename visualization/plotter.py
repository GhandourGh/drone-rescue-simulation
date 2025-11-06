"""
Matplotlib visualization for drone rescue simulation
Live path plotting and search coverage visualization
"""
import matplotlib.pyplot as plt  # Import plotting library



class SimulationPlotter:
    def __init__(self, grid_size):
        """
        Initialize the plotter for drone simulation visualization.

        Args:
            grid_size (tuple): (rows, cols) of the search area
        """
        self.grid_size = grid_size  # Store grid dimensions
        self.fig, self.ax = plt.subplots(figsize=(10, 8))  # Create figure and axes
        self.setup_plot()  # Initialize the plot layout

    def setup_plot(self):
        """Initialize the plot with grid and labels."""
        rows, cols = self.grid_size  # Unpack grid size
        self.ax.set_xlim(-0.5, cols - 0.5)  # Set x-axis limits (columns)
        self.ax.set_ylim(-0.5, rows - 0.5)  # Set y-axis limits (rows)
        self.ax.set_aspect('equal')  # Make grid cells square
        self.ax.grid(True, alpha=0.3)  # Show grid lines with transparency
        self.ax.set_title('Drone Rescue Simulation - Live Search', fontsize=14, fontweight='bold')  # Plot title
        self.ax.set_xlabel('Columns')  # X-axis label
        self.ax.set_ylabel('Rows')  # Y-axis label
        self.ax.invert_yaxis()  # Flip y-axis so (0,0) is top-left

    def update_plot(self, drone, environment, step):
        """
        Update the plot with current simulation state.

        Args:
            drone: RescueDrone instance
            environment: SearchEnvironment instance
            step (int): Current simulation step
        """
        self.ax.clear()  # Clear previous plot elements
        self.setup_plot()  # Re-setup grid and labels

        # Plot obstacles (red squares)
        for obstacle in environment.obstacles:  # Loop through each obstacle
            self.ax.plot(obstacle[1], obstacle[0], 'rs', markersize=10, markeredgecolor='darkred',
                         # Plot red square at obstacle position
                         label='Obstacles' if obstacle == environment.obstacles[0] else "")  # Add label only for first obstacle

        # Plot remaining targets (green stars)
        for target in environment.targets:  # Loop through remaining targets
            self.ax.plot(target[1], target[0], 'g*', markersize=15,  # Plot green star at target position
                         label='Targets' if target == environment.targets[0] else "")  # Add label only for first target

        # Plot found targets (blue circles)
        for found_target in drone.found_targets:  # Loop through found targets
            self.ax.plot(found_target[1], found_target[0], 'bo', markersize=8, alpha=0.5,
                         # Plot blue circle at found target
                         label='Found Targets' if found_target == drone.found_targets[0] else "")  # Add label only for first found target

        # Plot drone path (blue line)
        if len(drone.path_history) > 1:  # Check if drone has moved
            path_x = [pos[1] for pos in drone.path_history]  # Extract all column coordinates
            path_y = [pos[0] for pos in drone.path_history]  # Extract all row coordinates
            self.ax.plot(path_x, path_y, 'b-', alpha=0.6, linewidth=2, label='Drone Path')  # Plot blue path line

        # Plot current drone position (blue drone)
        self.ax.plot(drone.position[1], drone.position[0], 'D', color='blue', markersize=10, label='Drone')  # Diamond marker for drone

        # Add info text
        info_text = f'Step: {step}\nTargets Found: {len(drone.found_targets)}\nBattery: {drone.battery}'  # Create status text
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,  # Position text at top-left
                     verticalalignment='top', fontsize=10,  # Text alignment and size
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))  # Text box styling

        # Add legend (only first occurrence of each type)
        handles, labels = self.ax.get_legend_handles_labels()  # Get all legend items
        by_label = dict(zip(labels, handles))  # Remove duplicate labels
        self.ax.legend(by_label.values(), by_label.keys(), loc='upper right')  # Display legend

        plt.tight_layout()  # Adjust layout to fit elements
        plt.pause(0.1)  # Pause to see the animation between steps

