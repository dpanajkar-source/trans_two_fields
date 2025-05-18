import pytest
from unittest.mock import patch
import json

# Assuming the functions have been imported, for example:
# from your_module import log_missing_fields, single_fields, participants_fields, portfolio_fields, extract_fields, transform_and_validate, main_inputs

# Test case for missing fields logging


def test_log_missing_fields():
    with patch("builtins.print") as mock_print:
        log_missing_fields(input_json, Settings().mapping_dictionary)
        mock_print.assert_called_with(
            "Missing Fields: []")  # No missing fields

# Test case for extracting single fields


def test_single_fields():
    output_data = single_fields(input_json, Settings().mapping_dictionary)
    assert output_data["goal_name_mapped"] == "Retirement"
    assert output_data["goal_amount_mapped"] == 500000

# Test case for participants field extraction (no participants in our mock, so test with empty data)


def test_participants_fields():
    input_data = {
        "participants": []  # Empty list
    }
    mappings = {"participants": [{"name": "name_mapped"}]}
    output_data = participants_fields(input_data, mappings)
    assert output_data["participants"] == []  # No participants in the output

# Test case for portfolio field extraction (mocked)


def test_portfolio_fields():
    input_data = {
        "scenariosList": [
            {
                "goalFeasibilityResponse": {
                    "plan": {
                        "portfoliosClient": [
                            {"allocs": [
                                {"type": "stock", "value": 1000}], "version": "v1"}
                        ]
                    }
                }
            }
        ]
    }
    mappings = {
        "portfolio": [
            {"version": "version", "portfolio_allocs": [
                {"type": "alloc_type", "value": "alloc_value"}]}
        ]
    }
    output_data = portfolio_fields(input_data, mappings)
    assert len(output_data["portfolio"]) == 1  # One portfolio entry
    assert output_data["portfolio"][0]["portfolio_allocs"][0]["alloc_type"] == "stock"
    assert output_data["portfolio"][0]["portfolio_allocs"][0]["alloc_value"] == 1000

# Test case for extracting goal attributes


def test_extract_fields():
    output_data = extract_fields(
        input_json, Settings().mapping_dictionary, 2351371, "0449828929")
    assert "goal_attributes" in output_data
    assert len(output_data["goal_attributes"]) == 1  # One goal attribute
    assert output_data["goal_attributes"][0]["goal_name_mapped"] == "Retirement"

# Test case for main_inputs function (integrating networth_response_json and input_json)


def test_main_inputs():
    mappings_new = Settings().mapping_dictionary
    output_json = main_inputs(networth_response_json, input_json, mappings_new)
    assert output_json["goal_name_mapped"] == "Retirement"
    assert output_json["goal_amount_mapped"] == 500000
    assert output_json["total_net_worth"] == 50000
    assert output_json["total_plan_current_assets"] == 100000
    assert output_json["total_plan_current_liabilities"] == 50000

# Test case for transform_and_validate function (testing full flow)


def test_transform_and_validate():
    schema = {
        "type": "object",
        "properties": {
            "goal_name_mapped": {"type": "string"},
            "goal_amount_mapped": {"type": "number"},
            "total_net_worth": {"type": "number"}
        },
        "required": ["goal_name_mapped", "goal_amount_mapped", "total_net_worth"]
    }

    # Use the same output from main_inputs
    output_data = transform_and_validate(
        output_json, schema, 2351371, "0449828929")
    assert output_data["goal_name_mapped"] == "Retirement"
    assert output_data["total_net_worth"] == 50000  # Derived value
    assert "goal_attributes" in output_data

# Test edge case with missing required fields (e.g., missing 'assets.amount')


def test_edge_case_missing_field():
    input_data = {"assets": {}, "liabilities": {
        "amount": 50000}}  # Missing 'amount' in assets
    output_data = main_inputs(networth_response_json,
                              input_data, Settings().mapping_dictionary)
    # No total_net_worth as assets are incomplete
    assert "total_net_worth" not in output_data
    # Similarly, missing assets amount
    assert "total_plan_current_assets" not in output_data
