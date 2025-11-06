import csv
def load_mission_data(file_path):
    """
    Load mission configuration from CSV file.
    Contains drone start position, grid size, and mission targets.
    """
    print(f"\n1. Loading mission configuration from {file_path}...")

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            first_row = next(reader)

            mission_data = {
                'mission_id': int(first_row['mission_id']),
                'start_position': (int(first_row['start_row']), int(first_row['start_col'])),
                'grid_size': (int(first_row['grid_size']), int(first_row['grid_size'])),
                'targets_to_find': int(first_row['targets_to_find'])
            }

            print(f"✅ Mission configuration loaded successfully")
            return mission_data

    except FileNotFoundError:
        print("❌ ERROR: Mission configuration file not found")
        return None
    except Exception as e:
        print(f"❌ ERROR reading mission file: {e}")
        return None


def load_targets_data(file_path):
    """
    Load target data including positions and priority levels.
    Each target has coordinates and rescue priority (high/medium/low).
    """
    print(f"\n4. Loading targets data from {file_path}...")
    targets = []

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                target = {
                    'target_id': int(row['target_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'priority': row['priority']
                }
                targets.append(target)

            print(f"✅ Successfully loaded {len(targets)} targets")
            return targets

    except FileNotFoundError:
        print("❌ ERROR: Targets file not found")
        return []
    except Exception as e:
        print(f"❌ ERROR reading targets file: {e}")
        return []


def load_obstacles_data(file_path):
    print(f"\n6. Loading obstacles data from {file_path}...")
    obstacles = []

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:

                obstacle = {
                    'obstacle_id': int(row['obstacle_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'type': row['type'],
                }
                obstacles.append(obstacle)
            print(f" Successfully loaded {len(obstacles)} obstacles")
            return obstacles

    except FileNotFoundError:
        print("❌ ERROR: obstacle file not found")
        return []
    except Exception as e:
        print(f"❌ ERROR reading obstacles file: {e}")
        return []


def load_waypoints_data(file_path):
    print(f"\n Loading waypoints data from {file_path}...")
    waypoints = []

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                waypoint = {
                    'waypoint_id': int(row['waypoint_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'priority': row['priority'],
                }
                waypoints.append(waypoint)
            print(f"✅ Successfully loaded {len(waypoints)} waypoints")
            return waypoints

    except FileNotFoundError:
        print("❌ ERROR: waypoint file not found")
        return []
    except Exception as e:
        print(f"❌ ERROR reading waypoint file: {e}")
        return []
