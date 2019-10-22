# Microservice template for Python with subscription endpoints

![Microservice](https://img.shields.io/badge/microservice-ready-brightgreen.svg?style=for-the-badge)
[![Build status](https://img.shields.io/travis/com/microservices/python-events/master.svg?style=for-the-badge)](https://travis-ci.com/microservices/python-events)
[![Docker Build Status](https://img.shields.io/docker/build/microservices/awesome-noun.svg?style=for-the-badge)](https://hub.docker.com/r/OWNER/REPO/)

An OMS template for Python with subscription endpoints.

Usage
-----

### Listen to all users

```coffee
# Storyscript
your_service listen as srv
  when srv heartbeat as event
    log info event
# {"user": "max", "time": "..."}
# {"user": "moritz", "time": "..."}
```

### Listen to a single user

```coffee
# Storyscript
when your_service listen heartbeat user: 'Max' as event
  log info event
# {"user": "max", "time": "..."}
# {"user": "max", "time": "..."}
```

### Publish events

```coffee
# Storyscript
your_service publish eventName:'heartbeat' data:{'time': '...'}
```

Test
----

### Subscribe to all user events

```sh
> oms subscribe listen heartbeat
ℹ Building Docker image
…
✔ Built Docker image with name: oms/microservices/python-events
✔ Started Docker container: 7be7d3cc4da6
✔ Health check passed
✔ Ran action: `listen` with output:
✔ Subscribed to event: `heartbeat` data will be posted to this terminal window when appropriate
{
  "eventType": "heartbeat",
  "type": "com.microservices.python.template",
  "specversion": "0.2",
  "source": "/foo",
  "id": "PYTHON-TEMPLATE-0",
  "time": "2019-04-06T18:59:24.938Z",
  "datacontenttype": "application/json",
  "data": {
    "user": "max",
    "time": "Sat Apr 06 2019 18:59:24 GMT+0000 (Coordinated Universal Time)"
  }
}
{
  "eventType": "heartbeat",
  "type": "com.microservices.python.template",
  "specversion": "0.2",
  "source": "/foo",
  "id": "PYTHON-TEMPLATE-1",
  "time": "2019-04-06T18:59:26.938Z",
  "datacontenttype": "application/json",
  "data": {
    "user": "moritz",
    "time": "Sat Apr 06 2019 18:59:26 GMT+0000 (Coordinated Universal Time)"
  }
}
…
✔ Stopped Docker container: 7be7d3cc4da6
```

### Subscribe to all individual user events

```sh
> oms subscribe listen heartbeat -a user='max'
ℹ Building Docker image
…
✔ Built Docker image with name: oms/microservices/python-events
✔ Started Docker container: 5d2592cbd82b
✔ Health check passed
✔ Ran action: `listen` with output:
✔ Subscribed to event: `heartbeat` data will be posted to this terminal window when appropriate
{
  "eventType": "heartbeat",
  "type": "com.microservices.python.template",
  "specversion": "0.2",
  "source": "/foo",
  "id": "PYTHON-TEMPLATE-0",
  "time": "2019-04-06T19:04:00.845Z",
  "datacontenttype": "application/json",
  "data": {
    "user": "max",
    "time": "Sat Apr 06 2019 19:04:00 GMT+0000 (Coordinated Universal Time)"
  }
}
{
  "eventType": "heartbeat",
  "type": "com.microservices.python.template",
  "specversion": "0.2",
  "source": "/foo",
  "id": "PYTHON-TEMPLATE-1",
  "time": "2019-04-06T19:04:03.844Z",
  "datacontenttype": "application/json",
  "data": {
    "user": "max",
    "time": "Sat Apr 06 2019 19:04:03 GMT+0000 (Coordinated Universal Time)"
  }
}
…
✔ Stopped Docker container: 5d2592cbd82b
```
