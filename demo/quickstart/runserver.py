#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from rsrc import Resource, View, Response, status
from rsrc.framework.flask import add_resource

todos = {
    1: {'id': 1, 'name': 'work'},
    2: {'id': 2, 'name': 'sleep'}
}


class Todo(View):
    def get_list(self, request):
        return Response(todos.values())

    def get_item(self, request, pk):
        pk = int(pk)
        return Response(todos.get(pk, {}))

    def post(self, request):
        pk = len(todos) + 1
        item = dict(id=pk, **request.data)
        todos[pk] = item
        return Response({'id': pk}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        pk = int(pk)
        item = dict(id=pk, **request.data)
        todos[pk] = item
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        pk = int(pk)
        todos[pk].update(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        pk = int(pk)
        del todos[pk]
        return Response(status=status.HTTP_204_NO_CONTENT)


resource = Resource('todos', Todo)

app = Flask(__name__)


if __name__ == '__main__':
    add_resource(app, resource)
    app.run(debug=True)
