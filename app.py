#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
from collections import namedtuple
from datetime import datetime, timezone
from threading import Thread
from time import sleep


import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

Node = namedtuple('Node', ['endpoint', 'data'])


# A simple manager which tracks all event subscriptions
class Manager:

    def __init__(self):
        self._events = {}
        self._nr_sent_events = 0

    def subscribe(self, id_, endpoint, event_name, data):
        data = data or {}
        logger.info(f'[subscribe] id: "{id_}", endpoint:"{endpoint}"'
                    f'name: "{event_name}", data: %s', data)
        if event_name not in self._events:
            self._events[event_name] = {}
        # Check whether the id is new
        if id_ in self._events[event_name]:
            return False
        self._events[event_name][id_] = Node(endpoint, data)

    def unsubscribe(self, id_, event_name):
        logger.info(f'[unsubscribe] id: "{id_}", name: "{event_name}"')
        if event_name not in self._events:
            return False
        # Check whether the id exists
        if id_ not in self._events[event_name]:
            return False
        del self._events[event_name][id_]

    def publish(self, event_name, data):
        logger.info(f'[publish] name: "{event_name}", data: %s', data)
        if event_name not in self._events:
            return False

        for node in self._events[event_name].values():
            # filter for user (optional)
            if 'user' in node.data and 'user' in data:
                if node.data['user'] == data['user']:
                    self._send_event(node, event_name, data)
            else:
                self._send_event(node, event_name, data)

        return True

    def _send_event(self, node, event_name, data):
        local_time = datetime.now(timezone.utc).astimezone()
        requests.post(node.endpoint, json={
            'eventType': event_name,
            'type': 'com.microservices.python.template',
            'specversion': '0.2',
            'source': '/my-source',
            'id': f'PYTHON-TEMPLATE-{self._nr_sent_events}',
            'time': local_time.isoformat(),
            'datacontenttype': 'application/json',
            'data': data,
        })
        self._nr_sent_events = self._nr_sent_events + 1


manager = Manager()


@app.route('/events', methods=['POST'])
def subscribe():
    return jsonify({'sucess': manager.subscribe(
        id_=request.json['id'],
        endpoint=request.json['endpoint'],
        event_name=request.json['event'],
        data=request.json.get('data', {}),
    )})


@app.route('/events', methods=['DELETE'])
def unsubscribe():
    return jsonify({'sucess': manager.unsubscribe(
        id_=request.json['id'],
        event_name=request.json['event'],
    )})


@app.route('/publish', methods=['POST'])
def publish():
    data = request.json.get('data', {})
    if 'user' in request.json:
        data['user'] = request.json['user']
    return jsonify({'sucess': manager.publish(
        event_name=request.json['event'],
        data=data,
    )})


@app.route('/health', methods=['GET'])
def health():
    return 'OK'


# Return errors as JSON objects
def app_error(e):
    return jsonify({'message': str(e)}), 400


# Calls a callback every period with args
def set_interval(period, callback, **args):
    def wrapper():
        while True:
            sleep(period)
            callback(**args)
    Thread(target=wrapper).start()


def heartbeat(user):
    manager.publish('heartbeat', {
        'user': user,
        'time': str(datetime.now()),
    })


if __name__ == '__main__':
    app.register_error_handler(Exception, app_error)
    set_interval(3, heartbeat, user='max')
    set_interval(5, heartbeat, user='moritz')
    app.run(host='0.0.0.0', port=8080)
