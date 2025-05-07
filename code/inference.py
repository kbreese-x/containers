import json


def model_fn(model_dir):
    """
    Load model components needed for inference

    Args:
        model_dir: Directory where model artifacts are stored

    Returns:
        Dictionary containing loaded model components
    """
    with open(f"{model_dir}/model.txt", "r") as f:
        model = json.loads(f.read())
    return model


def input_fn(request_body, request_content_type):
    """
    Parse input data payload

    Args:
        request_body: Request body from SageMaker invocation
        request_content_type: Content type of the request

    Returns:
        Parsed input data
    """
    if request_content_type == "application/json":
        try:
            parsed = json.loads(request_body)
            if "data" not in parsed:
                raise ValueError("Missing 'data' key in input JSON")
            return parsed["data"]
        except Exception as e:
            raise e
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")


def predict_fn(input_data, model):
    """
    Perform prediction based on input data and loaded model

    Args:
        input_data: Parsed input data from input_fn
        model: Model components loaded by model_fn

    Returns:
        Simple authorization result
    """
    return {
        "your_input": input_data,
        "model_response": model.get(input_data, "No response found"),
    }


def output_fn(prediction, response_content_type):
    """
    Format prediction output

    Args:
        prediction: Result from predict_fn
        response_content_type: Desired content type of the response

    Returns:
        Formatted response
    """
    if response_content_type == "application/json":
        try:
            return json.dumps(prediction)
        except Exception as e:
            return json.dumps(
                {"authorized": False, "error": "Failed to serialize response"}
            )
    else:
        raise ValueError(f"Unsupported content type: {response_content_type}")
