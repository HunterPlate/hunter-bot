import re


def clean_plates(plates: str) -> str:
    return re.sub(r'[-\/*@ %$#&?()+=]', '', plates)

def verify_plates(plates: str) -> bool:
    if re.match(r'^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$', plates) and len(plates) == 7:
        return True
    return False