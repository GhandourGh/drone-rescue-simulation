import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
import time
from io import BytesIO

# Add your project modules to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_nfz_data, load_waypoints_data, \
    load_drone_starts
from algorithms.waypoint import WaypointNavigator
from simulation.engine import SimulationEngine
from visualization.plotter import SimulationPlotter


class WebPlotter:
    """Adapted plotter for Streamlit web display"""

    def __init__(self, grid_size):
        self.grid_size = grid_size

    def create_plot(self, drones, environment, step, targets_found, total_battery):
        """Create a matplotlib plot suitable for Streamlit"""
        rows, cols = self.grid_size
        fig, ax = plt.subplots(figsize=(10, 8))

        # Basic grid setup
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect("equal")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3)

        # Title and info
        ax.set_title(f"Mission Progress — Step {step}\nTargets: {targets_found} | Battery: {total_battery}",
                     fontsize=12, pad=20)

        # Draw NFZs
        for nfz in environment.nfz_rectangles:
            top_row, left_col = nfz["top_left"]
            bottom_row, right_col = nfz["bottom_right"]
            width = right_col - left_col + 1
            height = bottom_row - top_row + 1
            rect = plt.Rectangle((left_col - 0.5, top_row - 0.5), width, height,
                                 linewidth=2, edgecolor='red', facecolor='lightcoral',
                                 alpha=0.7, label='No-Fly Zone')
            ax.add_patch(rect)

        # Draw waypoints (from first drone)
        if drones and hasattr(drones[0], 'waypoints'):
            for i, waypoint in enumerate(drones[0].waypoints):
                ax.plot(waypoint[1], waypoint[0], 'D', color='purple', markersize=10,
                        label='Waypoints' if i == 0 else "")
                ax.text(waypoint[1], waypoint[0], f'W{i + 1}',
                        fontsize=8, ha='center', va='center', color='white', weight='bold')

        # Draw targets
        for target in environment.targets:
            ax.plot(target[1], target[0], 'g*', markersize=15, label='Targets Remaining')

        # Draw found targets and drone paths
        for drone in drones:
            # Found targets
            for found_target in drone.found_targets:
                ax.plot(found_target[1], found_target[0], 'bo', markersize=8, alpha=0.7, label='Targets Found')

            # Drone path
            if len(drone.path_history) > 1:
                path_x = [pos[1] for pos in drone.path_history]
                path_y = [pos[0] for pos in drone.path_history]
                ax.plot(path_x, path_y, '-', color=drone.color, alpha=0.6, linewidth=2,
                        label=f'Drone {drone.drone_id} Path')

            # Current position
            ax.plot(drone.position[1], drone.position[0], 'D', color=drone.color,
                    markersize=12, label=f'Drone {drone.drone_id}')
            ax.text(drone.position[1], drone.position[0], str(drone.drone_id),
                    fontsize=8, ha='center', va='center', color='white', weight='bold')

        # Legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=8)

        return fig


def load_mission():
    """Load mission data"""
    mission = load_mission_data('data/missions.csv')
    if not mission:
        return None, None, None, None

    drone_starts = load_drone_starts('data/drone_starts.csv')
    if not drone_starts:
        drone_starts = [{'drone_id': 1, 'start_position': mission['start_position'], 'color': 'blue'}]

    targets = load_targets_data('data/targets.csv')
    nfz_rectangles = load_nfz_data('data/nfz.csv')
    waypoints = load_waypoints_data('data/waypoints.csv')

    return mission, drone_starts, targets, nfz_rectangles, waypoints


def initialize_simulation(mission, drone_starts, targets, nfz_rectangles, waypoints):
    """Initialize the simulation environment"""
    environment = SearchEnvironment(grid_size=mission['grid_size'])

    for target in targets:
        environment.add_target(target['position'])

    for nfz in nfz_rectangles:
        environment.add_nfz_rectangle(nfz)

    # Create drones
    drones = []
    for i, drone_config in enumerate(drone_starts):
        drone = RescueDrone(
            start_position=drone_config['start_position'],
            battery=400,
            drone_id=drone_config['drone_id'],
            color=drone_config['color']
        )

        if waypoints:
            # Split waypoints between drones
            if len(drone_starts) == 2:
                if i == 0:
                    drone_waypoints = waypoints[:len(waypoints) // 2]
                else:
                    drone_waypoints = waypoints[len(waypoints) // 2:]
            else:
                drone_waypoints = waypoints

            drone.set_waypoints(drone_waypoints)

        drones.append(drone)

    # Create navigators
    navigators = []
    for drone in drones:
        navigator = WaypointNavigator(
            grid_size=mission['grid_size'],
            start_position=drone.position,
            environment=environment,
            drone=drone
        )
        navigators.append(navigator)

    simulation = SimulationEngine(drones, environment, navigators)
    plotter = WebPlotter(grid_size=mission['grid_size'])

    return drones, environment, simulation, plotter


def main():
    st.set_page_config(page_title="Drone Mission Control", layout="wide")

    st.title("🚁 Rescue Drone Mission Control")
    st.markdown("---")

    # Initialize session state
    if 'mission_running' not in st.session_state:
        st.session_state.mission_running = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'mission_data' not in st.session_state:
        st.session_state.mission_data = None

    # Sidebar
    with st.sidebar:
        st.header("🎯 Mission Controls")

        if not st.session_state.mission_running:
            if st.button("🚀 Initialize Mission", type="primary", use_container_width=True):
                with st.spinner("Loading mission data..."):
                    mission_data = load_mission()
                    if mission_data[0] is None:
                        st.error("Failed to load mission data!")
                    else:
                        st.session_state.mission_data = mission_data
                        st.success("Mission loaded successfully!")

            if st.session_state.mission_data:
                if st.button("▶️ Start Simulation", type="secondary", use_container_width=True):
                    st.session_state.mission_running = True
                    st.session_state.current_step = 0
                    st.rerun()
        else:
            if st.button("⏹️ Stop Mission", type="secondary", use_container_width=True):
                st.session_state.mission_running = False
                st.rerun()

        st.markdown("---")
        st.header("📊 Mission Info")

        if st.session_state.mission_data:
            mission, drone_starts, targets, nfz_rectangles, waypoints = st.session_state.mission_data
            st.write(f"**Grid Size:** {mission['grid_size'][0]}x{mission['grid_size'][1]}")
            st.write(f"**Targets:** {len(targets)}")
            st.write(f"**Drones:** {len(drone_starts)}")
            st.write(f"**NFZs:** {len(nfz_rectangles)}")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎮 Live Mission View")

        if st.session_state.mission_running and st.session_state.mission_data:
            mission, drone_starts, targets, nfz_rectangles, waypoints = st.session_state.mission_data
            drones, environment, simulation, plotter = initialize_simulation(
                mission, drone_starts, targets, nfz_rectangles, waypoints
            )

            # Create placeholder for the plot
            plot_placeholder = st.empty()
            status_placeholder = st.empty()

            # Run simulation steps
            max_steps = 100
            for step in range(1, max_steps + 1):
                if not st.session_state.mission_running:
                    break

                st.session_state.current_step = step

                # Run simulation step
                should_continue = simulation.run_step()

                # Update visualization
                total_targets_found = sum(len(drone.found_targets) for drone in drones)
                total_battery = sum(drone.battery for drone in drones)

                fig = plotter.create_plot(drones, environment, step, total_targets_found, total_battery)
                plot_placeholder.pyplot(fig)
                plt.close(fig)

                # Update status
                with status_placeholder.container():
                    st.write(f"**Step {step}** | Targets Found: {total_targets_found} | Battery: {total_battery}")

                    # Drone status table
                    status_data = []
                    for drone in drones:
                        status_data.append({
                            "Drone": f"Drone {drone.drone_id}",
                            "Position": f"({drone.position[0]}, {drone.position[1]})",
                            "Battery": f"{drone.battery}",
                            "Targets": f"{len(drone.found_targets)}"
                        })

                    st.dataframe(status_data, use_container_width=True)

                # Add small delay for better visualization
                time.sleep(0.1)

                if not should_continue:
                    st.balloons()
                    st.success("🎉 Mission Completed Successfully!")
                    st.session_state.mission_running = False
                    break

            if st.session_state.current_step >= max_steps:
                st.warning("⏰ Maximum steps reached!")
                st.session_state.mission_running = False

        elif st.session_state.mission_data and not st.session_state.mission_running:
            # Show initial state
            mission, drone_starts, targets, nfz_rectangles, waypoints = st.session_state.mission_data
            drones, environment, simulation, plotter = initialize_simulation(
                mission, drone_starts, targets, nfz_rectangles, waypoints
            )

            fig = plotter.create_plot(drones, environment, 0, 0, 0)
            st.pyplot(fig)
            plt.close(fig)

            st.info("Click 'Start Simulation' to begin the mission!")

        else:
            st.info("👆 Click 'Initialize Mission' in the sidebar to get started!")

    with col2:
        st.subheader("🚁 Drone Fleet Status")

        if st.session_state.mission_data:
            mission, drone_starts, targets, nfz_rectangles, waypoints = st.session_state.mission_data

            for drone_config in drone_starts:
                with st.container():
                    st.markdown(f"### Drone {drone_config['drone_id']}")
                    st.write(f"**Start:** {drone_config['start_position']}")
                    st.write(f"**Color:** {drone_config['color']}")

                    if st.session_state.mission_running:
                        # This would show real-time status during simulation
                        st.metric("Status", "🟢 Active" if st.session_state.current_step < 100 else "🔴 Completed")
                    else:
                        st.metric("Status", "🟡 Ready")

                    st.markdown("---")

        st.subheader("📈 Mission Statistics")
        if st.session_state.mission_running:
            st.metric("Current Step", st.session_state.current_step)
            st.metric("Mission Status", "Running" if st.session_state.mission_running else "Stopped")
        else:
            st.write("Statistics will appear when mission is running...")


if __name__ == "__main__":
    main()