class SearchEnvironment:

    def __init__(self, grid_size=(10,10)):
        self.grid_size = grid_size #(rows, col)
        self.targets = [] #list of target positions
        self.obstacles = [] # list of obstacle positions


    def add_target(self, position):
        self.targets.append(position) #Add to existing list
        #example: add_target((3,4)) adds position (3,4) to targets

    def add_obstacle(self, position):
        self.obstacles.append(position)

    def is_valid_position(self, position): # check if the position is in thr GRID and not in the obstacles
        row, col = position
        rows, cols = self.grid_size

        return (0 <= row < rows and
                0 <= col < cols and
                position not in self.obstacles)

    def has_target(self, position):
        return position in self.targets #checks if position is in targets

    def remove_target(self, position):
        #Remove the target when found
        if position in self.targets:
            self.targets.remove(position)
            return True
        return False

    def get_environment_stats(self):

        return {
            'grid_size': self.grid_size,
            'targets_count': len(self.targets),
            'obstacles_count': len(self.obstacles),
            'search_area': f"{self.grid_size[0]}x{self.grid_size[1]} cells"
        }
