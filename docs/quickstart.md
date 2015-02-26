Quickstart
==========

As a start, we implement a Todo application based on `resource`.


Todo
----

Below is the full code of Todo:

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from flask import Flask
    from rsrc import Resource, View, Response, status
    from rsrc.exceptions import NotFoundError
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
            try:
                return Response(todos[pk])
            except KeyError:
                raise NotFoundError()

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
            try:
                todos[pk].update(request.data)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except KeyError:
                raise NotFoundError()

        def delete_list(self, request):
            todos.clear()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def delete_item(self, request, pk):
            pk = int(pk)
            try:
                del todos[pk]
                return Response(status=status.HTTP_204_NO_CONTENT)
            except KeyError:
                raise NotFoundError()


    resource = Resource('todos', Todo)

    app = Flask(__name__)


    if __name__ == '__main__':
        add_resource(app, resource)
        app.run(debug=True)


HTTP-verb and View-method
-------------------------

When you access the `todos` resource via different HTTP verbs, different methods of Todo view will be called. The following table shows the correspondence:

HTTP Verb          | View Method
------------------ | ---------------
GET    /todos      | Todo:get_list()
POST   /todos      | Todo:post()
DELETE /todos      | Todo:delete_list()
GET    /todos/<pk> | Todo:get_item()
PUT    /todos/<pk> | Todo:put()
PATCH  /todos/<pk> | Todo:patch()
DELETE /todos/<pk> | Todo:delete_item()
