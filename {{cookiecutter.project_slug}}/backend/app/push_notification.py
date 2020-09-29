import logging
from asyncio import Queue, get_event_loop
from uuid import uuid4

from aioapns import APNs, NotificationRequest
from aiofcm import FCM, Message
from aiohttp import web
from funcy import merge

from app import config
from app.sdk import sdk

if config.apns_pem_file:
    # How to create pem from p12
    # https://stackoverflow.com/a/1762824
    apns_cert_client = APNs(
        client_cert=config.apns_pem_file, use_sandbox=config.use_sandbox,
    )

if config.fcm_sender_id and config.fcm_api_key:
    fcm = FCM(config.fcm_sender_id, config.fcm_api_key)

MAIN_PUSH_NOTIFICATIONS_QUEUE = Queue()
FILTERED_PUSH_NOTIFICATIONS_QUEUE = Queue()


async def main_notifications_queue_worker():
    delays_list = []

    # NOTE получается, что delays_list может сильно разрастаться?
    while True:
        notification_data = await MAIN_PUSH_NOTIFICATIONS_QUEUE.get()
        existing_delay_tuples = [d for d in delays_list if d[0] == notification_data]

        if len(existing_delay_tuples) > 0:
            for existing_delay_tuple in existing_delay_tuples:
                notification_handler_callback = existing_delay_tuple[-1]

                notification_handler_callback.cancel()

        loop = get_event_loop()

        put_to_filtered_queue_callback = loop.call_later(
            1, FILTERED_PUSH_NOTIFICATIONS_QUEUE.put_nowait, notification_data
        )
        delay_tuple = (
            notification_data,
            put_to_filtered_queue_callback,
        )
        delays_list.append(delay_tuple)
        MAIN_PUSH_NOTIFICATIONS_QUEUE.task_done()


async def filtered_notifications_queue_worker():
    while True:
        notification_data = await FILTERED_PUSH_NOTIFICATIONS_QUEUE.get()
        user_pk = notification_data["user_pk"]
        notification = notification_data["notification"]

        await send_push_notifications_from_queue([user_pk], notification)
        FILTERED_PUSH_NOTIFICATIONS_QUEUE.task_done()


# Use only for testing purposes
# @sdk.operation(["POST"], ["send-push-notification"])
# async def send_push_notification_entrypoint(operation, request):
#     """
#     POST /send-push-notification
#
#     notification:
#       title: Hello
#       text: This is a test push
#     userId: '12345'
#     """
#     resource = request["resource"]
#     notification = resource["notification"]
#     result = await send_push_notification(
#         resource["userId"],
#         create_notification(
#             notification["title"], notification["text"], notification.get("data")
#         ),
#     )
#     return web.json_response(result)


def create_notification(title, text, data=None):
    # https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/generating_a_remote_notification
    # https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#notification

    data = data or {}

    return {
        "ios": {
            "aps": {
                "alert": {"title": title, "body": text},
                "badge": 0,
                "sound": "default",
            },
            "data": data,
        },
        "android": {"data": merge(data, {"title": title, "body": text})},
    }


async def send_push_notification(user_pk, notification):
    return await send_push_notifications([user_pk], notification)


async def send_push_notifications(user_pks, notification):
    for user_pk in user_pks:
        await MAIN_PUSH_NOTIFICATIONS_QUEUE.put(
            {"user_pk": user_pk, "notification": notification}
        )


async def send_push_notifications_from_queue(user_pks, notification):
    if len(user_pks) == 0:
        return {"ok": 0, "error": 0}
    result = {"ok": 0, "error": 0}
    for sub in (
        await sdk.client.resources("PushSubscription")
        .search(user=",".join(user_pks))
        .fetch_all()
    ):
        if sub["deviceType"] == "ios":
            request = NotificationRequest(
                device_token=sub["deviceToken"],
                message=notification["ios"],
                notification_id=str(uuid4()),
            )
            response = await apns_cert_client.send_notification(request)
            logging.info(
                "Apple response for %s is %s,%s",
                sub["id"],
                response.status,
                response.description,
            )
            if not response.is_successful:
                await sdk.client.resource("PushSubscription", **sub).delete()
            result["ok"] += 1
        elif sub["deviceType"] == "android":
            message = Message(
                device_token=sub["deviceToken"],
                notification=notification["android"],
                data=notification["android"]["data"],
                message_id=str(uuid4()),
            )
            response = await fcm.send_message(message)
            if not response.is_successful:
                await sdk.client.resource("PushSubscription", **sub).delete()
            logging.info(
                "Google response for %s is %s,%s",
                sub["id"],
                response.status,
                response.description,
            )
            result["ok"] += 1
        else:
            logging.error(
                "Unknown deviceType %s for PushSubscription %s",
                sub["deviceType"],
                sub["id"],
            )
            result["error"] += 1
    return result
