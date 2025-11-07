import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib as mpl

class SimulationPlotter:
    """Handles visualization of drone navigation and mission progress."""

    def __init__(self, grid_size):
        self.grid_size = grid_size  # (rows, cols)
        self.drone_colors = {}  # Maps drone_id to color for consistent displays

    def plot_step(self, drones, environment, step):
        """Display current mission state for multiple drones."""
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
        """Display final mission results for multiple drones."""
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

    def _create_plot(self, title, drones, environment, info_text):
        """Create and configure the mission visualization plot."""
        rows, cols = self.grid_size
        fig, ax = plt.subplots(figsize=(12, 10))
        plt.subplots_adjust(right=0.82)

        # Set axes and grid style
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect("equal")
        ax.invert_yaxis()
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticks([x - 0.5 for x in range(cols + 1)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(rows + 1)], minor=True)
        ax.grid(True, which="major", linestyle="-", linewidth=1, alpha=0.35, color="#b5b5b5")
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.18)
        ax.set_title(title, fontsize=18, fontweight="bold", pad=16)
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
        ax.set_facecolor("#f9faff")
        for spine in ax.spines.values():
            spine.set_color("#b8c6d2")
            spine.set_linewidth(1.2)

        # Draw environment NFZs
        self._draw_obstacles(ax, environment.nfz_rectangles)

        # Build all waypoints—assume all drones share the same set
        all_waypoints = []
        if drones:
            for drone in drones:
                if hasattr(drone, 'waypoints'):
                    all_waypoints.extend(drone.waypoints)
        # Mark locations where a waypoint and target overlap, for offsetting
        target_points = set(environment.targets)
        waypoint_points = set(all_waypoints)
        overlap_points = target_points & waypoint_points

        # Draw targets first, with offset if necessary
        self._draw_targets(ax, environment.targets, [target for drone in drones for target in drone.found_targets], overlap_points)

        # Draw all waypoints above targets; always clearly visible!
        self._draw_waypoints(ax, all_waypoints)

        # Draw drone paths and positions
        color_map = mpl.colormaps.get_cmap('tab10')
        for idx, drone in enumerate(drones):
            color = self.drone_colors.setdefault(drone.drone_id, color_map(idx % 10))
            self._draw_drone_path(ax, drone.path_history, color)
            self._draw_drone_position(ax, drone.position, color, drone.drone_id)

        # Professional, grouped legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(
            by_label.values(),
            by_label.keys(),
            loc="upper left",
            bbox_to_anchor=(1.02, 0.98),
            borderaxespad=0.0,
            frameon=True,
            fontsize=10,
            title="Legend"
        )

        # Info box
        fig.text(
            0.99, 0.18, info_text,
            ha="right", va="bottom",
            fontsize=12,
            bbox=dict(boxstyle="round,pad=0.7", facecolor="#e4f2ff", edgecolor="#2980b9", alpha=0.87)
        )

        return fig, ax

    def _draw_obstacles(self, ax, nfz_rectangles):
        """Draw No-Fly Zones as semi-transparent red rectangles."""
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
                linewidth=2.7,
                edgecolor="#b61515",
                facecolor="#f7b4b4",
                alpha=0.5,
                zorder=1,
                label="No-Fly Zone" if label_once else None,
            )
            ax.add_patch(rect)
            label_once = False

    def _draw_waypoints(self, ax, waypoints):
        """Draw waypoints as purple diamonds with large white border, always on top."""
        if not waypoints:
            return
        for i, (r, c) in enumerate(waypoints):
            ax.plot(
                c, r, marker="D", markersize=13,
                markerfacecolor="#781C81", markeredgecolor="white", markeredgewidth=3,
                linestyle="None", zorder=9, label="Waypoint" if i == 0 else None
            )
            ax.text(
                c, r-0.32, f"W{i + 1}", fontsize=10, ha="center", va="center",
                color="#781C81", fontweight="bold", zorder=10
            )

    def _draw_targets(self, ax, targets, found_targets, overlap_points=None):
        """Draw remaining and found targets—offset if overlapping waypoint."""
        offset = 0.18
        used_label = {"Target (remaining)": False, "Target (found)": False}
        # Remaining targets
        if targets:
            for (r, c) in targets:
                # If overlap, slightly offset target marker
                if overlap_points and (r, c) in overlap_points:
                    tr, tc = r + offset, c + offset
                else:
                    tr, tc = r, c
                label = None if used_label["Target (remaining)"] else "Target (remaining)"
                ax.plot(tc, tr, marker="*", markersize=18,
                        linestyle="None", color="green", markeredgecolor="white",
                        markeredgewidth=2.5, alpha=0.94, zorder=7,
                        label=label)
                used_label["Target (remaining)"] = True
        # Found targets
        if found_targets:
            for (r, c) in found_targets:
                # If overlap, offset by -offset
                if overlap_points and (r, c) in overlap_points:
                    tr, tc = r - offset, c - offset
                else:
                    tr, tc = r, c
                label = None if used_label["Target (found)"] else "Target (found)"
                ax.plot(tc, tr, marker="p", markersize=15,
                        linestyle="None", color="#277ab6", markeredgecolor="white",
                        markeredgewidth=2.5, alpha=0.85, zorder=8,
                        label=label)
                used_label["Target (found)"] = True

    def _draw_drone_path(self, ax, path_history, color):
        """Draw drone's path in its assigned color."""
        if len(path_history) > 1:
            xs = [c for (r, c) in path_history]
            ys = [r for (r, c) in path_history]
            ax.plot(xs, ys, "-", alpha=0.83, linewidth=2.9, color=color, zorder=6, label=None)

    def _draw_drone_position(self, ax, position, color, drone_id):
        """Highlight current drone position, filled bold, with ID."""
        r, c = position
        ax.plot(c, r, marker="o", markersize=15, linestyle="None", color=color, zorder=10,
                markeredgecolor='white', markeredgewidth=2.5, label=f"Drone {drone_id}")
        ax.text(c, r, str(drone_id), fontsize=10, ha="center", va="center",
                color="white", fontweight="bold", zorder=11)

