import numpy as np

def fetch_freight_cost(route):
    """
    Simulate fetching freight cost data for a given route.
    
    This function uses a base freight cost per route and adds a random variation
    to simulate realistic freight cost fluctuations.
    
    Args:
        route (str): The shipping route identifier (e.g., "Route A").
        
    Returns:
        dict: A dictionary with simulated freight cost information.
    """
    base_costs = {
        "Route A": 15.5,
        "Route B": 18.2,
        "Route C": 12.8,
        "Route D": 20.0
    }
    
    base_cost = base_costs.get(route, 17.0)
    
    variation = np.random.uniform(-0.1, 0.1) * base_cost
    simulated_cost = base_cost + variation
    
    simulated_cost = round(simulated_cost, 2)
    
    return {"freight_cost": simulated_cost, "currency": "USD"}

if __name__ == "__main__":
    print(fetch_freight_cost("Route A"))