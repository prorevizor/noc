# ----------------------------------------------------------------------
# cleaning label commands
# ----------------------------------------------------------------------
# Copyright (C) 2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db.models import Func, F

# NOC modules
from noc.core.management.base import BaseCommand
from noc.core.mongo.connection import connect
from noc.models import get_model
from noc.main.models.label import Label


models = [
    #    ("fm.ActiveAlarm", "labels"),
    #    ("fm.ArchivedAlarm", "labels"),
    ("sa.ManagedObject", "labels"),
    #    ("sla.SLAProbe", "labels"),
]


class ArrayRemove(Func):
    function = "array_remove"
    template = "%(function)s(%(expressions)s, %(expressions)s)"


class Command(BaseCommand):
    help = "Cleaning label"

    def add_arguments(self, parser):
        parser.add_argument(
            "label",
            help="label name",
        ),

    def is_document(self, klass):
        """
        Check klass is Document instance
        :param cls:
        :return:
        """
        return isinstance(klass._meta, dict)

    def delete_label(self, model, field, label_name):
        self.print(f"began cleaning {model}...")
        field__contains = f"{field}__contains"
        model_ins = get_model(model)
        if self.is_document(model_ins):
            label = label_name
            model_ins.objects.filter(**{field__contains: label})
        else:
            label = [label_name]
            model_ins.objects.filter(**{field__contains: label}).update(
                labels=Func(ArrayRemove(F(field), label_name))
            )
        self.print(f"finished {model}\n")

    def reading_models(self, label):
        for model, field in models:
            self.delete_label(model, field, label)

    def handle(self, label, *args, **options):
        connect()
        if Label.objects.filter(name=label).first():
            self.print(f"Label: {label}\n")
            self.reading_models(label)
            self.print("Done")
        else:
            self.print(f"{label} doesn't exist")


if __name__ == "__main__":
    Command().run()
