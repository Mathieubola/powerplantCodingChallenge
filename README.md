# Powerplan production plan calculator

This is an api that calculates the production plan for a powerplant given a load and a list of powerplants.

## How to run

### Localy

In order to run the app localy, you need [Python 3.8](https://www.python.org/downloads/release/python-380/) (or newer) and [pip](https://pip.pypa.io/en/stable/installing/).

Then, you can run the following commands to install the nessessary dependancies:

```bash
pip install -r requirements.txt
```

And then you can run the following command to start the server in debug mode:

```bash
python3 ./app.py
```

Or run this command to start the server in production mode

```bash
python3 -m flask run --host=0.0.0.0 --port=8888
```

### Docker

You can also run the app using docker. In order to do so, you need [Docker](https://docs.docker.com/get-docker/) installed.

Then, you can run the following command to build the docker image:

```bash
docker build -t ppe .
```

And then you can run the following command to start the server:

```bash
docker run -p 8888:8888 ppe
```

## How to use

Once the api is up and running, you can all it in code with a request api or using postman.

### Production plan

The only endpoint of this api is `/productionplan` and it accepts a `POST` request with the following body:

```python
{
    "load": int,
    "fuels": {
        str: float,
        ...
    },
    "powerplants": [
        {
            "name": str,
            "type": str,
            "efficiency": float,
            "pmin": int,
            "pmax": int
        }, ...
    ]
}
```

The api will then solve the problem and return a response with the following body:

```python
[
    {
        "name": str,
        "p": int
    }, ...
]
```

If the problem is unsolvable, the api will return a `400` error with the following body:

```python
{
    "error": str
}
```

### Adding / modifying powerplants type and fuel

The api comes with a default list of powerplants types and fuels. You can add or modify them by editing the `config.json` file in the `ProductionPlanEngine` folder.

### Adding / modifying free powerplants

Juste note that the `wind` type is a special type that doesn't use any fuel. You can change this too in the `config.json` file.

### Adding / modifying co2 emission cost

You can also change the co2 emission cost by editing the `config.json` file in the `ProductionPlanEngine` folder.