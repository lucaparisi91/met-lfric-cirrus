import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from dataclasses import dataclass


test_file="/work/z62/z62/lparisiz62/lfric/met-lfric-cirrus/runs/nodes192_ppn8_meshC1536_cray_pat_mpi/report.txt"

@dataclass
class dataLine:
    """ Entry containing data found on a line
    """
    level: float
    time: float
    calls: float
    name: list[str]


def parse_section_closure(line: str) -> bool:
    """
    Check if a line indicates the closure of a section in the Cray PAT report.
    A section closure line typically contains pipes followed by dashes, e.g.: ||------

    Args:
        line: A single line from the report file.
    Returns:
        level: The level of the section closed, determined by the number of pipes.
        If the line does not indicate a section closure, returns None.
    """
    
    closure_pattern = r'^(\|+)\-+\s*$'
    closure_match= re.match(closure_pattern, line)
    if closure_match is not None:
        level=len(closure_match.group(1)) # The number of pipes indicates the level
        return level - 1
    

class CallstackNode:
    def __init__(self,name):
        self.name = name
        self.parent = None
        self.children = {}
        self.level = 0
    def attach(self,parent):
        if self.parent is not None:
            # Invalid state
            raise ValueError("Node already has a parent. Each node can only have one parent.")
        
        self.parent = parent
        self.parent.children[self.name] = self
        self.level = parent.level + 1
    
    def get_parent_at_level(self,level):

        """ Get the ancestor node at a specific level."""
        node=self
        
        assert node.level >= level, f"Current node level is already less than target level. {level}"


        while node.level > level:
            node=node.parent
        return node
    

    def __getitem__(self, key):
        return self.children[key]
    
    def keys(self):
        return self.children.keys()
        
    def __repr__(self):
        children_names = ', '.join(self.children.keys())
        description=f"<name={self.name},level={self.level} -> {children_names} > "

        return description

    
    




def parse_data_line(line: str) -> dataLine:
    """
    Parse a line of the Cray PAT report to extract data.
    Lines parsed are of same format as the example below:
    5||||   0.4% |   0.716426 |   9,468.0 | __sci_psykal_light_mod_MOD_invoke_rdouble_x_innerproduct_x

    Args:
        line: A single line from the report file.
    Returns:
        dataLine object with parsed values.

    """

    data_line_pattern = r'^(?:(\d*)(\|+) )?\s*(?:([\d.]+)%)*\s+\|\s+(?:([\d.]+))*\s+\|\s+([\d,]+\.\d+)*\s+\|\s+(.+?)\s*$'
    is_data_line = re.match(data_line_pattern, line)
    if is_data_line:
        # Extract level. This is equal to the digit at the start of the line plus the number of pipes the line starts with.
        
        level=0

        if is_data_line.group(1):
            level = int(is_data_line.group(1) )
        else:
            pipes=is_data_line.group(2)

            if pipes:
                level = level  + len(pipes)
        
        time = float(is_data_line.group(4)) if is_data_line.group(4) else None
        calls = float(is_data_line.group(5).replace(',', '')) if is_data_line.group(5) else None
        name = is_data_line.group(6).strip()

        return dataLine(level=level, time=time, calls=calls, name=name)
    else:
        return None


def extract_mpi_callstack_data(report_file):
    """
    Extract MPI function timing data with callstack information from a Cray PAT report.
    """

    data=[]
    max_lines= None
    root=None

    with open(report_file, 'r') as f:
        for i_line, line in enumerate(f):
            
            line=line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
           # Stop if maximum lines reached
            if max_lines is not None and i_line >= max_lines:
                break
            
            # extract data from line
            data_line = parse_data_line(line)
            if data_line is not None:
                if not data_line.name.startswith("pe"):
                        if data_line.level == 0:
                           root= CallstackNode(data_line.name)
                           current_node=root
                        else:
                           current_node=current_node.get_parent_at_level(data_line.level -1)
                           child = CallstackNode(data_line.name)
                           child.attach(current_node)
                           current_node=child



                           

            # Check for section closure
            closure_level = parse_section_closure(line)
            if closure_level is not None:
                pass
                #print(f"Section closed at level {closure_level}")
                            
    print(f"Callstack Structure: {root.children['MPI'].children['MPI_Waitall']}")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


# Parse the report
df = extract_mpi_callstack_data(test_file)

# Display results
print(f"\nExtracted {len(df)} MPI callstack entries")
print(f"\nSample data:")
print(df.head(20))
