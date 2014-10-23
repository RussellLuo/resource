#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bson
from jsonpatch import JsonPatch

from resource import View, Response, status
from resource.exceptions import get_exception_detail, NotFoundError


class Collection(View):
    """For MongoDB (NoSQL)."""

    def __init__(self, *arg, **kwargs):
        super(Collection, self).__init__(*arg, **kwargs)
        self.engine = self.db[self.table_name]

    def get_pk(self, pk):
        try:
            return bson.ObjectId(pk)
        except bson.errors.InvalidId:
            raise NotFoundError()

    def get_doc(self, pk):
        doc = self.engine.find_one({'_id': self.get_pk(pk)})
        if doc:
            return doc
        else:
            raise NotFoundError()

    def to_mongo_fields(self, fields):
        if fields is None:
            return None

        mongo_fields = {
            field_name: True
            for field_name in fields
        }
        if fields and '_id' not in fields:
            mongo_fields.update({'_id': False})
        return mongo_fields

    def get_list(self, page, per_page, sort, fields, lookup):
        skip, limit = (page - 1) * per_page, per_page
        fields = self.to_mongo_fields(fields)
        docs = self.engine.find(
            spec=lookup, skip=skip, limit=limit,
            sort=sort, fields=fields
        )
        count = self.engine.find(spec=lookup).count()
        headers = self.make_pagination_headers(page, per_page, count)
        return Response(list(docs), headers=headers)

    def get_item(self, pk):
        return Response(self.get_doc(pk))

    def post(self, data):
        form = self.form_cls(data)
        if form.is_valid():
            _id = self.engine.insert(form.document)
            return Response({'_id': _id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, pk, data):
        form = self.form_cls(data)
        if form.is_valid():
            doc = form.document
            doc.update({'_id': self.get_pk(pk)})
            self.engine.remove({'_id': doc['_id']})
            self.engine.insert(doc)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, pk, data):
        doc = self.get_doc(pk)

        # do JSON-Patch
        patch_data = JsonPatch(data)
        try:
            patch_data.apply(doc, in_place=True)
        except Exception as e:
            return Response({'jsonpatch_error': get_exception_detail(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        # validate data after JSON-Patch
        form = self.form_cls(doc)
        if form.is_valid():
            self.engine.save(form.document)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        doc = self.get_doc(pk)
        self.engine.remove({'_id': doc['_id']})
        return Response(status=status.HTTP_204_NO_CONTENT)
