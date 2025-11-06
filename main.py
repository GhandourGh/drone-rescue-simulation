from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_obstacles_data, load_waypoints_data
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

    # Load mission data
    targets = load_targets_data('data/targets.csv')
    obstacles = load_obstacles_data('data/obstacles.csv')
    waypoints = load_waypoints_data('data/waypoints.csv')

    print(f"\nTargets: {len(targets)} | Obstacles: {len(obstacles)} | Waypoints: {len(waypoints)}")

    # Initialize environment and drone
    environment = SearchEnvironment(grid_size=mission['grid_size'])

    for target in targets:
        environment.add_target(target['position'])

    for obstacle in obstacles:
        environment.add_obstacle(obstacle['position'])

    drone = RescueDrone(start_position=mission['start_position'], battery=200)

    if waypoints:
        drone.set_waypoints(waypoints)

    # Initialize navigation and simulation
    navigator = WaypointNavigator(
        grid_size=mission['grid_size'],
        start_position=mission['start_position'],
        environment=environment,
        drone=drone
    )

    simulation = SimulationEngine(drone, environment, navigator)
    plotter = SimulationPlotter(grid_size=mission['grid_size'])

    # Execute simulation
    print(f"\n🚀 Starting Mission")
    print("=" * 30)

    for step in range(1, 41):
        print(f"\nStep {step}:")
        should_continue = simulation.run_step()
        plotter.plot_step(drone, environment, step)

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