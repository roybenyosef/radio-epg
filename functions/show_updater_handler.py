import os
import json
import datetime
import xml.etree.cElementTree as tree
import pytz
import boto3
from botocore.exceptions import ClientError

S3 = boto3.client('s3')


def main(event, context):
    try:

        datetime_il = get_now_il()
        day_of_the_week = datetime_il.strftime("%a")
        current_time = datetime_il.strftime("%H%M")

        response = S3.get_object(Bucket=os.environ['DATA_BUCKET_NAME'], Key='epg_data.json')
        file_content = json.loads(response['Body'].read())
        get_epg_by_time(file_content, current_time, day_of_the_week, retry=True)

    except ClientError as e:
        raise


def get_now_il() -> datetime:
    tz_il = pytz.timezone('Israel')
    return datetime.datetime.now(tz_il)


def get_epg_by_time(file_content, current_time, day_of_the_week, retry):
    try:
        for station in file_content:
            read_station_data(current_time, day_of_the_week, station, retry)

    except Exception as e:
        print(e.with_traceback())


def read_station_data(current_time, day_of_the_week, station, retry):
    epg = station.get('epg').get(day_of_the_week)
    earlier_programs = [program for program in epg if program.get('StartTime') < current_time]
    try:
        current_program = max(earlier_programs, key=lambda x: x.get('StartTime'))
        station_name = station.get("stationName")
        write_xml(station_name, current_program)
    except ValueError as e:
        handle_empty_program(station, retry)


def handle_empty_program(station, retry):
    if retry:
        previous_day = (get_now_il().today() - datetime.timedelta(1)).strftime("%a")
        read_station_data("2359", previous_day, station, retry=False)
    else:
        raise Exception("Could not find valid program, possible invalid input data")


def write_xml(station_name, program):
    root = tree.Element("track")
    tree.SubElement(root, "startTime").text = program.get('StartTime')
    tree.SubElement(root, "duration").text = program.get('Duration')
    tree.SubElement(root, "name").text = program.get('Name')
    tree.SubElement(root, "artist").text = program.get('DJ')
    tree.SubElement(root, "desc").text = program.get('Description')
    tree.SubElement(root, "image").text = program.get('Picture')
    tree_ = tree.ElementTree(root)

    xml_str = tree.tostring(tree_.getroot(), encoding='utf-8', method='xml')
    S3.put_object(Body=xml_str, Bucket=os.environ['OUT_BUCKET_NAME'], Key=f'{station_name}_epg.xml')
