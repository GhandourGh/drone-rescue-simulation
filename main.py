# Import all necessary classes and functions

from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data, load_obstacles_data


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
    print("\n4. 🚧 LOADING OBSTACLES DATA...")
    obstacles = load_obstacles_data('data/obstacles.csv')

    # Display all loaded obstacles
    if obstacles:
        print(f"\n   Loaded {len(obstacles)} obstacles:")
        for obstacle in obstacles:
            print(f"   - Obstacle {obstacle['obstacle_id']} at {obstacle['position']} (Type: {obstacle['Type']})")
    else:
        print("   No obstacles loaded")

    # Create the simulation environment and drone
    print("\n5. BUILDING SIMULATION WORLD")
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

    # Obstacle validation test
    print(f"\n6. 🧪 OBSTACLE VALIDATION TEST:")
    if obstacles:
        test_position = obstacles[0]['position']
        print(f"   Position {test_position} valid? {environment.is_valid_position(test_position)}")
        print(f"   Free position (0,1) valid? {environment.is_valid_position((0, 1))}")
    else:
        print("   No obstacles to test")

    # Initialize rescue drone
    drone = RescueDrone(start_position=mission['start_position'], battery=200)
    print(f"\n7. 🚁 DRONE ACTIVATED")
    print(f"   ✅ Position: {mission['start_position']}")
    print(f"   ✅ Battery: {drone.battery} units")

    # Final system ready message
    print("\n" + "=" * 50)
    print("SYSTEM READY FOR SEARCH OPERATIONS ✅")
    print("=" * 50)


# Standard Python practice - run main() when script is executed directly
if __name__ == "__main__":
    main()