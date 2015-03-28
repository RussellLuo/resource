Introduction
============

Introduce to you the core concepts of `Resource` library.


Resource as the building block
------------------------------

In the world of RESTful APIs, resource is the first-class citizen. That is to say, when you are implementing a RESTful API, resources are your building blocks.

Suppose we are implementing a [RBAC][1] system, there are three key components: subject, role and permission. Then, we can divide the RESTful API into three resources:

+ Subject
+ Role
+ Permission


Resource is a collection
------------------------

In `Resource` library, a resource is conceptually equivalent to a collection (or a list).

As an example, the above three resources will be created like this:

    from rsrc import Resource, View

    # Subject resource
    class Subject(View):
        ...
    subjects = Resource('subjects', Subject)

    # Role resource
    class Role(View):
        ...
    roles = Resource('roles', Role)

    # Permission resource
    class Permission(View):
        ...
    permissions = Resource('permissions', Permission)


Design principle
----------------

Most of the design principles of `Resource` library are learned from [Best Practices for Designing a Pragmatic RESTful API][2].


[1]: http://en.wikipedia.org/wiki/Role-based_access_control
[2]: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
