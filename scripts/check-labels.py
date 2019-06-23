#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Check gitlab MR labels
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import print_function
import os
import sys


ENV_LABELS = "CI_MERGE_REQUEST_LABELS"
ENV_CI = "CI"
ERR_OK = 0
ERR_FAIL = 1

PRI_LABELS = ["pri::p1", "pri::p2", "pri::p3", "pri::p4"]
COMP_LABELS = ["comp::trivial", "comp::low", "comp::medium", "comp::high"]
KIND_LABELS = ["kind::feature", "kind::improvement", "kind::bug", "kind::cleanup"]


def get_labels():
    """
    Get list of labels.
    :return: List of labels or None if environment is not set
    """
    if ENV_LABELS not in os.environ and ENV_CI not in os.environ:
        return None
    return os.environ.get(ENV_LABELS, "").split(",")


def go_url(anchor):
    return "https://docs.getnoc.com/master/en/go.html#%s" % anchor


def check_pri(labels):
    """
    Check `pri::*`
    :param labels:
    :return: List of problems
    """
    pri = [x for x in labels if x.startswith("pri::")]
    if not pri:
        return [
            "'pri::*' label is not set. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(PRI_LABELS), go_url("dev-mr-labels-pri"))
        ]
    if len(pri) > 1:
        return [
            "Multiple 'pri::*' labels defined. Must be exactly one.\n"
            "Refer to %s for details." % go_url("dev-mr-labels-priority")
        ]
    pri = pri[0]
    if pri not in PRI_LABELS:
        return [
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(PRI_LABELS), go_url("dev-mr-labels-pri"))
        ]
    return []


def check_comp(labels):
    """
    Check `comp::*`
    :param labels:
    :return:
    """
    comp = [x for x in labels if x.startswith("comp::")]
    if not comp:
        return [
            "'comp::*' label is not set. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(COMP_LABELS), go_url("dev-mr-labels-comp"))
        ]
    if len(comp) > 1:
        return [
            "Multiple 'comp::*' labels defined. Must be exactly one.\n"
            "Refer to %s for details." % go_url("dev-mr-labels-comp")
        ]
    comp = comp[0]
    if comp not in COMP_LABELS:
        return [
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(COMP_LABELS), go_url("dev-mr-labels-comp"))
        ]
    return []


def check_kind(labels):
    """
    Check `kind::*`
    :param labels:
    :return:
    """
    kind = [x for x in labels if x.startswith("kind::")]
    if not kind:
        return [
            "'kind::*' label is not set. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(KIND_LABELS), go_url("dev-mr-labels-kind"))
        ]
    if len(kind) > 1:
        return [
            "Multiple 'kind::*' labels defined. Must be exactly one.\n"
            "Refer to %s for details." % go_url("dev-mr-labels-kind")
        ]
    kind = kind[0]
    if kind not in KIND_LABELS:
        return [
            "Invalid label %s. Must be one of %s.\n"
            "Refer to %s for details." % (", ".join(KIND_LABELS), go_url("dev-mr-labels-kind"))
        ]
    return []


def check_affected(labels, name):
    n = sum(1 for x in labels if x == name)
    if not n:
        return [
            "'%s' label is not set.\n"
            "Refer to %s for details." % (name, go_url("dev-mr-labels-affected"))
        ]
    return []


def check(labels):
    """
    Perform all checks
    :param labels: List of labels
    :return: List of policy violations
    """
    problems = []
    if "--pri" in sys.argv:
        problems += check_pri(labels)
    if "--comp" in sys.argv:
        problems += check_comp(labels)
    if "--kind" in sys.argv:
        problems += check_kind(labels)
    for area in ["core", "documentation", "ui", "profiles", "migration", "tests"]:
        if "--%s" % area in sys.argv:
            problems += check_affected(labels, area)
    return problems


def main():
    labels = get_labels()
    problems = []
    if labels is None:
        problems += [
            "%s environment variable is not defined. Must be called within Gitlab CI" % ENV_LABELS
        ]
    else:
        problems += check(labels)
    if problems:
        print("\n\n".join(problems))
        sys.exit(ERR_FAIL)
    sys.exit(ERR_OK)


if __name__ == "__main__":
    main()
