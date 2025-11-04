# Drone Rescue Simulation 🚁

A professional search and rescue drone simulation built in Python. This simulation provides a framework for testing and analyzing autonomous drone search algorithms in rescue scenarios.

## What Can This Simulation Do?

### Core Capabilities
- **Autonomous Drone Navigation**: Simulate drone movements across a grid-based search area
- **Battery Management**: Track battery consumption based on distance traveled
- **Target Detection**: Locate and prioritize multiple rescue targets
- **Mission Configuration**: Load customizable missions from CSV files
- **Path Tracking**: Record complete movement history for analysis
- **Real-time Status**: Monitor drone position, battery, and mission progress

### Current Features
✅ Grid-based search environment (configurable size)  
✅ Drone movement with battery tracking  
✅ CSV data loading for missions and targets  
✅ Target priority system (high/medium/low)  
✅ Position validation and boundary checking  
✅ Path history recording  

### Planned Features
🚧 Search algorithms (Parallel Track, Expanding Square, Random Walk)  
🚧 Obstacle detection and avoidance  
🚧 Performance metrics and analysis  
🚧 Visualization (heatmaps, path plots)  
🚧 Multiple algorithm comparison  

## Features
- Grid-based search environment
- Multiple search algorithms (planned)
- Real-time visualization (planned)
- Performance metrics (planned)

## Project Structure
```
drone_rescue/
├── models/          # Simulation classes (drone.py, environment.py)
├── utils/           # Helper functions (data_loader.py)
├── data/            # Mission data (missions.csv, targets.csv)
├── outputs/         # Results & visualizations (planned)
└── main.py          # Entry point
```

## Setup
1. Clone repository
2. Install requirements: `pip install matplotlib` (for future visualization)
3. Ensure data files exist in `data/` directory
4. Run: `python main.py`

## Usage

### Basic Usage
```bash
python main.py              # Run the simulation
python main.py --help       # Show detailed capabilities guide
python main.py --info       # Show quick information
```

### Data Files
The simulation requires two CSV files in the `data/` directory:

**missions.csv** - Mission configuration:
```csv
mission_id,start_row,start_col,grid_size,targets_to_find
1,0,0,20,5
```

**targets.csv** - Target locations:
```csv
target_id,row,col,priority
1,5,7,high
2,12,15,medium
```

## Development Status
📍 **Current Phase**: Phase 2 - Data & Integration  
✅ Phase 1: Foundation (Complete)  
🚧 Phase 2: Data & Integration (In Progress)  
⏳ Phase 3: Search Algorithms (Next)  

See `PROJECT_CHECKLIST.md` for detailed development roadmap.