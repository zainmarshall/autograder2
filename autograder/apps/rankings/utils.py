import requests
import logging
import string

logger = logging.getLogger(__name__)


def get_codeforces_rating(user):
    if user.cf_handle is None or len(user.cf_handle) == 0:
        return 0
    handle = str(user.cf_handle)
    if not all([c in string.ascii_letters + string.digits + "_." for c in handle]):
        return 0

    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)

    if response.status_code != 200:
        logger.warning(response)
        logger.warning("Failed to connect to Codeforces API.")
        return None

    data = response.json()
    if data["status"] == "OK":
        res = data["result"][0].get("maxRating", 0)
        logger.info(
            f"Fetched cf rating of {res} from handle {handle} of user {user.username}"
        )
        return res
    else:
        logger.info(f"API error: {data['comment']}")
        return None
