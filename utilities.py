from operator import itemgetter
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dataclasses import dataclass

@dataclass
class TimelineEvent:
    name: str
    start: int
    end: int
    
    @property
    def duration(self) -> int:
        return self.end - self.start

def read_events_from_csv(filepath: str) -> List[TimelineEvent]:
    """Read timeline events from CSV file."""
    df = pd.read_csv(filepath)
    return [
        TimelineEvent(row['name'], row['start'], row['end']) 
        for _, row in df.iterrows()
    ]

def calculate_plot_dimensions(events: List[TimelineEvent]) -> Dict[str, int]:
    """Calculate optimal plot dimensions based on data."""
    max_name_length = max(len(event.name) for event in events)
    min_year = min(event.start for event in events)
    max_year = max(event.end for event in events)
    
    # Calculate dimensions
    height = len(events) * 0.5  # 0.5 units per event
    width = (max_year - min_year) * 0.15  # Scale factor for width
    
    # Adjust width for text labels
    text_space = max_name_length * 0.1  # Space for text labels
    
    return {
        'figsize': (width + text_space, height),
        'xlim': (min_year, max_year)
    }

def create_timeline_plot(events: List[TimelineEvent]) -> plt.Figure:
    """Create timeline visualization."""
    # Sort events by start date
    sorted_events = sorted(events, key=lambda x: x.start)
    
    # Calculate plot dimensions
    dimensions = calculate_plot_dimensions(sorted_events)
    
    # Create figure with calculated dimensions
    fig, ax = plt.subplots(figsize=dimensions['figsize'])
    
    # Create horizontal bars
    y_positions = range(len(sorted_events))
    colors = sns.color_palette("husl", len(sorted_events))
    
    bars = ax.barh(
        y_positions,
        width=[event.duration for event in sorted_events],
        left=[event.start for event in sorted_events],
        height=0.5,
        color=colors
    )
    
    # Add event labels
    for i, (bar, event) in enumerate(zip(bars, sorted_events)):
        ax.text(
            bar.get_x(), 
            bar.get_y() + bar.get_height() / 2,
            event.name,
            ha='right',
            va='center',
            fontsize=8
        )
    
    # Calculate decade lines
    start_decade = (dimensions['xlim'][0] // 10) * 10  # Round down to nearest decade
    end_decade = ((dimensions['xlim'][1] + 9) // 10) * 10  # Round up to nearest decade
    decade_lines = range(start_decade, end_decade + 10, 10)
    
    # Add vertical lines for decades
    for year in decade_lines:
        ax.axvline(x=year, color='gray', linestyle='--', alpha=0.3, zorder=0)
        ax.text(year, -0.5, str(year), ha='center', va='top', fontsize=8)
    
    # Customize plot
    ax.set_yticks([])
    ax.set_xlim(start_decade, end_decade)
    
    # Remove default grid
    ax.grid(False)
    
    plt.tight_layout()
    return fig

def save_timeline_plot(fig: plt.Figure, output_path: str, dpi: int = 300) -> None:
    """Save plot to file."""
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')from operator import itemgetter