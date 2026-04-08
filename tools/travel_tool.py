"""
tools/travel_tool.py
--------------------
Travel tools for trip planning, transport suggestions, packing checklist,
and best time to visit Indian destinations.
"""

from langchain.tools import tool


@tool
def estimate_trip_budget(destination: str, days: int, people: int = 1) -> str:
    """
    Estimate a simple travel budget for an Indian destination.
    Inputs:
    - destination: destination city/place
    - days: number of travel days
    - people: number of travelers
    """
    destination = destination.strip().title()

    hotel_per_day = 1800
    food_per_day = 700
    local_transport_per_day = 500
    sightseeing_per_day = 400

    total_per_person_per_day = (
        hotel_per_day + food_per_day + local_transport_per_day + sightseeing_per_day
    )

    total_cost = total_per_person_per_day * days * people

    return (
        f"Estimated budget for a {days}-day trip to {destination} for {people} "
        f"person(s) is around ₹{total_cost:,}. "
        f"This includes stay, food, local travel, and basic sightseeing."
    )


@tool
def suggest_transport(distance_km: int) -> str:
    """
    Suggest the best mode of transport based on distance in kilometers.
    Input:
    - distance_km: travel distance in km
    """
    if distance_km <= 80:
        return (
            f"For a distance of {distance_km} km, car, cab, or bike would be convenient."
        )
    elif distance_km <= 300:
        return (
            f"For a distance of {distance_km} km, bus or car is a practical and economical option."
        )
    elif distance_km <= 700:
        return (
            f"For a distance of {distance_km} km, train is usually the best balance of comfort and cost."
        )
    else:
        return (
            f"For a distance of {distance_km} km, flight is the fastest option, "
            f"while train can be chosen if you prefer a lower-cost journey."
        )


@tool
def travel_checklist(destination: str) -> str:
    """
    Provide a general travel packing checklist for a destination.
    Input:
    - destination: destination city/place
    """
    destination = destination.strip().title()

    checklist = [
        "Valid ID cards and tickets",
        "Mobile charger and power bank",
        "Comfortable clothes and footwear",
        "Toiletries and personal medicines",
        "Water bottle and light snacks",
        "Cash and digital payment options",
        "Umbrella or cap depending on weather",
    ]

    formatted = "\n".join([f"- {item}" for item in checklist])

    return f"Here is a basic travel checklist for {destination}:\n{formatted}"


@tool
def best_time_to_visit(destination: str) -> str:
    """
    Suggest the best time to visit a destination in India.
    Input:
    - destination: destination city/place
    """
    destination_clean = destination.strip().lower()

    season_map = {
        "chennai": "The best time to visit Chennai is from November to February, when the weather is relatively pleasant.",
        "goa": "The best time to visit Goa is from November to February for beaches, sightseeing, and festivals.",
        "ooty": "The best time to visit Ooty is from October to June, especially for cool weather and scenic views.",
        "ladakh": "The best time to visit Ladakh is from May to September, when most roads and tourist routes are open.",
        "jaipur": "The best time to visit Jaipur is from October to March for comfortable sightseeing weather.",
        "munnar": "The best time to visit Munnar is from September to March for greenery and cool climate.",
    }

    if destination_clean in season_map:
        return season_map[destination_clean]

    return (
        f"The best time to visit {destination.strip().title()} is usually during the cooler "
        f"or less rainy months. It is a good idea to check local weather before finalizing your trip."
    )