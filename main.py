import csv
import re

with open('phonebook_raw.csv', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_pattern = re.compile(r'(\+?7|8)\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s*\(доб\.\s*(\d+)\))?')


def format_phone_number(phone):
    match = phone_pattern.search(phone)
    if not match:
        return ""
    formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(6):
        formatted_phone += f" доб.{match.group(7).strip()}"
    return formatted_phone


def process_contacts(contacts):
    formatted_contacts = []
    contact_dict = {}

    for contact in contacts[1:]:
        full_name = " ".join(contact[:3]).split()
        if len(full_name) < 3:
            full_name += [""] * (3 - len(full_name))

        key = (full_name[0], full_name[1])

        if key not in contact_dict:
            contact_dict[key] = {
                'lastname': full_name[0],
                'firstname': full_name[1],
                'surname': full_name[2],
                'organization': contact[3],
                'position': contact[4],
                'phone': format_phone_number(contact[5]),
                'email': contact[6]
            }
        else:
            existing_contact = contact_dict[key]
            if not existing_contact['surname'] and full_name[2]:
                existing_contact['surname'] = full_name[2]
            if not existing_contact['organization']:
                existing_contact['organization'] = contact[3]
            if not existing_contact['position']:
                existing_contact['position'] = contact[4]
            if not existing_contact['phone']:
                existing_contact['phone'] = format_phone_number(contact[5])
            if not existing_contact['email']:
                existing_contact['email'] = contact[6]

    for key, value in contact_dict.items():
        formatted_contacts.append(list(value.values()))

    return [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']] + formatted_contacts


formatted_contacts_list = process_contacts(contacts_list)


with open('phonebook.csv', mode="w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(formatted_contacts_list)
