import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class SimulationPlotter:
    """Handles visualization of drone navigation and mission progress"""

    def __init__(self, grid_size):
        self.grid_size = grid_size  # (rows, cols)

    # ---------- Public API ----------
    def plot_step(self, drones, environment, step):
        """Display current mission state for multiple drones"""
        total_targets_found = sum(len(drone.found_targets) for drone in drones)
        total_battery = sum(drone.battery for drone in drones)

        info_text = (
            f"Step: {step}\n"
            f"Targets Found: {total_targets_found}\n"
            f"Battery: {total_battery}\n"
            f"Drones Active: {len(drones)}"
        )
        fig, ax = self._create_plot(f"Mission Progress — Step {step}", drones, environment, info_text)
        plt.show(block=False)
        plt.pause(0.01)
        plt.close(fig)

    def plot_final_state(self, drones, environment):
        """Display final mission results for multiple drones"""
        total_targets_found = sum(len(drone.found_targets) for drone in drones)
        total_battery = sum(drone.battery for drone in drones)

        info_text = (
            "Mission Complete\n"
            f"Targets Found: {total_targets_found}\n"
            f"Battery: {total_battery}\n"
            f"Drones: {len(drones)}"
        )
        fig, ax = self._create_plot("Mission Complete", drones, environment, info_text)
        plt.show()

    # ---------- Internals ----------
    def _create_plot(self, title, drones, environment, info_text):
        """Create and configure the mission visualization plot"""
        rows, cols = self.grid_size

        # Leave room on the right for legend + info panel
        fig, ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(right=0.78)  # reserve right margin

        # Axes / grid styling
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect("equal")
        ax.invert_yaxis()

        # Ticks: show cell indices clearly
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticks([x - 0.5 for x in range(cols + 1)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(rows + 1)], minor=True)

        # Grid: light major grid for cells, faint minor grid for borders
        ax.grid(True, which="major", linestyle="-", linewidth=0.6, alpha=0.35)
        ax.grid(True, which="minor", linestyle="-", linewidth=0.4, alpha=0.15)

        # Labels & style
        ax.set_title(title, fontsize=15, fontweight="bold", pad=12)
        ax.set_xlabel("Columns", labelpad=8)
        ax.set_ylabel("Rows", labelpad=8)
        ax.set_facecolor("#fafafa")
        for spine in ax.spines.values():
            spine.set_color("#bbbbbb")

        # Draw environment elements in sensible z-order
        self._draw_obstacles(ax, environment.nfz_rectangles)

        # Use waypoints from first drone (they should all have same waypoints)
        if drones:
            self._draw_waypoints(ax, getattr(drones[0], "waypoints", []))

        self._draw_targets(ax, environment.targets, [target for drone in drones for target in drone.found_targets])

        # Draw paths and positions for all drones
        for drone in drones:
            self._draw_drone_path(ax, drone.path_history, drone.color)
            self._draw_drone_position(ax, drone.position, drone.color, drone.drone_id)

        # Legend (outside the grid, top-right)
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(
            by_label.values(),
            by_label.keys(),
            loc="upper left",
            bbox_to_anchor=(1.01, 1.0),
            borderaxespad=0.0,
            frameon=True,
            title="Legend",
        )

        # Info panel (outside the grid, right side)
        fig.text(
            0.985, 0.50, info_text,
            ha="right", va="center",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="#e8f1ff", edgecolor="#9ec5fe", alpha=0.9, pad=0.6)
        )

        return fig, ax

    def _draw_obstacles(self, ax, nfz_rectangles):
        """Draw No-Fly Zones as semi-transparent red rectangles"""
        if not nfz_rectangles:
            return
        label_once = True
        for nfz in nfz_rectangles:
            top_row, left_col = nfz["top_left"]
            bottom_row, right_col = nfz["bottom_right"]
            width = right_col - left_col + 1
            height = bottom_row - top_row + 1
            rect = Rectangle(
                (left_col - 0.5, top_row - 0.5),
                width, height,
                linewidth=1.8,
                edgecolor="red",
                facecolor="#f7b4b4",
                alpha=0.55,
                zorder=1,
                label="No-Fly Zone" if label_once else None,
            )
            ax.add_patch(rect)
            label_once = False

    def _draw_waypoints(self, ax, waypoints):
        """Draw waypoints as purple diamonds with labels"""
        if not waypoints:
            return
        for i, (r, c) in enumerate(waypoints):
            ax.plot(
                c, r, marker="D", markersize=9,
                markerfacecolor="purple", markeredgecolor="white", markeredgewidth=1.2,
                linestyle="None",
                zorder=3,
                label="Waypoint" if i == 0 else None,
            )
            ax.text(c, r, f"W{i + 1}", fontsize=8, ha="center", va="center",
                    color="white", weight="bold", zorder=4)

    def _draw_targets(self, ax, targets, found_targets):
        """Draw remaining and found targets"""
        # Remaining
        if targets:
            for i, (r, c) in enumerate(targets):
                ax.plot(c, r, marker="*", markersize=15, linestyle="None",
                        color="green", alpha=0.9, zorder=4,
                        label="Target (remaining)" if i == 0 else None)
        # Found
        if found_targets:
            for i, (r, c) in enumerate(found_targets):
                ax.plot(c, r, marker="o", markersize=8, linestyle="None",
                        color="#1f77b4", alpha=0.85, zorder=5,
                        label="Target (found)" if i == 0 else None)

    def _draw_drone_path(self, ax, path_history, color):
        """Draw drone's traveled path with assigned color"""
        if len(path_history) > 1:
            xs = [c for (r, c) in path_history]
            ys = [r for (r, c) in path_history]
            ax.plot(xs, ys, "-", alpha=0.7, linewidth=2.2, color=color,
                    zorder=6, label=f"Drone Path ({color})")

    def _draw_drone_position(self, ax, position, color, drone_id):
        """Draw current drone position with assigned color and ID"""
        r, c = position
        ax.plot(c, r, marker="D", markersize=12,
                linestyle="None", color=color,
                zorder=7, label=f"Drone {drone_id}")
        ax.text(c, r, str(drone_id), fontsize=8, ha="center", va="center",
                color="white", weight="bold", zorder=8)