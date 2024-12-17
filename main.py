from utilities import (
    read_events_from_csv, 
    create_timeline_plot, 
    save_timeline_plot
)

def main(input_csv: str, output_path: str) -> None:
    """Main function to create and save timeline visualization."""
    events = read_events_from_csv(input_csv)
    fig = create_timeline_plot(events)
    save_timeline_plot(fig, output_path)

if __name__ == "__main__":
    main("scientists.csv", "timeline.png")