# Import all necessary classes and functions
from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data


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
    print("\n""2. Mission Initial Start: ")
    print(f" Mission ID: {mission['mission_id']}")  # Unique mission id
    print(f" Start Position: {mission['start_position']}")  # Where drone begins
    print(f"️ Grid Size: {mission['grid_size'][0]} x {mission['grid_size'][1]}")  # Search area dimensions
    print(f" Targets to find: {mission['targets_to_find']}")  # Number of people to rescue

    # Load targets data from CSV file
    print("\n3. 🎯 LOADING TARGETS DATA...:")
    targets = load_targets_data('data/targets.csv')

    # Display all loaded targets
    if targets:
        print(f"\n Loaded {len(targets)} targets 🎯: \n")
        for target in targets:
            # Show each target's ID, position, and priority level
            print(f" - Target {target['target_id']} at {target['position']} (priority: {target['priority']})")
    else:
        print("No targets loaded")  # Error message if no targets

    # Create the simulation environment and drone
    print("\n4. BUILDING SIMULATION WORLD")
    environment = SearchEnvironment(grid_size=mission['grid_size'])  # Create search area with mission grid size
    for target in targets:
        environment.add_target(target['position'])  # Place each target in the environment
    print(f"✅ Created {mission['grid_size'][0]} x {mission['grid_size'][1]} search area")
    print(f"✅ Placed {len(targets)} targets in environment")

    drone = RescueDrone(start_position=mission['start_position'], battery=200)  # Create drone at start position
    print(f"✅ Drone activated at position {mission['start_position']}")
    print(f"✅ Drone battery: {drone.battery} units")  # Show initial battery level

    # Final system ready message
    print("\n" + "=" * 50)
    print("SYSTEM READY!! ✅")  # All components loaded and integrated
    print("=" * 50)


# Standard Python practice - run main() when script is executed directly
if __name__ == "__main__":
    main()