#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlsoup
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from jsonpatch import JsonPatch
from mongosql import MongoQuery

from resource import View, Response, status
from resource.core.exceptions import BaseError, NotFoundError
from resource.utils import get_exception_detail


class Table(View):
    """For RDBMS (SQL)."""

    def __init__(self, *arg, **kwargs):
        super(Table, self).__init__(*arg, **kwargs)

        base = automap_base()
        base.prepare(self.db, reflect=True)
        self.session = Session(self.db)
        self.model = getattr(base.classes, self.table_name)

        self.db = sqlsoup.SQLSoup(self.db)
        try:
            self.engine = getattr(self.db, self.table_name, None)
        except sqlalchemy.exc.NoSuchTableError:
            raise BaseError(
                '"%s" has no table named `%s`' % (self.db, self.table_name)
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

    def as_dict(self, row, fields=None):
        columns = self.engine._table.columns
        if fields is not None:
            columns = [c for c in columns if c.name in fields]

        return {
            column.name: getattr(row, column.name, None)
            for column in columns
        }

    def from_dict(self, row, doc):
        for column, value in doc.items():
            setattr(row, column, value)

    def to_sqla_sort(self, sort):
        if sort is None:
            return None
        return [
            '%s%s' % (field_name, '-' if order == -1 else '+')
            for field_name, order in sort
        ]

    def get_list(self, page, per_page, sort, fields, lookup):
        skip, limit = (page - 1) * per_page, per_page
        sort = self.to_sqla_sort(sort)

        mq = MongoQuery.get_for(self.model, self.session.query(self.model))
        query = mq.filter(lookup or None)
        rows = query.sort(sort).limit(limit, skip).end()
        count = query.end().count()

        content = [self.as_dict(row, fields) for row in rows]
        headers = self.make_pagination_headers(page, per_page, count)
        return Response(content, headers=headers)

    def get_item(self, pk):
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
