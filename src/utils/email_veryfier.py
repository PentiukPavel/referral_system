from http import HTTPStatus
import logging

from aiohttp import ClientSession, ClientResponse

from core.config import settings

logger = logging.getLogger("logs")


async def get_response(session: ClientSession, url: str) -> ClientResponse:
    """
    Получение http response.

    :param url: url
    :return: http response
    """

    async with session.get(url) as result:
        return result


async def email_veryfier(email: str) -> bool:
    """
    Проверка email с помощью API hunter.io

    :param email: email
    :return: результат проверки
    """

    try:
        url = (
            f"{settings.VERIFIER_URL}?email="
            f"{email}&api_key{settings.VERIFIER_API_CODE}"
        )
        async with ClientSession() as session:
            response = await get_response(session, url)
            if response.status == HTTPStatus.OK:
                email_status = response.json()["data"]["status"]
                status_verification = response.json()["data"]["result"]
                if (
                    email_status == "invalid"
                    and status_verification == "deliverable"
                ):
                    return False
        return True
    except Exception as e:
        logger.exception(e)
