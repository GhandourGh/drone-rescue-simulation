import csv

def load_mission_data(file_path):
    """
        Load mission data from a CSV file.
        This function reads the mission configuration including:
        - Where the drone starts
        - How big the search area is
        - How many targets to find
        """
    print("\n1. Loading Mission configuration data from {}".format(file_path)+ "....")

    try:
        #step 1 : open CSV file
        with open(file_path, 'r') as file:
            #step 2: create a csv reader to understand the file format
            reader = csv.DictReader(file)

            #Step 3 : Read the first row of the data(mission)
            first_row = next(reader)

            #step 4: Convert data types and prepare mission info
            mission_data = {
                'mission_id': int(first_row['mission_id']),
                'start_position': (int(first_row['start_row']), int(first_row['start_col'])),
                'grid_size': (int(first_row['grid_size']), int(first_row['grid_size'])),
                'targets_to_find': (int(first_row['targets_to_find'])),
                }

            return mission_data

    except FileNotFoundError:
        print(" ❌ Mission configuration file not found")
        return None
    except Exception as e:
        print(f"❌ ERROR reading mission file: {e}")
        return None


def load_targets_data(file_path):

    print("\nLoading targets data from {}".format(file_path)+ "....")
    targets = []

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                target = {
                    'target_id': int(row['target_id']),
                    'position': (int(row['row']), int(row['col'])),
                    'priority': (row['priority']), #high, medium, low
                }
                targets.append(target) #add to the list
            return targets

    except FileNotFoundError:
        print("❌ Mission configuration file not found")
        return []
    except Exception as e:
        print(f"❌ Error reading targets file:  {e}")
        return []



