from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_obstacles_data, load_waypoints_data
from algorithms.parallel_track import ParallelTrackSearch
from simulation.engine import SimulationEngine
from visualization.plotter import SimulationPlotter

def main():
    # Display welcome banner
    print("\n" + "🚁" * 10)
    print("Welcome to Rescue Drone")
    print("🚁" * 10)

    # Load mission configuration from CSV file
    mission = load_mission_data('data/missions.csv')

    # Check if mission data was loaded successfully
    if not mission:
        print("Mission configuration file not found")
        return

    # Display mission details
    print("\n2. Mission Initial Start:")
    print(f"   Mission ID: {mission['mission_id']}")
    print(f"   Start Position: {mission['start_position']}")
    print(f"   Grid Size: {mission['grid_size'][0]} x {mission['grid_size'][1]}")
    print(f"   Targets to find: {mission['targets_to_find']}")

    # Load targets data from CSV file
    print("\n3. 🎯 LOADING TARGETS DATA...")
    targets = load_targets_data('data/targets.csv')

    # Display all loaded targets
    if targets:
        print(f"\n   Loaded {len(targets)} targets:")
        for target in targets:
            print(f"   - Target {target['target_id']} at {target['position']}")
    else:
        print("   No targets loaded")

    # Load obstacles data from CSV file
    print("\n5. 🚧 LOADING OBSTACLES DATA...")
    obstacles = load_obstacles_data('data/obstacles.csv')

    # Display all loaded obstacles
    if obstacles:
        print(f"\n   Loaded {len(obstacles)} obstacles:")
        for obstacle in obstacles:
            print(f"   - Obstacle {obstacle['obstacle_id']} at {obstacle['position']}")
    else:
        print("   No obstacles loaded")

    print("\n6. 📍 LOADING WAYPOINTS DATA...")
    waypoints = load_waypoints_data('data/waypoints.csv')

    # Display loaded waypoints
    if waypoints:
        print(f"\n   Loaded {len(waypoints)} waypoints:")
        for waypoint in waypoints:
            print(f"   - Waypoint {waypoint['waypoint_id']} at {waypoint['position']}")
    else:
        print("   No waypoints loaded")

    # Create the simulation environment and drone
    print("\n7. BUILDING SIMULATION WORLD")
    environment = SearchEnvironment(grid_size=mission['grid_size'])

    # Place targets in environment
    for target in targets:
        environment.add_target(target['position'])

    # Place obstacles in environment
    for obstacle in obstacles:
        environment.add_obstacle(obstacle['position'])

    # Initialize rescue drone
    drone = RescueDrone(start_position=mission['start_position'], battery=200)

    if waypoints:
        drone.set_waypoints(waypoints)

    print(f"\n8. 🚁 DRONE ACTIVATED")
    print(f"   Position: {mission['start_position']}")
    print(f"   Battery: {drone.battery} units")
    if waypoints:
        print(f"   Waypoints: {len(waypoints)} assigned")

    # Final system ready message
    print("\n" + "=" * 50)
    print("SYSTEM READY FOR WAYPOINT NAVIGATION")
    print("=" * 50)

    print(f"\n9. 🧠 INITIALIZING WAYPOINT NAVIGATION")
    search_algorithm = ParallelTrackSearch(
        grid_size=mission['grid_size'],
        start_position=mission['start_position'],
        environment=environment,
        drone=drone
    )

    print(f"\n10. 🎮 INITIALIZING SIMULATION ENGINE")
    simulation = SimulationEngine(drone, environment, search_algorithm)

    # RUN SIMULATION
    print(f"\n11. 🚀 STARTING SIMULATION")
    print("    " + "=" * 30)

    plotter = SimulationPlotter(grid_size=mission['grid_size'])

    for step in range(1, 41):
        print(f"\n   Step {step}:")
        should_continue = simulation.run_step()

        plotter.plot_step(drone, environment, step)

        if not should_continue:
            print("   🛑 Simulation ended early!")
            break

        # Show current stats
        stats = simulation.get_mission_stats()
        print(f"      Targets: {stats['targets_found']} found, {stats['targets_remaining']} remaining")
        print(f"      Battery: {stats['battery_remaining']} unit/s")

    # FINAL MISSION REPORT
    print(f"\n12. 📊 MISSION COMPLETION REPORT")
    print("    " + "=" * 30)

    final_stats = simulation.get_mission_stats()
    for key, value in final_stats.items():
        print(f"    {key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()