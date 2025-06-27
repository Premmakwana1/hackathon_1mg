"""
Decorator utility for automatic fallback handling in v2 routes.
This ensures all v2 APIs automatically fall back to mock data when they fail.
"""

import functools
from typing import Callable, Any, Optional
from sanic import Request, response
from sanic.log import logger
from app.services.fallback_service import FallbackService

def with_fallback(endpoint_name: str, fallback_method: Optional[str] = None):
    """
    Decorator that adds automatic fallback logic to v2 route handlers.
    
    Args:
        endpoint_name: Name of the endpoint for fallback lookup
        fallback_method: Specific fallback method name (optional)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                # Call the original function
                result = await func(request, *args, **kwargs)
                
                # Check if we should fallback
                if FallbackService.should_fallback(result):
                    logger.warning(f"{endpoint_name} v2 API returned empty/error, falling back to mock data")
                    
                    # Get fallback data
                    if fallback_method:
                        if fallback_method == "get_search_results_fallback":
                            # Special case for search results that need query from request body
                            body = request.json or {}
                            query = body.get('query', '')
                            fallback_data = FallbackService.get_search_results_fallback_with_query(query)
                        else:
                            fallback_data = getattr(FallbackService, fallback_method)(**kwargs)
                    else:
                        fallback_data = FallbackService.get_fallback_response(endpoint_name, **kwargs)
                    
                    # Add fallback indicator
                    if isinstance(fallback_data, dict):
                        fallback_data["_fallback"] = True
                    
                    return response.json(fallback_data)
                
                return result
                
            except Exception as e:
                logger.error(f"Error in {endpoint_name} v2 API: {str(e)}, falling back to mock data")
                
                # Get fallback data
                if fallback_method:
                    if fallback_method == "get_search_results_fallback":
                        # Special case for search results that need query from request body
                        body = request.json or {}
                        query = body.get('query', '')
                        fallback_data = FallbackService.get_search_results_fallback_with_query(query)
                    else:
                        fallback_data = getattr(FallbackService, fallback_method)(**kwargs)
                else:
                    fallback_data = FallbackService.get_fallback_response(endpoint_name, **kwargs)
                
                # Add fallback indicator
                if isinstance(fallback_data, dict):
                    fallback_data["_fallback"] = True
                
                return response.json(fallback_data)
        
        return wrapper
    return decorator

def with_step_fallback(endpoint_name: str):
    """
    Special decorator for step-based endpoints that need the step parameter.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(request: Request, step: int, *args, **kwargs):
            try:
                # Call the original function
                result = await func(request, step, *args, **kwargs)
                
                # Check if we should fallback
                if FallbackService.should_fallback(result):
                    logger.warning(f"{endpoint_name} v2 API returned empty/error for step {step}, falling back to mock data")
                    
                    # Get fallback data with step
                    fallback_method = f"get_{endpoint_name}_fallback"
                    fallback_data = getattr(FallbackService, fallback_method)(step)
                    
                    if fallback_data:
                        fallback_data["_fallback"] = True
                        return response.json(fallback_data)
                    else:
                        return response.json({"error": "Step not found"}, status=404)
                
                return result
                
            except Exception as e:
                logger.error(f"Error in {endpoint_name} v2 API for step {step}: {str(e)}, falling back to mock data")
                
                # Get fallback data with step
                fallback_method = f"get_{endpoint_name}_fallback"
                fallback_data = getattr(FallbackService, fallback_method)(step)
                
                if fallback_data:
                    fallback_data["_fallback"] = True
                    return response.json(fallback_data)
                else:
                    return response.json({"error": "Step not found"}, status=404)
        
        return wrapper
    return decorator 