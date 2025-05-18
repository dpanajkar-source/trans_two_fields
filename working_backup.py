import json
from jsonschema import validate, ValidationError
from config import Settings
from output_JSON import outputJSON


def log_missing_fields(input_data, mappings):
    """Log fields missing in input but present in the mappings."""
    missing_fields = []
    for old_key in mappings.keys():
        keys = old_key.split(".")
        value = input_data
        try:
            for key in keys:
                value = value.get(key, None)
            if value is None:
                missing_fields.append(old_key)
        except AttributeError:
            missing_fields.append(old_key)

    if missing_fields:
        print(f"Missing Fields: {missing_fields}")


def single_fields(input_data, mappings):
    """Extract single fields from input data."""
    output_data = {}
    for old_key, new_key in mappings.items():
        if isinstance(new_key, list):
            continue
        try:
            value = input_data.get(old_key, None)
            output_data[new_key] = value
        except AttributeError:
            output_data[new_key] = None
    return output_data


def participants_fields(input_data, mappings):
    """Extract and transform participants-related fields."""
    participants_data = {"participants": []}
    for participant in input_data.get("participants", []):
        transformed_goal = {}
        for mapping in mappings["participants"]:
            for output_key, path in mapping.items():
                if isinstance(path, list):
                    continue
                input_key = path.split('.')[-1]
                transformed_goal[output_key] = participant.get(input_key, None)

        # Handle nested 'residencyPeriods'
        transformed_participant = {"residencyPeriods": []}
        for residency in participant.get("residencyPeriods", []):
            transformed_residency = {}
            for mapping in mappings["participants"][0]["residencyPeriods"]:
                for output_key, path in mapping.items():
                    input_key = path.split('.')[-1]
                    transformed_residency[output_key] = residency.get(
                        input_key, None)
            transformed_participant["residencyPeriods"].append(
                transformed_residency)

        transformed_goal.update(transformed_participant)
        participants_data["participants"].append(transformed_goal)

    return participants_data


def portfolio_fields(input_data, mappings):
    """Extract and transform portfolio-related fields."""
    output_data = {"portfolio": []}
    for scenario in input_data.get("scenariosList", []):
        for portfolio in scenario.get("goalFeasibilityResponse", {}).get("plan", {}).get("portfoliosClient", []):
            transformed_portfolio = {"portfolio_allocs": []}
            for mapping in mappings["portfolio"][0]:
                if mapping == "version":
                    transformed_portfolio[mapping] = None
                elif mapping == "portfolio_allocs":
                    for alloc in portfolio.get("allocs", []):
                        transformed_alloc = {}
                        for alloc_mapping in mappings["portfolio"][0]["portfolio_allocs"]:
                            for output_key, path in alloc_mapping.items():
                                input_key = path.split(".")[-1]
                                transformed_alloc[output_key] = alloc.get(
                                    input_key, None)
                        transformed_portfolio["portfolio_allocs"].append(
                            transformed_alloc)
                else:
                    input_key = mappings["portfolio"][0][mapping].split(
                        '.')[-1]
                    transformed_portfolio[mapping] = portfolio.get(
                        input_key, None)
            output_data["portfolio"].append(transformed_portfolio)

    return output_data


def extract_fields(input_data, mappings, package_id, eci):
    """Extract and transform fields from input JSON based on mappings."""
    output_data = {"goal_attributes": []}
    for goal in input_data["analysisGoals"]:
        transformed_goal = {}
        for mapping in mappings["goal_attributes"]:
            for output_key, path in mapping.items():
                if isinstance(path, list):
                    input_key = path[0].split(".")
                else:
                    input_key = path.split(".")
                transformed_goal[output_key] = goal.get(input_key[-1], None)
        output_data["goal_attributes"].append(transformed_goal)

    output_data["package_id"] = package_id
    output_data["eci"] = eci
    return output_data


def validate_output(output_data, schema):
    """Validate the output JSON against the schema."""
    try:
        validate(instance=output_data, schema=schema)
    except ValidationError as e:
        print(f"Validation Error: {e.message}")
        raise


def transform_and_validate(input_data, schema, package_id, eci):
    """Main function to transform and validate JSON."""
    settings = Settings()
    mappings = settings.mapping_dictionary

    log_missing_fields(input_data, mappings)
    single_fields_dict = single_fields(input_data, mappings)
    participants_dict = participants_fields(input_data, mappings)
    portfolio_dict = portfolio_fields(input_data, mappings)
    goal_attributes_dict = extract_fields(
        input_data, mappings, package_id, eci)

    output_data = {**single_fields_dict, **participants_dict,
                   **portfolio_dict, **goal_attributes_dict}
    validate_output(output_data, schema)
    return output_data


def main_inputs(networth_response_json, input_json, mappings_new):
    """Extract required amounts from the networth_response_json and merge with input_json."""
    # Extract required amounts from the networth_response_json
    assets_amount = networth_response_json["assets"]["amount"]
    liabilities_amount = networth_response_json["liabilities"]["amount"]

    # Calculate derived values
    total_net_worth = assets_amount - liabilities_amount
    total_plan_current_assets = assets_amount
    total_plan_current_liabilities = liabilities_amount

    # Map these values to input_json
    input_json["total_net_worth"] = total_net_worth
    input_json["total_plan_current_assets"] = total_plan_current_assets
    input_json["total_plan_current_liabilities"] = total_plan_current_liabilities

    # Output JSON structure
    output_json = {}

    # Populate output_json using Settings mappings or fallback
    for key, value in input_json["data"].items():
        if key in mappings_new:
            mapped_key = mappings_new[key]
            if value is not None:
                output_json[mapped_key] = value
        else:
            # Fallback: add key directly if not mapped
            output_json[key] = value

    return output_json


def main():
    try:
        package_id = 2351371
        eci = "0449828929"

        # Load input JSON files
        with open("networth_response.json", "r") as file:
            networth_response_json = json.load(file)
        with open("CWM_Response_with_Buckets.json", "r") as file:
            input_json = json.load(file)

        # Merge and transform
        settings = Settings()
        mappings_new = settings.mappings
        merged_json = main_inputs(
            networth_response_json, input_json, mappings_new)

        # Validate and save
        output_json1 = transform_and_validate(
            merged_json, outputJSON, package_id, eci)
        with open("transformed_output.json", "w") as file:
            json.dump(output_json1, file)
        print("JSON transformation and validation complete.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
