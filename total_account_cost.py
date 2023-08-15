import ast
import json
import logging
import os
import time
from datetime import date, datetime, timedelta
import botocore
import boto3
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Initialize boto3 client
try:
    client = boto3.client("ce")
except Exception as e:
    logging.error("Error creating boto3 client for ce: " + str(e))
try:
    client_ssm = boto3.client("ssm")
except Exception as e:
    logging.error("Error creating boto3 client for ssm: " + str(e))
try:
    s3 = boto3.client("s3")
except Exception as e:
    logging.error("Error creating boto3 client for s3: " + str(e))


def cost_of_account(client, account_id, start_date, end_date):
    """
    Retrieves the unblended cost of a given account within a specified
    time period using the AWS Cost Explorer API.

    Args:
        client: A boto3.client object for the AWS Cost Explorer API.
        account_id: A string representing the AWS account ID to retrieve cost data for.
        start_date: A string representing the start date of the time
        period to retrieve cost data for in YYYY-MM-DD format.
        end_date: A string representing the end date of the time
        period to retrieve cost data for in YYYY-MM-DD format.

    Returns:
        A dictionary representing the response from the AWS Cost
        Explorer API, containing the unblended cost of the specified
         account for the specified time period.
    Raises:
        ValueError: If there is a problem with the input data format,
         or if the calculation fails.
    """
    try:
        response = client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="MONTHLY",
            Filter={
                "And": [
                    {
                        "Dimensions": {
                            "Key": "LINKED_ACCOUNT",
                            "Values": [account_id],
                        },
                    },
                    {
                        "Not": {
                            "CostCategories": {
                                "Key": "ChargeType",
                                "Values": ["Credit", "Refund"],
                            }
                        }
                    },
                ]
            },
            Metrics=["UnblendedCost"],
            GroupBy=[
                {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
            ],
        )
        print(response)
        return response
    except ValueError as ve:
        raise ValueError(
            f"ValueError occurred: {ve}.\nPlease check the input data format and try again."
        )
    except Exception as e:
        raise ValueError(
            f"An error occurred: {e}. Please check the input data and try again."
        )


def create_monthly_dict(json_data):
    """
    Converts AWS Cost Explorer API response data from a list
    of monthly cost data to a dictionary of monthly totals.

    Args:
        json_data: A dictionary representing the response
        data from the AWS Cost Explorer API.

    Returns:
        A dictionary where the keys are the names of the months
         in the input data (e.g. 'January', 'February', etc.),
         and the values are the total unblended cost for that month,
         calculated from the input data.
    Raises:
        KeyError: If the expected keys are not present in the input dictionary.
        ValueError: If there is a problem with the input data format,
         or if the calculation fails.
    """
    try:
        monthly_dict = {}
        for result in json_data["ResultsByTime"]:
            start_date_str = result["TimePeriod"]["Start"]
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            month_name = start_date.strftime("%B")
            if (len(result["Groups"])) == 0:
                amount = float(result["Total"]["UnblendedCost"]["Amount"])
            else:
                amount = float(
                    result["Groups"][0]["Metrics"]["UnblendedCost"]["Amount"]
                )
            if month_name in monthly_dict:
                monthly_dict[month_name] += amount
            else:
                monthly_dict[month_name] = amount
    except KeyError as ke:
        raise KeyError(
            f"KeyError occurred: {ke}. Please check the format of the input dictionary."
        )
    except ValueError as ve:
        raise ValueError(
            f"ValueError occurred: {ve}.\nPlease check the input data format and try again."
        )
    except Exception as e:
        raise ValueError(
            f"An error occurred: {e}.\nPlease check the input data and try again."
        )
    return monthly_dict


def days_passed_in_current_year():
    """
    Returns the number of days passed in the current year.
    """
    today = date.today()
    first_day_of_year = date(today.year, 1, 1)
    days_passed = (today - first_day_of_year).days
    return days_passed


def lambda_handler(event, context):
    """
    Lambda function that collects and pushes cost data to Prometheus.

    :param event: The event that triggered the Lambda function.
                Expects an account ID in the form of a dictionary.
    :param context: The context of the Lambda function. Not used in this function.
    """
    account_detail = []
    # Collect cost data for the past 90 days
    cost_by_days = days_passed_in_current_year()
    end_date = str(datetime.now().date())
    start_date = str(datetime.now().date() - timedelta(days=cost_by_days))

    # Push cost data to Prometheus
    registry = CollectorRegistry()
    g = Gauge(
        "Total_Account_Cost99",
        "Cost by month",
        ["month", "cost", "account_id"],
        registry=registry,
    )

    # # Retrieve account ID from ssm
    # parameter_name = "/" + os.environ["account_detail"] + "/account_details"
    #
    # try:
    #     response = client_ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    #     parameter_value = response["Parameter"]["Value"]
    #     # Converting SSM ListString to List
    #     account_details = ast.literal_eval(parameter_value)
    # except ValueError as ve:
    #     raise ValueError(
    #         f"ValueError occurred: {ve}.\nPlease check the input data format and try again."
    #     )
    # except Exception as e:
    #     raise ValueError(
    #         f"An error occurred: {e}. Please check the input data and try again."
    #     )

    account_monthly_dict = []

    account = boto3.client("sts", region_name="eu-west-1")
    account_id = account.get_caller_identity()['Account']

    # Check that the account ID has 12 digits
    if len(account_id) != 12 or not account_id.isdigit():
        raise ValueError("Invalid AWS account ID")

    # Getting cost details of specific account    print(registry)
    response = cost_of_account(client, account_id, start_date, end_date)
    monthly_dict = create_monthly_dict(response)
    # Add account ID and its corresponding monthly dict to the new dict
    account_monthly_dict.append(monthly_dict)
    print(account_monthly_dict, "<=======")

    for month, cost in monthly_dict.items():
        print(month, cost)
        if cost >= 0:
            g.labels(month, cost, account_id).set(cost)
        else:
            g.labels(month, 0, account_detail).set(0)

    try:
        print("here")
        push_to_gateway(
            'localhost:9091', job="Total_Account_Cost99", registry=registry
        )
        print("success")
    except Exception as e:
        raise ValueError(f"Failed to push cost data to Prometheus: {str(e)}")

    # try:
    #     # Convert the dictionary to JSON
    #     json_data = json.dumps(account_monthly_dict)
    #
    #     # # Upload the file to S3
    #     # s3.put_object(
    #     #     Bucket=os.environ["bucket_name"],
    #     #     Key=os.environ["monthly_cost_prefix"],
    #     #     Body=json_data,
    #     # )
    # except botocore.exceptions.ClientError as e:
    #     if e.response["Error"]["Code"] == "NoSuchBucket":
    #         raise ValueError(f"Bucket not found: {os.environ['bucket_name']}")
    #     elif e.response["Error"]["Code"] == "AccessDenied":
    #         raise ValueError(f"Access denied to S3 bucket: {os.environ['bucket_name']}")
    #     else:
    #         raise ValueError(f"Failed to upload data to S3 bucket: {str(e)}")
    # except Exception as e:
    #     raise ValueError(f"Failed to upload data to S3 bucket: {str(e)}")

    return {"statusCode": 200, "body": json.dumps(response)}


lambda_handler("", "")
time.sleep(10000)
