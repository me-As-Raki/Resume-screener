import re

def extract_contact_details(text):
    name = ""
    email = ""
    phone = ""

    text = text.strip().replace('\r', '').replace('\t', '')
    lines = text.split('\n')

    # Extract email
    email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_matches:
        email = email_matches[0]

    # Extract phone
    phone_matches = re.findall(
        r'(?:(?:\+?\d{1,3}[-.\s]*)?(?:\(?\d{2,4}\)?[-.\s]*)?\d{3,5}[-.\s]?\d{3,5})',
        text
    )
    for p in phone_matches:
        digits = re.sub(r'\D', '', p)
        if 9 <= len(digits) <= 13:
            phone = p.strip()
            break

    # Guess name
    for line in lines:
        line_clean = line.strip()
        if (
            2 <= len(line_clean.split()) <= 4
            and not any(char.isdigit() for char in line_clean)
            and '@' not in line_clean
        ):
            name = line_clean
            break

    return name.strip(), email.strip(), phone.strip()
