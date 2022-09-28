from schema import Schema, And, Use, SchemaError, Or

payload_schema = Schema({
    'load': And(Use(int), lambda n: 0 < n),
    'fuels': {
        str: And(Use(float), lambda n: 0 <= n)
    },
    'powerplants': [{
        'name': str,
        'type': str,
        'efficiency': Or(
            And(Use(float), lambda n: 0. <= n <= 1.),
            And(Use(int), lambda n: 0 <= n <= 1)
        ),
        'pmin': And(Use(int), lambda n: 0 <= n),
        'pmax': And(Use(int), lambda n: 0 < n),
    }]
})

def verifyPayload(payload: dict) -> dict:
    """This function verify the payload and return a boolean.

    Args:
        payload (dict): The payload to verify.

    Returns:
        dict: A dictionary containing the result of the verification.
    """

    return payload_schema.validate(payload)
