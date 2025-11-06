from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_nfz_data, load_waypoints_data, \
    load_drone_starts
from algorithms.waypoint import WaypointNavigator
from simulation.engine import SimulationEngine
from visualization.plotter import SimulationPlotter


def main():
    """Main application for drone waypoint navigation simulation"""
    print("\n" + "🚁" * 10)
    print("Rescue Drone Waypoint Navigation")
    print("🚁" * 10)

    # Load mission configuration
    mission = load_mission_data('data/missions.csv')
    if not mission:
        return

    print(f"\nMission: {mission['mission_id']}")
    print(f"Start: {mission['start_position']}")
    print(f"Grid: {mission['grid_size'][0]}x{mission['grid_size'][1]}")
    print(f"Targets: {mission['targets_to_find']}")

    # load drone config
    drone_starts = load_drone_starts('data/drone_starts.csv')
    if not drone_starts:
        # Fallback to single drone
        drone_starts = [{'drone_id': 1, 'start_position': mission['start_position'], 'color': 'blue'}]

    print(f"Drones: {len(drone_starts)}")
    for drone_config in drone_starts:
        print(f"  - Drone {drone_config['drone_id']}: {drone_config['start_position']} ({drone_config['color']})")

    # Load mission data
    targets = load_targets_data('data/targets.csv')
    nfz_rectangles = load_nfz_data('data/nfz.csv')
    waypoints = load_waypoints_data('data/waypoints.csv')

    print(f"\nTargets: {len(targets)} | NFZs: {len(nfz_rectangles)} | Waypoints: {len(waypoints)}")

    # Display loaded NFZs
    if nfz_rectangles:
        print(f"\nNo-Fly Zones:")
        for nfz in nfz_rectangles:
            print(f"  - NFZ {nfz['nfz_id']}: {nfz['top_left']} to {nfz['bottom_right']} ({nfz['type']})")

    # === STEP 6: CREATE DRONES (BUT USE ONLY FIRST ONE) ===
    # Initialize environment and drones
    environment = SearchEnvironment(grid_size=mission['grid_size'])

    for target in targets:
        environment.add_target(target['position'])

    for nfz in nfz_rectangles:
        environment.add_nfz_rectangle(nfz)

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
            if len(drone_starts) == 2:  # For 2 drones
                if i == 0:  # Drone 1 gets first half
                    drone_waypoints = waypoints[:len(waypoints) // 2]  # First 6 waypoints
                else:  # Drone 2 gets second half
                    drone_waypoints = waypoints[len(waypoints) // 2:]  # Last 6 waypoints
            else:
                drone_waypoints = waypoints  # Fallback for single drone

            drone.set_waypoints(drone_waypoints)
            print(f"  - Drone {drone.drone_id} assigned {len(drone_waypoints)} waypoints")

        drones.append(drone)



    # === END STEP 6 ===

    # Initialize navigation and simulation

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
    plotter = SimulationPlotter(grid_size=mission['grid_size'])

    # Execute simulation
    print(f"\n🚀 Starting Mission")
    print("=" * 30)

    for step in range(1, 201):
        print(f"\nStep {step}:")
        should_continue = simulation.run_step()
        plotter.plot_step(drones, environment, step)

        if not should_continue:
            print("Mission complete")
            break

        stats = simulation.get_mission_stats()
        print(f"  Targets: {stats['targets_found']}/{stats['targets_remaining']}")
        print(f"  Battery: {stats['battery_remaining']}")

    # Final report
    print(f"\n📊 Mission Report")
    print("=" * 30)

    final_stats = simulation.get_mission_stats()
    for key, value in final_stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")



if __name__ == "__main__":
    main()