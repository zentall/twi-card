import cerberus

schema = {
    "url": {
        "required": True,
        "type": "string",
        "regex": "https?://[^ ]+"
    },

    "title": {
        "required": True,
        "type": "string"
    },

    "description": {
        "required": True,
        "type": "string"
    },

    "card_type": {
        "required": True,
        "type": "string"
    }
}


validator = cerberus.Validator(schema)