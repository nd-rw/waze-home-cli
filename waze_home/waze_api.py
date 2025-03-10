"""Module for interacting with the Waze API."""

import requests
from typing import Dict, Any, List, Tuple, Optional
import json
from datetime import datetime, timedelta
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Waze API details
# Note: This is using the public Waze API endpoints that might change
WAZE_URL = "https://www.waze.com/live-map/api/routing"

def _get_coordinates_from_address(address: str) -> Tuple[float, float]:
    """
    Convert an address to coordinates using a geocoding service.
    
    For simplicity, this function uses a mock implementation.
    In a real application, you would use a geocoding service like Google Maps, Nominatim, etc.
    
    Args:
        address: Street address
        
    Returns:
        Tuple of (latitude, longitude)
    """
    # This is a mock implementation
    # In a real application, you would make an API call to a geocoding service
    # For the provided addresses, we're using approximate coordinates
    
    # Mock geocoding database based on our known addresses
    geocode_db = {
        "91 Abbett St, Scarborough WA 6019": (-31.8941, 115.7586),  # Example coordinates
        "11 Mount St, Perth WA 6000": (-31.9523, 115.8613),  # Example coordinates
    }
    
    # Return coordinates if address is in our mock database
    if address in geocode_db:
        return geocode_db[address]
        
    # For unknown addresses, log a warning and return fake coordinates
    logger.warning(f"Address not found in geocoding database: {address}")
    # Return default coordinates (Perth, Australia area)
    return (-31.9505, 115.8605)

def get_route(origin: str, destination: str) -> Dict[str, Any]:
    """
    Get the route information between two locations.
    
    Args:
        origin: Starting address
        destination: Ending address
        
    Returns:
        Dictionary with route information
    """
    # Get coordinates for origin and destination
    origin_coords = _get_coordinates_from_address(origin)
    destination_coords = _get_coordinates_from_address(destination)
    
    logger.info(f"Requesting route from {origin} to {destination}")
    
    try:
        # Prepare the request parameters
        params = {
            "from": f"ll:{origin_coords[0]},{origin_coords[1]};na:{origin}",
            "to": f"ll:{destination_coords[0]},{destination_coords[1]};na:{destination}",
            "at": int(time.time() * 1000),  # Current time in milliseconds
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": 3,
            "options": "AVOID_TRAILS:t,ALLOW_UTURNS:t"
        }
        
        # Make the request to the Waze API
        # In a real implementation, you would make an actual API call:
        # response = requests.get(WAZE_URL, params=params)
        # route_data = response.json()
        
        # For this implementation, we'll return mock data
        route_data = _get_mock_route_data(origin, destination)
        
        return route_data
        
    except Exception as e:
        logger.error(f"Error getting route: {str(e)}")
        raise RuntimeError(f"Failed to get route information: {str(e)}")

def _get_mock_route_data(origin: str, destination: str) -> Dict[str, Any]:
    """
    Generate mock route data for demonstration purposes.
    
    Args:
        origin: Starting address
        destination: Ending address
        
    Returns:
        Mock route data
    """
    # Calculate a realistic travel time based on the addresses
    # For our specific locations in Perth, Australia
    if (origin == "91 Abbett St, Scarborough WA 6019" and 
        destination == "11 Mount St, Perth WA 6000"):
        # Morning commute to work (more traffic)
        travel_time_minutes = 25
        distance_meters = 14200
    elif (origin == "11 Mount St, Perth WA 6000" and 
          destination == "91 Abbett St, Scarborough WA 6019"):
        # Evening commute home
        travel_time_minutes = 22
        distance_meters = 14200
    else:
        # Generic calculation for unknown routes
        travel_time_minutes = 20
        distance_meters = 12000
    
    # Current time plus travel time
    current_time = datetime.now()
    arrival_time = current_time + timedelta(minutes=travel_time_minutes)
    
    # Generate directions
    if origin == "91 Abbett St, Scarborough WA 6019" and destination == "11 Mount St, Perth WA 6000":
        directions = [
            "Head south on Abbett St toward Brighton Rd",
            "Turn right onto Scarborough Beach Rd",
            "Turn left onto West Coast Hwy",
            "Continue onto Mounts Bay Rd",
            "Turn right onto Mount St",
            "Arrive at destination on left"
        ]
    elif origin == "11 Mount St, Perth WA 6000" and destination == "91 Abbett St, Scarborough WA 6019":
        directions = [
            "Head north on Mount St toward St Georges Terrace",
            "Turn left onto Mounts Bay Rd",
            "Continue onto West Coast Hwy",
            "Turn right onto Scarborough Beach Rd",
            "Turn left onto Abbett St",
            "Arrive at destination on right"
        ]
    else:
        directions = [
            "Start driving",
            "Continue straight",
            "Turn at the intersection",
            "Keep going",
            "Arrive at destination"
        ]
    
    # Create mock route data
    return {
        "routes": [
            {
                "summary": {
                    "totalLength": distance_meters,
                    "totalTime": travel_time_minutes * 60,  # In seconds
                    "arrivalTime": arrival_time.strftime("%H:%M"),
                    "departureTime": current_time.strftime("%H:%M"),
                },
                "directions": directions,
                "traffic_conditions": "Light to moderate traffic",
                "alternate_routes": [
                    {
                        "name": "Alternative via Mitchell Freeway",
                        "total_time": (travel_time_minutes + 5) * 60,
                        "total_distance": distance_meters + 2000,
                    },
                    {
                        "name": "Alternative via inland roads",
                        "total_time": (travel_time_minutes + 8) * 60,
                        "total_distance": distance_meters - 1000,
                    }
                ]
            }
        ]
    }

def format_route_info(route_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the route data into a more readable format.
    
    Args:
        route_data: Raw route data from the API
        
    Returns:
        Formatted route information
    """
    if not route_data or "routes" not in route_data or not route_data["routes"]:
        return {
            "status": "error",
            "message": "No route found"
        }
    
    route = route_data["routes"][0]
    
    formatted_info = {
        "status": "success",
        "summary": {
            "total_time": f"{route['summary']['totalTime'] // 60} minutes",
            "total_distance": f"{route['summary']['totalLength'] / 1000:.1f} km",
            "departure_time": route['summary']['departureTime'],
            "arrival_time": route['summary']['arrivalTime'],
        },
        "directions": route["directions"],
        "traffic_conditions": route.get("traffic_conditions", "Unknown"),
    }
    
    # Add alternative routes if available
    if "alternate_routes" in route:
        alt_routes = []
        for alt in route["alternate_routes"]:
            alt_routes.append({
                "name": alt["name"],
                "total_time": f"{alt['total_time'] // 60} minutes",
                "total_distance": f"{alt['total_distance'] / 1000:.1f} km",
            })
        formatted_info["alternate_routes"] = alt_routes
    
    return formatted_info