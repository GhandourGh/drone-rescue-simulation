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

def load_drone_starts(file_path):

    drones = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drone = {
                    'drone_id': int(row['drone_id']),
                    'start_position': (int(row['start_row']), int(row['start_col'])),
                    'color': row['color']
                }
                drones.append(drone)
            return drones
    except FileNotFoundError:
        print("❌ Drone starts file not found")
        return []

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

def load_nfz_data(file_path):
    """Load No-Fly Zone rectangles from CSV file"""
    nfz_rectangles = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nfz = {
                    'nfz_id': int(row['nfz_id']),
                    'top_left': (int(row['top_left_row']), int(row['top_left_col'])),
                    'bottom_right': (int(row['bottom_right_row']), int(row['bottom_right_col'])),
                    'type': row['type']
                }
                nfz_rectangles.append(nfz)
            return nfz_rectangles

    except FileNotFoundError:
        print("❌ NFZ file not found")
        return []
    except Exception as e:
        print(f"❌ Error reading NFZ file: {e}")
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
