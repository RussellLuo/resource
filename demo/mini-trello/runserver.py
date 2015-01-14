#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from rsrc import Resource, View, Response
from rsrc.exceptions import NotFoundError
from rsrc.framework.flask import add_resource

lists = {
    1: {'id': 1, 'name': 'list1'},
    2: {'id': 2, 'name': 'list2'}
}

cards = {
    1: {'id': 1, 'name': 'card1', 'list_id': 1},
    2: {'id': 2, 'name': 'card2', 'list_id': 1},
    3: {'id': 3, 'name': 'card3', 'list_id': 2},
}


class List(View):
    def get_list(self, request):
        return Response(lists.values())

    def get_item(self, request, pk):
        pk = int(pk)
        try:
            return Response(lists[pk])
        except KeyError:
            raise NotFoundError()


class Card(View):
    def get_list(self, request, list_id):
        list_id = int(list_id)
        query_func = lambda c: c['list_id'] == list_id
        result_cards = filter(query_func, cards.values())
        return Response(result_cards)

    def get_item(self, request, list_id, pk):
        list_id = int(list_id)
        pk = int(pk)
        query_func = lambda c: c['list_id'] == list_id and c['id'] == pk
        result_cards = filter(query_func, cards.values())
        if result_cards:
            return Response(result_cards[0])
        else:
            raise NotFoundError()


resources = [
    Resource('lists', List),
    Resource('cards', Card, uri='/lists/<list_id>/cards')
]

app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)
    app.run(debug=True)
