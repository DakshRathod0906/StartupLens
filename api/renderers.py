from rest_framework.renderers import JSONRenderer

class StandardizedJSONRenderer(JSONRenderer):
    """
    Standardizes all API responses to follow a consistent JSON envelope:
    {
        "success": bool,
        "message": str,
        "data": dict/list,
        "errors": list
    }
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code if renderer_context else 200
        is_success = 200 <= status_code < 300
        
        # Check if the data is already in the standard envelope (e.g. from a custom view)
        if isinstance(data, dict) and 'success' in data and 'data' in data:
            response_data = data
        else:
            response_data = {
                "success": is_success,
                "message": "" if is_success else str(data.get('detail', 'An error occurred')) if isinstance(data, dict) else "",
                "data": data if is_success else None,
                "errors": data if not is_success else []
            }
            
        return super().render(response_data, accepted_media_type, renderer_context)
