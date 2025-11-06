import matplotlib.pyplot as plt


class SimulationPlotter:
    """Handles visualization of drone navigation and mission progress"""

    def __init__(self, grid_size):
        self.grid_size = grid_size

    def _create_plot(self, title, drone, environment, info_text):
        """Create and configure the mission visualization plot"""
        fig, ax = plt.subplots(figsize=(10, 8))
        rows, cols = self.grid_size

        # Configure plot layout
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        ax.invert_yaxis()

        # Draw environment elements in order of visibility
        self._draw_obstacles(ax, environment.obstacles)
        self._draw_waypoints(ax, drone.waypoints)
        self._draw_targets(ax, environment.targets, drone.found_targets)
        self._draw_drone_path(ax, drone.path_history)
        self._draw_drone_position(ax, drone.position)

        # Add mission info overlay
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        # Configure legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')

        plt.tight_layout()
        return fig, ax

    def _draw_obstacles(self, ax, obstacles):
        """Draw obstacles as red squares"""
        for obstacle in obstacles:
            ax.plot(obstacle[1], obstacle[0], 'rs', markersize=10, label='Obstacles', zorder=1)

    def _draw_waypoints(self, ax, waypoints):
        """Draw waypoints as purple diamonds with labels"""
        if waypoints:
            for i, waypoint in enumerate(waypoints):
                ax.plot(waypoint[1], waypoint[0], 'D', color='purple', markersize=10,
                        label='Waypoints' if i == 0 else "", zorder=2)
                ax.text(waypoint[1], waypoint[0], f'W{i + 1}',
                        fontsize=8, ha='center', va='center', color='white', weight='bold')

    def _draw_targets(self, ax, targets, found_targets):
        """Draw remaining and found targets"""
        for target in targets:
            ax.plot(target[1], target[0], 'g*', markersize=15, label='Targets Remaining', zorder=3)
        for found_target in found_targets:
            ax.plot(found_target[1], found_target[0], 'bo', markersize=8, alpha=0.7, label='Targets Found', zorder=4)

    def _draw_drone_path(self, ax, path_history):
        """Draw drone's traveled path"""
        if len(path_history) > 1:
            path_x = [pos[1] for pos in path_history]
            path_y = [pos[0] for pos in path_history]
            ax.plot(path_x, path_y, 'b-', alpha=0.6, linewidth=2, label='Drone Path', zorder=5)

    def _draw_drone_position(self, ax, position):
        """Draw current drone position"""
        ax.plot(position[1], position[0], 'D', color='blue', markersize=12, label='Drone', zorder=6)

    def plot_step(self, drone, environment, step):
        """Display current mission state"""
        info_text = f'Step: {step}\nTargets: {len(drone.found_targets)}\nBattery: {drone.battery}'
        fig, ax = self._create_plot(f'Mission Progress - Step {step}', drone, environment, info_text)
        plt.show(block=False)
        plt.pause(0.01)
        plt.close()

    def plot_final_state(self, drone, environment):
        """Display final mission results"""
        info_text = f'Mission Complete\nSteps: {len(drone.path_history)}\nTargets: {len(drone.found_targets)}\nBattery: {drone.battery}'
        fig, ax = self._create_plot('Mission Complete', drone, environment, info_text)
        plt.show()