"""Command line interface for the Waze Home application."""

import click
from typing import Optional
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .config import get_location, get_config
from .waze_api import get_route, format_route_info

# Create console for rich output
console = Console()

@click.group()
def cli() -> None:
    """Waze Home - Get the fastest route between home and work."""
    pass

@cli.command()
@click.option("--from", "origin", help="Starting location (default: home)", default="home")
@click.option("--to", "destination", help="Destination location (default: work)", default="work")
def route(origin: str, destination: str) -> None:
    """Get the fastest route between two locations."""
    # Get the actual addresses from the location names
    origin_address = get_location(origin)
    destination_address = get_location(destination)
    
    if not origin_address:
        console.print(f"[bold red]Error:[/] Location '{origin}' not found. Use 'set-location' to add it.")
        sys.exit(1)
        
    if not destination_address:
        console.print(f"[bold red]Error:[/] Location '{destination}' not found. Use 'set-location' to add it.")
        sys.exit(1)
    
    with console.status(f"[bold green]Getting route from {origin} to {destination}...[/]"):
        # Get route information
        try:
            route_data = get_route(origin_address, destination_address)
            formatted_route = format_route_info(route_data)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)
    
    if formatted_route["status"] == "error":
        console.print(f"[bold red]Error:[/] {formatted_route['message']}")
        sys.exit(1)
    
    # Display route information
    summary = formatted_route["summary"]
    
    # Create summary panel
    summary_text = (
        f"[bold]From:[/] {origin} ({origin_address})\n"
        f"[bold]To:[/] {destination} ({destination_address})\n"
        f"[bold]Departure:[/] {summary['departure_time']}\n"
        f"[bold]Arrival:[/] {summary['arrival_time']}\n"
        f"[bold]Travel time:[/] {summary['total_time']}\n"
        f"[bold]Distance:[/] {summary['total_distance']}\n"
        f"[bold]Traffic:[/] {formatted_route['traffic_conditions']}"
    )
    
    console.print(Panel(summary_text, title="Route Summary", border_style="green"))
    
    # Create directions table
    directions_table = Table(box=box.ROUNDED, title="Directions", show_header=False)
    directions_table.add_column("Step", style="dim")
    directions_table.add_column("Instruction")
    
    for i, direction in enumerate(formatted_route["directions"], 1):
        directions_table.add_row(f"{i}.", direction)
    
    console.print(directions_table)
    
    # Display alternative routes if available
    if "alternate_routes" in formatted_route:
        alt_table = Table(title="Alternative Routes", box=box.SIMPLE)
        alt_table.add_column("Route")
        alt_table.add_column("Time")
        alt_table.add_column("Distance")
        
        for alt in formatted_route["alternate_routes"]:
            alt_table.add_row(alt["name"], alt["total_time"], alt["total_distance"])
        
        console.print(alt_table)

@cli.command(name="set-location")
@click.argument("name")
@click.argument("address")
def set_location_cmd(name: str, address: str) -> None:
    """Set a named location."""
    # Import locally to avoid name conflict
    from .config import set_location
    set_location(name.lower(), address)
    console.print(f"[green]Location '{name}' set to '{address}'[/]")

@cli.command(name="locations")
@click.argument("name", required=False)
def get_location_cmd(name: Optional[str] = None) -> None:
    """Get a named location or list all locations."""
    if name:
        address = get_location(name.lower())
        if address:
            console.print(f"[bold]{name}:[/] {address}")
        else:
            console.print(f"[bold red]Error:[/] Location '{name}' not found.")
            sys.exit(1)
    else:
        # List all locations
        config = get_config()
        locations = config.get("locations", {})
        
        if not locations:
            console.print("[yellow]No locations set. Use 'set-location' to add locations.[/]")
            return
        
        table = Table(title="Saved Locations")
        table.add_column("Name")
        table.add_column("Address")
        
        for name, address in locations.items():
            table.add_row(name, address)
        
        console.print(table)

@cli.command(name="home")
def go_home() -> None:
    """Get the fastest route home from your current location (work)."""
    # Direct call instead of passing to click command function
    origin_address = get_location("work")
    destination_address = get_location("home")
    
    if not origin_address:
        console.print("[bold red]Error:[/] Location 'work' not found. Use 'set-location' to add it.")
        sys.exit(1)
        
    if not destination_address:
        console.print("[bold red]Error:[/] Location 'home' not found. Use 'set-location' to add it.")
        sys.exit(1)
    
    with console.status("[bold green]Getting route from work to home...[/]"):
        try:
            route_data = get_route(origin_address, destination_address)
            formatted_route = format_route_info(route_data)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)
    
    if formatted_route["status"] == "error":
        console.print(f"[bold red]Error:[/] {formatted_route['message']}")
        sys.exit(1)
    
    # Display route information
    summary = formatted_route["summary"]
    
    # Create summary panel
    summary_text = (
        f"[bold]From:[/] work ({origin_address})\n"
        f"[bold]To:[/] home ({destination_address})\n"
        f"[bold]Departure:[/] {summary['departure_time']}\n"
        f"[bold]Arrival:[/] {summary['arrival_time']}\n"
        f"[bold]Travel time:[/] {summary['total_time']}\n"
        f"[bold]Distance:[/] {summary['total_distance']}\n"
        f"[bold]Traffic:[/] {formatted_route['traffic_conditions']}"
    )
    
    console.print(Panel(summary_text, title="Route Summary", border_style="green"))
    
    # Create directions table
    directions_table = Table(box=box.ROUNDED, title="Directions", show_header=False)
    directions_table.add_column("Step", style="dim")
    directions_table.add_column("Instruction")
    
    for i, direction in enumerate(formatted_route["directions"], 1):
        directions_table.add_row(f"{i}.", direction)
    
    console.print(directions_table)
    
    # Display alternative routes if available
    if "alternate_routes" in formatted_route:
        alt_table = Table(title="Alternative Routes", box=box.SIMPLE)
        alt_table.add_column("Route")
        alt_table.add_column("Time")
        alt_table.add_column("Distance")
        
        for alt in formatted_route["alternate_routes"]:
            alt_table.add_row(alt["name"], alt["total_time"], alt["total_distance"])
        
        console.print(alt_table)

@cli.command(name="work")
def go_to_work() -> None:
    """Get the fastest route to work from your current location (home)."""
    # Direct call instead of passing to click command function
    origin_address = get_location("home")
    destination_address = get_location("work")
    
    if not origin_address:
        console.print("[bold red]Error:[/] Location 'home' not found. Use 'set-location' to add it.")
        sys.exit(1)
        
    if not destination_address:
        console.print("[bold red]Error:[/] Location 'work' not found. Use 'set-location' to add it.")
        sys.exit(1)
    
    with console.status("[bold green]Getting route from home to work...[/]"):
        try:
            route_data = get_route(origin_address, destination_address)
            formatted_route = format_route_info(route_data)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)
    
    if formatted_route["status"] == "error":
        console.print(f"[bold red]Error:[/] {formatted_route['message']}")
        sys.exit(1)
    
    # Display route information
    summary = formatted_route["summary"]
    
    # Create summary panel
    summary_text = (
        f"[bold]From:[/] home ({origin_address})\n"
        f"[bold]To:[/] work ({destination_address})\n"
        f"[bold]Departure:[/] {summary['departure_time']}\n"
        f"[bold]Arrival:[/] {summary['arrival_time']}\n"
        f"[bold]Travel time:[/] {summary['total_time']}\n"
        f"[bold]Distance:[/] {summary['total_distance']}\n"
        f"[bold]Traffic:[/] {formatted_route['traffic_conditions']}"
    )
    
    console.print(Panel(summary_text, title="Route Summary", border_style="green"))
    
    # Create directions table
    directions_table = Table(box=box.ROUNDED, title="Directions", show_header=False)
    directions_table.add_column("Step", style="dim")
    directions_table.add_column("Instruction")
    
    for i, direction in enumerate(formatted_route["directions"], 1):
        directions_table.add_row(f"{i}.", direction)
    
    console.print(directions_table)
    
    # Display alternative routes if available
    if "alternate_routes" in formatted_route:
        alt_table = Table(title="Alternative Routes", box=box.SIMPLE)
        alt_table.add_column("Route")
        alt_table.add_column("Time")
        alt_table.add_column("Distance")
        
        for alt in formatted_route["alternate_routes"]:
            alt_table.add_row(alt["name"], alt["total_time"], alt["total_distance"])
        
        console.print(alt_table)

if __name__ == "__main__":
    cli()