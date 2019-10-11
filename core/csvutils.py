# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# CSV import/export utilities
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import csv

# Third-party modules
import six
from six.moves import zip

# Third-party modules
from django.db import models


# CSV import conflict resolution constants
IR_FAIL = 0  # Fail on first conflict
IR_SKIP = 1  # Skip conflicted records
IR_UPDATE = 2  # Overwrite conflicted records
# Set of ignored fields
IGNORED_FIELDS = {"id", "bi_id"}


def update_if_changed(obj, values):
    """
    Update fields if changed.
    :param obj: Document instance
    :type obj: Document
    :param values: New values
    :type values: dict
    :returns: List of changed (key, value)
    :rtype: list
    """
    changes = []
    for k, v in six.iteritems(values):
        vv = getattr(obj, k)
        if v != vv:
            if not isinstance(v, int) or not hasattr(vv, "id") or v != vv.id:
                setattr(obj, k, v)
                changes += [(k, v)]
    if changes:
        obj.save()
    return changes


def get_model_fields(model):
    # Detect fields
    fields = []
    ignored = set(getattr(model, "csv_ignored_fields", [])) | IGNORED_FIELDS
    for f in model._meta.fields:
        if f.name in ignored:
            continue
        required = not f.null and f.default == models.fields.NOT_PROVIDED
        # Process references
        if f.rel:
            if isinstance(f.rel, models.fields.related.ManyToOneRel):
                # Foreign Key
                # Try to find unique key
                k = "id"
                for ff in f.remote_field.model._meta.fields:
                    if ff.name != k and ff.unique:
                        k = ff.name
                        break
                fields += [(f.name, required, f.remote_field.model, k)]
        elif hasattr(f, "document"):
            k = f.document._meta["id_field"]
            for ff, fi in six.iteritems(f.document._fields):
                if fi.name != k and fi.unique and fi.name not in IGNORED_FIELDS:
                    k = fi.name
                    break
            fields += [(f.name, required, f.document, k)]
        else:
            fields += [(f.name, required, None, None)]
    return fields


def csv_export(model, queryset=None, first_row_only=False):
    """
    Export to CSV
    """
    io = six.StringIO()
    writer = csv.writer(io)
    fields = get_model_fields(model)
    # Write header
    writer.writerow([f[0] for f in fields])
    if first_row_only:
        return io.getvalue()
    # Build queryset
    if queryset is None:
        queryset = model.objects.all()
        # Write rows
    for r in queryset.select_related():
        row = []
        # Format row
        for f, required, rel, rf in fields:
            v = getattr(r, f)
            if v is None:
                v = ""
            if f == "tags":
                row += [",".join(v)]
            elif rel is None or not v:
                row += [v]
            else:
                row += [getattr(v, rf)]
        row = [unicode(f).encode("utf-8") for f in row]
        writer.writerow(row)
        # Return result
    return io.getvalue()


def csv_import(model, f, resolution=IR_FAIL, delimiter=","):
    """
    Import from CSV
    :returns: (record_count,error_message).
              record_count is None if error_message set
    """
    # Detect UTF8 BOM (EF BB BF)
    if not f.read(3) == "\xef\xbb\xbf":
        # No BOM found, seek to start
        f.seek(0)
    reader = csv.reader(f, delimiter=delimiter)
    # Process model fields
    field_names = set()
    required_fields = set()
    unique_fields = {ff.name for ff in model._meta.fields if ff.unique}
    fk = {}  # Foreign keys: name->(model,field)
    # find boolean fields
    booleans = {ff.name for ff in model._meta.fields if isinstance(ff, models.BooleanField)}
    integers = {ff.name for ff in model._meta.fields if isinstance(ff, models.IntegerField)}
    # Search for foreign keys and required fields
    ir = {"id", "bi_id"}
    ir.update(getattr(model, "csv_ignored_fields", []))
    for name, required, rel, rname in get_model_fields(model):
        field_names.add(name)
        if rel:
            fk[name] = (rel, rname)
        if required and name not in ir:
            required_fields.add(name)
    # Read and validate header
    header = next(reader)
    left = field_names.copy()
    u_fields = [h for h in header if h in unique_fields]
    ut_fields = [
        fs
        for fs in model._meta.unique_together
        if len(fs) == len([ff for ff in fs if ff in header])
    ]
    # Check field names
    for h in header:
        if h not in field_names:
            return None, "Invalid field '%s'" % h
        left.remove(h)
    # Check all required fields present
    for h in left:
        if h in required_fields:
            return None, "Required field '%s' is missed" % h
    # Load data
    count = 0
    l_header = len(header)
    for row in reader:
        count += 1
        if len(row) != l_header:
            return None, "Invalid row size. line %d" % count
        vars = dict(zip(header, row))
        for h, v in vars.items():
            if v in ("None", ""):
                v = None
            # Check required field is not none
            if not v and h in required_fields:
                return None, "Required field '%s' is empty at line %d" % (h, count)
            # Delete empty values
            if not v:
                del vars[h]
            else:
                if h in fk:
                    # reference foreign keys
                    rel, rname = fk[h]
                    try:
                        ro = rel.objects.get(**{rname: v})
                    except rel.DoesNotExist:
                        # Failed to reference by name, fallback to id
                        try:
                            id = int(v)
                        except ValueError:
                            return (
                                None,
                                "Cannot resolve '%s' in field '%s' at line '%s'" % (v, h, count),
                            )
                        try:
                            ro = rel.objects.get(**{"id": id})
                        except rel.DoesNotExist:
                            return (
                                None,
                                "Cannot resolve '%s' in field '%s' at line '%s'" % (v, h, count),
                            )
                    vars[h] = ro
                elif h in booleans:
                    # Convert booleans
                    vars[h] = v.lower() in ["t", "true", "yes", "y"]
                elif h in integers:
                    # Convert integers
                    try:
                        vars[h] = int(v)
                    except ValueError as e:
                        raise ValueError("Invalid integer: %s" % e)
                elif h == "tags":
                    vars[h] = [x.strip() for x in v.split(",") if x.strip()]
        # Find object
        o = None
        for f in u_fields:
            if f not in vars:
                continue
            # Find by unique fields
            try:
                o = model.objects.get(**{f: vars[f]})
                break
            except model.DoesNotExist:
                pass
        if o is None and ut_fields:
            # Find by composite unique keys
            for fs in ut_fields:
                try:
                    o = model.objects.get(**dict([(f, vars[f]) for f in fs if f in vars]))
                    break
                except model.DoesNotExist:
                    pass
        if o:
            # Object exists, behave according the resolution order
            if resolution == IR_FAIL:
                # Fail
                return (
                    None,
                    "Failed to save line %d: Object %s is already exists" % (count, repr(vars)),
                )
            elif resolution == IR_SKIP:
                # Skip line
                count -= 1
                continue
            elif resolution == IR_UPDATE:
                c = update_if_changed(o, vars)
                if not c:
                    count -= 1
                continue
        else:
            # Create object
            o = model()
        # Set attributes
        for k, v in six.iteritems(vars):
            setattr(o, k, v)
        # Save
        try:
            o.save()
        except Exception as e:
            return None, "Failed to save line %d: %s. %r" % (count, e, vars)
    return count, None
