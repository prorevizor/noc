# ----------------------------------------------------------------------
# Fill .md from collections
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import sys
import json
import os
from typing import Dict, Any, Iterable, List, Optional
from dataclasses import dataclass
import enum
import re
import shutil


@dataclass
class EventClassVar(object):
    name: str
    description: str
    type: str
    is_required: bool

    @property
    def is_required_mark(self):
        if self.is_required:
            return ":material-close:"
        else:
            return ":material-check:"


class DispositionAction(enum.Enum):
    CLEAR = "clear"
    RAISE = "raise"
    IGNORE = "ignore"


@dataclass
class EventClassDisposition(object):
    name: str
    action: DispositionAction
    alarm: str


@dataclass
class EventClass(object):
    name: str
    uuid: str
    description: str
    symptoms: str
    probable_causes: str
    recommended_actions: str
    vars: Optional[List[EventClassVar]]
    disposition: Optional[List[EventClassDisposition]]

    def quote(self, name: str) -> str:
        return name.strip().lower().replace(" ", "-")

    @property
    def dir_path(self) -> List[str]:
        return [self.quote(x) for x in self.name.split(" | ")][:-1]

    @property
    def file_name(self) -> str:
        return self.quote(self.name.split(" | ")[-1]) + ".md"


class CollectionDoc(object):
    rx_indent = re.compile(r"^(\s+)-")

    def __init__(self):
        full_path = os.path.abspath(sys.argv[0])
        self.src_root = os.path.abspath(os.path.join(os.path.dirname(full_path), "..", ".."))
        self.doc_root = os.path.join(self.src_root, "docs", "en", "docs")
        self.yml_path = os.path.join(self.src_root, "docs", "en", "mkdocs.yml")
        self.new_yml_path = f"{self.yml_path}.new"
        self.event_class: Dict[str, EventClass] = {}

    def build(self):
        shutil.copy(self.yml_path, self.new_yml_path)
        self.read_collections()
        self.build_eventclasses()

    def read_collections(self):
        self.read_eventclasses()

    def iter_jsons(self, path: str) -> Iterable[Dict[str, Any]]:
        for root, _, files in os.walk(path):
            for fn in files:
                if fn.startswith(".") or not fn.endswith(".json"):
                    continue
                with open(os.path.join(root, fn)) as f:
                    yield json.loads(f.read())

    def read_eventclasses(self):
        for d in self.iter_jsons(os.path.join("collections", "fm.eventclasses")):
            event_class = EventClass(
                name=d["name"],
                uuid=d["uuid"],
                description=d.get("description") or "",
                symptoms=d.get("symptoms") or "",
                probable_causes=d.get("probable_causes") or "",
                recommended_actions=d.get("recommended_actions") or "",
                vars=None,
                disposition=None,
            )
            ec_vars = d.get("vars")
            if ec_vars:
                event_class.vars = [
                    EventClassVar(
                        name=v["name"],
                        description=v["description"],
                        type=v.get("type"),
                        is_required=bool(v.get("required")),
                    )
                    for v in ec_vars
                ]
            ec_disposition = d.get("disposition")
            if ec_disposition:
                event_class.disposition = [
                    EventClassDisposition(
                        name=v["name"],
                        action=DispositionAction(v["action"]),
                        alarm=v["alarm_class__name"],
                    )
                    for v in ec_disposition
                    if v["action"] != "ignore"
                ]
            self.event_class[event_class.name] = event_class

    def ensure_dir(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def update_toc(self, key: str, lines: List[str]):
        r = []
        rx_key = re.compile(fr"^(\s+)- {key}:")
        indent = ""
        to_feed = False
        with open(self.new_yml_path) as f:
            for line in f:
                line = line[:-1]
                if to_feed:
                    # Feed rest of ToC
                    r += [line]
                    continue
                if not indent:
                    # Search mode
                    r += [line]
                    match = rx_key.search(line)
                    if match:
                        indent = match.group(1)
                        # Inject new part of ToC
                        r += [f"{indent}    {item}" for item in lines]
                    continue
                # Search for the next item
                match = self.rx_indent.search(line)
                if match:
                    if len(match.group(1)) <= len(indent):
                        to_feed = True
                    else:
                        continue  # Skip replaced part
                r += [line]
        with open(self.new_yml_path, "w") as f:
            f.write("\n".join(r))

    def build_eventclasses(self):
        print("# Writing event classes doc:")
        new_files = 0
        changed_files = 0
        unmodified_files = 0
        toc = []
        ec_root = os.path.join(self.doc_root, "reference", "event-classes")
        last_path: List[str] = []
        indent: str = ""
        for ec_name in sorted(self.event_class):
            ec = self.event_class[ec_name]
            rel_dir = os.path.join(*ec.dir_path)
            ec_dir = os.path.join(ec_root, rel_dir)
            self.ensure_dir(ec_dir)
            path = [x.strip() for x in ec_name.split(" | ")][:-1]
            if not last_path or path != last_path:
                level = 0
                for last_pc, current_pc in zip(last_path, path):
                    if last_pc == current_pc:
                        level += 1
                    else:
                        break
                indent = "    " * (level - 1)
                for current_pc in path[level:]:
                    indent = "    " * level
                    toc += [f'{indent}- "{current_pc}":']
                    level += 1
                last_path = path
            short_name = ec_name.split(" | ")[-1].strip()
            toc += [
                f'{indent}    - "{short_name}": reference/event-classes/{rel_dir}/{ec.file_name}'
            ]
            # render page
            data = ["---", f"uuid: {ec.uuid}", "---", f"# {ec.name}"]
            if ec.description:
                data += ["", ec.description]
            data += ["", "## Symptoms"]
            if ec.symptoms:
                data += ["", ec.symptoms]
            data += ["", "## Probable Causes"]
            if ec.probable_causes:
                data += ["", ec.probable_causes]
            data += ["", "## Recommended Actions"]
            if ec.recommended_actions:
                data += ["", ec.recommended_actions]
            if ec.vars:
                data += [
                    "",
                    "## Variables",
                    "",
                    "Variable | Type | Required | Description",
                    "--- | --- | --- | ---",
                ]
                data += [
                    f"{v.name} | {v.type} | {v.is_required_mark} | {v.description}" for v in ec.vars
                ]
            if ec.disposition:
                data += ["", "## Alarms"]
                d_list = [d for d in ec.disposition if d.action == DispositionAction.RAISE]
                if d_list:
                    data += [
                        "",
                        "### Raising alarms",
                        "",
                        f"`{ec.name}` events may raise following alarms:",
                        "",
                        "Alarm Class | Description",
                        "--- | ---",
                    ]
                    data += [f"`{d.alarm}` | {d.name}" for d in d_list]
                d_list = [d for d in ec.disposition if d.action == DispositionAction.CLEAR]
                if d_list:
                    data += [
                        "",
                        "### Clearing alarms",
                        "",
                        f"`{ec.name}` events may clear following alarms:",
                        "",
                        "Alarm Class | Description",
                        "--- | ---",
                    ]
                    data += [f"`{d.alarm}` | {d.name}" for d in d_list]
            data += [""]
            page = "\n".join(data)
            #
            page_path = os.path.join(ec_dir, ec.file_name)
            to_write = False
            if os.path.exists(page_path):
                with open(page_path) as f:
                    old_page = f.read()
                if old_page == page:
                    unmodified_files += 1
                else:
                    changed_files += 1
                    to_write = 1
            else:
                new_files += 1
                to_write = True
            if to_write:
                print(f"Writing: {ec_dir}/{ec.file_name}")
                with open(page_path, "w") as f:
                    f.write(page)
        # print("\n".join(toc))
        total_files = new_files + changed_files + unmodified_files
        print(
            f"  Pages: new {new_files}, changed {changed_files}, unmodified {unmodified_files}, total {total_files}"
        )
        self.update_toc("Event Classes", toc)


if __name__ == "__main__":
    CollectionDoc().build()
