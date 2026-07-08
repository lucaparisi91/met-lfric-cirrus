import numpy as np
import re
import tqdm
import datetime
import argparse
from typing import List

def to_linux_ms(timestamp: str) -> int:
    """Convert to linux timestamp in microseconds"""
    dt,ms = timestamp.split('.')
    dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    return int(dt.timestamp() * 1e6) + int(ms)


def parse_event(line: str) -> dict:
    """ Parse event line from the log and return a JSON object if the string can be parsed into a valid event, otherwise return None.
    
    Args:
        line (str): A line from the log file.

    Returns:
        dict: A dictionary representing the parsed event, or None if the line is not a valid event.

    """

    m = re.match(r"(.*)-> info :(.*)", line)
    if m is not None:
        timestampString, entry = m.groups()
        timestampNs = 0

        # If entry does not start with a timestamp return None
        try:
            timestamp = to_linux_ms(timestampString)
        except Exception as e:
            
            return None
        
        # Only return events with attributes
        attributes=re.findall(r"(\S+)=(\S+)", entry)
        if len(attributes) > 0:
            label=re.sub(r"(\S+)=(\S+)", r"", entry).strip()
            return {
                    "timestamp": timestamp,
                    "label": label,
                    "attributes": dict(attributes)
            }


def get_events_from_report(report: str) -> List:
    
    """Get events from report file and return a list of events.
    
    Args:
        report (str): The path to the report file.
    Returns:
        list: A list of events parsed from the report file.
    """

    events=[]
    with open(report, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                event = parse_event(line)
                if event is not None:
                    events.append(event)
            except Exception as e:
                print(f"Error parsing line: {line.strip()} - {e}")
    return events

def get_min_timestamp(events: list) -> int:
    """Get the minimum timestamp from a list of events.
    
    Args:
        events (list): A list of events.
    Returns:
        int: The minimum timestamp found in the list of events, or None if no timestamps are found.
    """

    min_timestamp = None
    for event in events:
        if "timestamp" in event.keys():
            if min_timestamp is None or event["timestamp"] < min_timestamp:
                min_timestamp = event["timestamp"]
    return min_timestamp

def subsctract_min_timestamp(events: list) -> list:
    """Subtract the minimum timestamp from all events in the list.
    
    Args:
        events (list): A list of events.
    Returns:
        list: A new list of events with updated timestamps.
    """

    min_timestamp = get_min_timestamp(events)
    for event in events:
        if "timestamp" in event.keys():
            event["timestamp"] -= min_timestamp
    return events

def set_pid(events: list, pid: int) -> list:
    """Set the process ID (pid) for all events in the list.
    
    Args:
        events (list): A list of events.
    Returns:
        list: A new list of events with updated process IDs (pid).
    """

    for event in events:
            event["pid"] = pid
    return events


def get_events_from_reports(files: List[str], patterns : List[str]=[r"xios_server_(\d+)\.out",r"xios_client_(\d+)\.out"]) -> List[dict]:
    """Load events from all report files in a folder and return a list of events.

    Args:
        files (list): A list of report files to parse.
        patterns (list): A list of regex patterns to match the report files. Default is [r"xios_server_(\d+)\.out", r"xios_client_(\d+)\.out"].


    Returns:
        list: A list of events parsed from the report files in the folder.
    """
    
    # find all files in the form xios_server_\d+.out
    import os
    events = []
    for filename in tqdm.tqdm(files):

        match = None
        for pattern in patterns:
            if match is None:# If a match has already been found, skip the rest of the patterns
                
                match = re.match(pattern, os.path.basename(filename) )
                print(match,filename)
                if match:
                    pid = int(match.group(1)) # set pid = to the rank of the server, based on the provided pattern
                    
                    report_events = get_events_from_report(filename)
                    report_events = set_pid(report_events, pid)
                    events = events + report_events

    return events


def generate_perfetto_trace(events: list) -> dict:
    """Generate a perfetto trace from the event table.
    
    Args:
        events (list): A list of events.
    Returns:
        dict: A dictionary representing the perfetto trace.
    """

    def get_phase(phase: str) -> str:
        """Get the phase of the event.
        
        Args:
            phase (str): The phase of the event.
        Returns:
            str: The phase of the event in perfetto format.
        """
        if phase == "begin":
            return "b"
        elif phase == "end":
            return "e"
        elif phase == "next":
            return "n"
        else:
            return None
    
    trace = []
    for event in tqdm.tqdm(events):
            if "phase" in event["attributes"].keys():          
                        try:       
                            phase = get_phase(event["attributes"]["phase"])
                            
                            event_span={
                                "name": f"{event['attributes']['name']} ",
                                "cat": "event",
                                "id2" :
                                { "local": f"{event['attributes']['id']}" },
                                "ph": phase,
                                "ts": float(event["timestamp"] ),
                                "pid": event.get("pid", 0),
                                "tid": 0,
                                "args": event['attributes']
                            }
                            trace.append(event_span)
                        except Exception as e:
                            print(f"Error processing event: {event}")
                            print(f"Exception: {e}")

    perfetto_trace = {
        "traceEvents": trace,
        "displayTimeUnit": "s"
    }

    return perfetto_trace


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a perfetto trace from XIOS server logs.")
    parser.add_argument("files", type=str, nargs='+', help="xios logs")
    parser.add_argument("--output", type=str, default="trace.json", help="Output file for the perfetto trace (default: trace.json).")
    args = parser.parse_args()
    events = get_events_from_reports(args.files)

    perfetto_trace = generate_perfetto_trace(events)

    import json
    with open(args.output, 'w') as f:
        json.dump(perfetto_trace, f, indent=4)

    print(f"Perfetto trace saved to {args.output}")