
import re

def extract_tonnage(text):

    return {

        "vessel_name": extract(
            r"MV\s+([A-Z\s]+?)(?:\(|DWT|OPEN)",
            text,
            flags=re.I
        ),

        "open_port": extract(
            r"OPEN\s+([A-Z\s,]+?)(?:O/A|\d|$)",
            text,
            flags=re.I
        ),

        "vessel_size": extract(r"(?:DWT\s*(\d+\s?[Kk]?))|((\d+\s?[Kk]?\s?DWT))",text,flags=re.I),

        "vessel_type": (

            "Geared Bulk Carrier"
            if "GEARED BULK" in text.upper()
        
            else "Gearless Bulker"
            if "GEARLESS" in text.upper()
        
            else "Bulk Carrier"
            if "BULK" in text.upper()
        
            else "Supramax"
            if "SUPRAMAX" in text.upper()
        
            else "Ultramax"
            if "ULTRAMAX" in text.upper()
        
            else "Panamax"
            if "PANAMAX" in text.upper()
        
            else "Handysize"
            if "HANDYSIZE" in text.upper()
        
            else None
        )
    }

def extract_vc(text):

    return {

        "cargo_name": extract(
            r"mts\s+(.*?)\s+in bulk",
            text,
            flags=re.I
        ),

        "loading_port": extract(
            r"(?:LP|LOAD PORT|POL)[: ]*([^\n\r]+)",
            text,
            flags=re.I
        ),

        "discharge_port": extract(
            r"(?:DP|DISCHARGE PORT|POD)[: ]*([^\n\r]+)",
            text,
            flags=re.I
        ),

        "laycan": extract(
            r"(\d{1,2}-\d{1,2}\s+[A-Za-z]+)",
            text,
            flags=re.I
        )
    }

def extract_tc(text):
    return {
        "delivery_port": extract(r"DELIVERY\s+(.*)", text),
        "redelivery_port": extract(r"REDELIVERY\s+(.*)", text),
        "duration": extract(r"DURATION\s+(.*)", text)
    }

def extract(pattern, text, flags=0):

    match = re.search(pattern, text, flags)

    if not match:
        return None

    for group in match.groups():

        if group:
            return group.strip()

    return match.group(0).strip()