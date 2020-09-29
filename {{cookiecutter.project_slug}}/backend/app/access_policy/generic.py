user_can_create_push_subscription = {
    "required": [
        "resource",
        "params",
    ],
    "properties": {
        "request-method": {"constant": "put"},
        "params": {
            "required": [
                "resource/type",
            ],
            "properties": {
                "resource/type": {"constant": "PushSubscription"},
            },
        },
    },
}

user_can_delete_push_subscription = {
    "required": [
        "params",
    ],
    "properties": {
        "request-method": {"constant": "delete"},
        "params": {
            "required": [
                "resource/type",
                "resource/id",
            ],
            "properties": {
                "resource/type": {"constant": "PushSubscription"},
            },
        },
    },
}
