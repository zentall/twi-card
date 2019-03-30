import cerberus

schema = {
    "img": {
        "required": True
    },

    "url": {
        "required": True,
        "type": "binary",
        "regex": "https?://[^ ]+"
    },

    "title": {
        "required": True,
        "type": "binary"
    },

    "description": {
        "required": True,
        "type": "binary"
    }
}


validator = cerberus.Validator(schema)