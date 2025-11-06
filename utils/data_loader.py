import csv

def load_mission_data(file_path):
    """Load mission configuration from CSV file"""
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
            return mission_data

    except FileNotFoundError:
        print("❌ Mission configuration file not found")
        return None
    except Exception as e:
        print(f"❌ Error reading mission file: {e}")
        return None

def load_targets_data(file_path):
    """Load target positions from CSV file"""
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
            return targets

    except FileNotFoundError:
        print("❌ Targets file not found")
        return []
    except Exception as e:
        print(f"❌ Error reading targets file: {e}")
        return []

def load_obstacles_data(file_path):
    """Load obstacle positions from CSV file"""
    obstacles = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obstacle = {
                    'obstacle_id': int(row['obstacle_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'type': row['type']
                }
                obstacles.append(obstacle)
            return obstacles

    except FileNotFoundError:
        print("❌ Obstacles file not found")
        return []
    except Exception as e:
        print(f"❌ Error reading obstacles file: {e}")
        return []

def load_waypoints_data(file_path):
    """Load waypoint positions from CSV file"""
    waypoints = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                waypoint = {
                    'waypoint_id': int(row['waypoint_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'priority': row['priority']
                }
                waypoints.append(waypoint)
            return waypoints

    except FileNotFoundError:
        print("❌ Waypoints file not found")
        return []
    except Exception as e:
        print(f"❌ Error reading waypoints file: {e}")
        return []
