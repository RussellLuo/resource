#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlsoup
import sqlalchemy
from jsonpatch import JsonPatch

from resource import View, Response, status
from resource.core.exceptions import BaseError, NotFoundError
from resource.utils import get_exception_detail


class Table(View):
    """For RDBMS (SQL)."""

    def __init__(self, *arg, **kwargs):
        super(Table, self).__init__(*arg, **kwargs)
        self.db = sqlsoup.SQLSoup(self.db)
        try:
            self.engine = getattr(self.db, self.table, None)
        except sqlalchemy.exc.NoSuchTableError:
            raise BaseError(
                '"%s" has no table named `%s`' % (self.db, self.table)
            )

    def get_pk(self, pk):
        try:
            return int(pk)
        except ValueError:
            raise NotFoundError()

    def get_row(self, pk):
        row = self.engine.filter_by(id=self.get_pk(pk)).first()
        if row:
            return row
        else:
            raise NotFoundError()

    def as_dict(self, row):
        return {
            column.name: getattr(row, column.name, None)
            for column in self.engine._table.columns
        }

    def from_dict(self, row, doc):
        for column, value in doc.items():
            setattr(row, column, value)

    def get(self, pk=None, filter_=None):
        if pk is None:
            filter_ = filter_ or {}
            rows = map(self.as_dict, self.engine.filter_by(**filter_))
            return Response(rows)
        else:
            row = self.as_dict(self.get_row(pk))
            return Response(row)

    def post(self, data):
        form = self.form_cls(data)
        if form.is_valid():
            row = self.engine.insert(**form.document)
            self.db.commit()
            return Response({'id': row.id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, pk, data):
        form = self.form_cls(data)
        if form.is_valid():
            doc = form.document
            doc.update({'id': self.get_pk(pk)})
            self.engine.filter_by(id=doc['id']).delete()
            self.engine.insert(**doc)
            self.db.commit()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, pk, data):
        row = self.get_row(pk)
        doc = self.as_dict(row)

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
            self.from_dict(row, doc)
            self.db.commit()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        row = self.get_row(pk)
        self.db.delete(row)
        self.db.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)
