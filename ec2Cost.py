import json
import boto3

from pkg_resources import resource_filename
from functools import lru_cache

region = "ap-southeast-2"
vpc_ids = ["vpc-0b33911ad08479179"]

ec2 = boto3.resource("ec2", region)
ec2_client = boto3.client("ec2", region)
price_client = boto3.client("pricing", region)


def get_price_from_pricelist(response):
    for result in response['PriceList']:
        json_result = json.loads(result)
        for json_result_level_1 in json_result['terms']['OnDemand'].values():
            for json_result_level_2 in json_result_level_1['priceDimensions'].values():
                for price_value in json_result_level_2['pricePerUnit'].values():
                    continue
    return float(price_value)


# Translate region code to region name
@lru_cache
def get_region_name(region_code):
    default_region = "EU (Ireland)"
    endpoint_file = resource_filename("botocore", "data/endpoints.json")
    try:
        with open(endpoint_file, "r") as f:
            data = json.load(f)
        return data["partitions"][0]["regions"][region_code]["description"]
    except IOError:
        return default_region


@lru_cache
def get_ec2_price(instance_type, os="Linux", region=region):
    # Search product filter
    resolved_region = get_region_name(region)
    filter = [
        {'Field': 'tenancy', 'Value': 'shared', 'Type': 'TERM_MATCH'},
        {'Field': 'operatingSystem', 'Value': os, 'Type': 'TERM_MATCH'},
        {'Field': 'preInstalledSw', 'Value': 'NA', 'Type': 'TERM_MATCH'},
        {'Field': 'instanceType', 'Value': instance_type, 'Type': 'TERM_MATCH'},
        {'Field': 'location', 'Value': resolved_region, 'Type': 'TERM_MATCH'},
        {'Field': 'capacitystatus', 'Value': 'Used', 'Type': 'TERM_MATCH'},
        {'Field': 'storage', 'Value': 'EBS only', 'Type': 'TERM_MATCH'},
        {'Field': 'marketoption', 'Value': 'OnDemand', 'Type': 'TERM_MATCH'},
        {'Field': 'licenseModel', 'Value': 'No License required', 'Type': 'TERM_MATCH'},
    ]

    response = price_client.get_products(ServiceCode="AmazonEC2", Filters=filter)
    return get_price_from_pricelist(response)


@lru_cache
def get_ebs_price(ebs_code, region=region):
    if ebs_code == 'standard':
        return 0.05  # Just hard code this, it doesn't fit the search and is rarely used

    resolved_region = get_region_name(region)
    filter = [
        {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': f"EBS:VolumeUsage.{ebs_code}"},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
    ]
    response = price_client.get_products(ServiceCode='AmazonEC2', Filters=filter)
    return get_price_from_pricelist(response)


def get_instance_price(id):
    instance = ec2.Instance(id)
    volumes = instance.volumes.all()
    vols = [(x.volume_type, int(x.size)) for x in volumes]
    instance_type = instance.instance_type
    ec2_monthly = get_ec2_price(instance_type) * 30 * 24
    total_monthly = 0 + ec2_monthly
    for vol in vols:
        vols_monthly = get_ebs_price(vol[0]) * vol[1]
    total_monthly += vols_monthly
    # print(f"{vol} - Month: ${month:.2f} Hour: ${month / (30 * 24):.2f}" )
    print(f"{total_monthly:.2f}:{id}:{vols}:{vols_monthly}:{instance_type}:{ec2_monthly}", flush=True)
    print(total_monthly)
    return total_monthly


def main():
    req = ec2_client.describe_instances()
    # print(ec2, ec2_client, price_client)
    print(req)
    for reservation in req["Reservations"]:
        print(reservation)
        for instance in reservation["Instances"]:
            id = instance["InstanceId"]
            print(get_instance_price(id))


if __name__ == "__main__":
    main()
