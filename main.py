# Import all necessary classes and functions
import argparse
import sys
from models.drone import RescueDrone
from models.environment import SearchEnvironment
from utils.data_loader import load_mission_data, load_targets_data


def show_help():
    """Display detailed help information about the simulation capabilities"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║         DRONE RESCUE SIMULATION - CAPABILITIES GUIDE          ║
╚════════════════════════════════════════════════════════════════╝

🚁 WHAT CAN THIS SIMULATION DO?

1. DRONE OPERATIONS:
   ✓ Autonomous navigation across a grid-based search area
   ✓ Battery management and consumption tracking
   ✓ Position tracking and path history recording
   ✓ Target scanning and detection capabilities
   ✓ Real-time status reporting

2. SEARCH ENVIRONMENT:
   ✓ Configurable grid-based search areas
   ✓ Target placement and management
   ✓ Obstacle detection and avoidance (coming soon)
   ✓ Position validation within boundaries
   ✓ Multi-target tracking system

3. MISSION MANAGEMENT:
   ✓ CSV-based mission configuration loading
   ✓ Customizable grid sizes
   ✓ Flexible start positions
   ✓ Target priority system (high/medium/low)
   ✓ Multiple targets support

4. DATA & ANALYSIS:
   ✓ Mission data import from CSV files
   ✓ Target location configuration
   ✓ Performance metrics tracking
   ✓ Path history visualization (planned)
   ✓ Search efficiency analysis (planned)

5. SEARCH ALGORITHMS (PLANNED):
   • Parallel Track (Lawnmower pattern)
   • Expanding Square (Spiral search)
   • Random Walk (Baseline comparison)
   • Custom algorithm support

📁 REQUIRED DATA FILES:
   • data/missions.csv  - Mission configurations
   • data/targets.csv   - Target locations and priorities

🎮 USAGE:
   python main.py              - Run simulation
   python main.py --help       - Show this help
   python main.py --info       - Show quick capabilities
   python main.py --demo       - Run demo mission (future)

🔧 CURRENT PHASE: Phase 2 - Data & Integration
   ✅ Foundation complete
   🚧 Working on CSV data loaders and integration
   ⏳ Search algorithms coming next

📖 For more information, see README.MD and PROJECT_CHECKLIST.md
"""
    print(help_text)


def show_info():
    """Display quick information about what the simulation can do"""
    info_text = """
🚁 DRONE RESCUE SIMULATION - Quick Info

What can I do?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Simulate autonomous drone search & rescue operations
✓ Navigate drones across configurable grid-based search areas
✓ Manage battery consumption and track drone movements
✓ Load mission configurations from CSV files
✓ Track and locate multiple targets with priority levels
✓ Monitor real-time drone status and performance
✓ Provide foundation for search algorithm testing

Current Status: Foundation Complete ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run with --help for detailed capabilities guide.
"""
    print(info_text)


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
    print("\n2. Mission Initial Start: ")
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
    # Set up argument parser for command-line options
    parser = argparse.ArgumentParser(
        description='Drone Rescue Simulation - Search and Rescue Operations',
        add_help=False  # We'll use custom help
    )
    parser.add_argument('--help', '-h', action='store_true',
                        help='Show detailed help and capabilities')
    parser.add_argument('--info', '-i', action='store_true',
                        help='Show quick information about capabilities')
    
    args = parser.parse_args()
    
    # Handle command-line arguments
    if args.help:
        show_help()
        sys.exit(0)
    elif args.info:
        show_info()
        sys.exit(0)
    else:
        main()