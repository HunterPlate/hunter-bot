import re


def clean_plates(plates: str) -> str:
    if re.match(r'[-\/*@ %$#&?]', plates):
        plates = plates.replace('-', '').replace('@', '').replace('%', '').replace('$', '').replace('#', '').replace('&', '').replace('?', '')
    return plates

def verify_plates(plates: str) -> bool:
    re.match(r'^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$', plates)
    return True