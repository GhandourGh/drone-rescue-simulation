import matplotlib.pyplot as plt


class SimulationPlotter:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        print(f"📊 Plotter initialized for {grid_size[0]}x{grid_size[1]} grid")

    def _create_plot(self, title, drone, environment, info_text):
        fig, ax = plt.subplots(figsize=(10, 8))

        # Setup plot (same as before)
        rows, cols = self.grid_size
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        ax.invert_yaxis()

        # 🆕 FIXED DRAWING ORDER - most important elements LAST
        # 1. Plot obstacles FIRST (background)
        for obstacle in environment.obstacles:
            ax.plot(obstacle[1], obstacle[0], 'rs', markersize=10, label='Obstacles', zorder=1)

        # 2. Plot targets SECOND
        for target in environment.targets:
            ax.plot(target[1], target[0], 'g*', markersize=15, label='Targets Remaining', zorder=2)

        # 3. Plot found targets THIRD
        for found_target in drone.found_targets:
            ax.plot(found_target[1], found_target[0], 'bo', markersize=8, alpha=0.7, label='Targets Found', zorder=3)

        # 4. Plot drone path FOURTH
        if len(drone.path_history) > 1:
            path_x = [pos[1] for pos in drone.path_history]
            path_y = [pos[0] for pos in drone.path_history]
            ax.plot(path_x, path_y, 'b-', alpha=0.6, linewidth=2, label='Drone Path', zorder=4)

        # 5. Plot current drone position LAST (on top)
        ax.plot(drone.position[1], drone.position[0], 'D', color='blue', markersize=12, label='Drone', zorder=5)

        # Rest of the code same...
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')

        plt.tight_layout()
        return fig, ax

    def plot_step(self, drone, environment, step):
        """Create a static plot for current step"""
        info_text = f'Step: {step}\nTargets Found: {len(drone.found_targets)}\nBattery: {drone.battery}'
        fig, ax = self._create_plot(f'Drone Rescue - Step {step}', drone, environment, info_text)

        plt.show(block=False)
        plt.pause(0.01)
        plt.close()

    def plot_final_state(self, drone, environment):
        """Create final static plot that stays open"""
        info_text = f'Final State\nSteps: {len(drone.path_history)}\nTargets Found: {len(drone.found_targets)}\nBattery: {drone.battery}'
        fig, ax = self._create_plot('Drone Rescue - Final Mission State', drone, environment, info_text)

        plt.show()
        print("✅ Final plot displayed!")