from fastapi import HTTPException, FastAPI
from firebase_functions import https_fn
import json 
import inspect

def router(req: https_fn.Request, app: FastAPI, debug: bool = False) -> https_fn.Response:
    path = req.path.rstrip("/")
    matched_route = None

    for route in app.routes:
        if debug:
            print("Requested Path:", path)
            print("Route Path:", route.path)
        
        if route.path.rstrip("/") == path:
            matched_route = route
            break

    if matched_route:
        endpoint_function = matched_route.endpoint.__call__
        request_data = json.loads(req.data.decode("utf-8")) if req.data else {}
        parameters = {}
        query_params = {}
        if "?" in req.full_path:
            query_string = req.full_path.split("?")[1]
            query_params = dict(q.split("=") for q in query_string.split("&") if '=' in q)
        else:
            query_params = {}

        if debug:
            print("Extracted Query Parameters:", query_params)
            print("Request Data:", request_data)
        
        for parameter in inspect.signature(endpoint_function).parameters.values():
            if parameter.name != "req":
                if parameter.kind == parameter.VAR_POSITIONAL:
                    parameters.update(request_data)
                elif parameter.kind == parameter.VAR_KEYWORD:
                    parameters.update(request_data)
                elif parameter.name in query_params:
                    parameters[parameter.name] = query_params.get(parameter.name)
                else:
                    parameters[parameter.name] = request_data.get(parameter.name)
        parameters.update(request_data)
        parameters.update(query_params)

        if debug:
            print("Extracted Parameters:", parameters)
            print("Request Data:", request_data)

        try:
            response = endpoint_function(**parameters)

            return https_fn.Response(
                json.dumps(response), 
                status=200, 
                content_type="application/json", 
                headers={"Access-Control-Allow-Credentials": "true"}
            )
        except HTTPException as e:
            return https_fn.Response(
                json.dumps({"error": str(e.detail)}),
                status=e.status_code,
                content_type="application/json",
            )
        except Exception as e:
            return https_fn.Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )
    else:
        return https_fn.Response(
            json.dumps({"error": "Route not found"}),
            status=404,
            content_type="application/json",
        )
