from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_obstacles_data
from algorithms.parallel_track import ParallelTrackSearch
from simulation.engine import SimulationEngine
from visualization.plotter import SimulationPlotter

def main():
    # Display welcome banner
    print("\n" + "🚁" * 10)
    print("Welcome to Rescue Drone!! ")
    print("🚁" * 10)

    # Load mission configuration from CSV file
    mission = load_mission_data('data/missions.csv')

    # Check if mission data was loaded successfully
    if not mission:
        print("Mission configuration file not found")
        return  # Exit if no mission data

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
        print(f"\n   Loaded {len(targets)} targets 🎯:")
        for target in targets:
            print(f"   - Target {target['target_id']} at {target['position']} (priority: {target['priority']})")
    else:
        print("   No targets loaded")

    # Load obstacles data from CSV file
    print("\n5. 🚧 LOADING OBSTACLES DATA...")
    obstacles = load_obstacles_data('data/obstacles.csv')

    # Display all loaded obstacles
    if obstacles:
        print(f"\n   Loaded {len(obstacles)} obstacles:")
        for obstacle in obstacles:
            print(f"   - Obstacle {obstacle['obstacle_id']} at {obstacle['position']} (Type: {obstacle['type']})")
    else:
        print("   No obstacles loaded")

    # Create the simulation environment and drone
    print("\n7. BUILDING SIMULATION WORLD")
    environment = SearchEnvironment(grid_size=mission['grid_size'])

    # Place targets in environment
    for target in targets:
        environment.add_target(target['position'])
    print(f"   ✅ Created {mission['grid_size'][0]} x {mission['grid_size'][1]} search area")
    print(f"   ✅ Placed {len(targets)} targets in environment")

    # Place obstacles in environment
    for obstacle in obstacles:
        environment.add_obstacle(obstacle['position'])
    print(f"   ✅ Placed {len(obstacles)} obstacles in environment")

    # Initialize rescue drone
    drone = RescueDrone(start_position=mission['start_position'], battery=200)
    print(f"\n8. 🚁 DRONE ACTIVATED")
    print(f"   ✅ Position: {mission['start_position']}")
    print(f"   ✅ Battery: {drone.battery} units")

    # Final system ready message
    print("\n" + "=" * 50)
    print("SYSTEM READY FOR SEARCH OPERATIONS ✅")
    print("=" * 50)

    print(f"\n9. 🧠 INITIALIZING SEARCH ALGORITHM")
    search_algorithm = ParallelTrackSearch(
        grid_size=mission['grid_size'],
        start_position=mission['start_position'],
        environment=environment  # CRITICAL: Pass environment for obstacle awareness
    )
    print(f"   ✅ Parallel Track search initialized (Obstacle-Aware)")

    print(f"\n10. 🎮 INITIALIZING SIMULATION ENGINE")
    simulation = SimulationEngine(drone, environment, search_algorithm)
    print(f"    ✅ Simulation engine ready")

    # RUN SIMULATION FOR 20 STEPS
    print(f"\n11. 🚀 STARTING SIMULATION")
    print("    " + "=" * 30)

    plotter = SimulationPlotter(grid_size=mission['grid_size'])

    for step in range(1, 54):  # Run 53 steps for demo
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


# Standard Python practice - run main() when script is executed directly
if __name__ == "__main__":
    main()