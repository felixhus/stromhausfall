import requests


def get_icon_url(icon_name):
    """
    Takes an icon name in the format "mdi:icon-name" and returns the Iconify URL for the icon.
    """
    base_url = "https://api.iconify.design"
    icon_url = f"{base_url}/{icon_name}.svg"
    response = requests.get(icon_url)
    return response.url

print(get_icon_url('quill:discard'))