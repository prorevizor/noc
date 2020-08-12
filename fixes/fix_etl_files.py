# ----------------------------------------------------------------------
# Fix ETL file/compression format
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
import os

# NOC modules
from noc.core.compressor.loader import loader
from noc.config import config

ext_map = {cc.ext: cc for cc in (c for c in loader.iter_classes()) if cc.ext}


def fix():
    root = config.path.etl_import
    if not os.path.exists(root):
        return  # Nothing to convert
    for d in os.listdir(root):
        sys_root = os.path.join(root, d)
        if not os.path.exists(sys_root):
            continue
        imports = [f for f in os.listdir(sys_root) if f.startswith("import.csv")]
        if "import.csv" in imports:
            ensure_format(os.path.join(sys_root, "import.csv"))
        elif len(imports) == 1:
            ensure_format(os.path.join(sys_root, imports[0]))
        arch_root = os.path.join(sys_root, "archive")
        archives = {f for f in os.listdir(arch_root) if f.startswith("import-")}
        for f in archives:
            ensure_format(os.path.join(arch_root, f))


def ensure_format(path: str) -> None:
    ext = config.etl.compression
    if path.endswith(ext):
        return  # Already compressed
    src_ext = ""
    for ext in ext_map:
        if path.endswith(ext):
            src_ext = ext
            break
    src_comp = loader.get_class(src_ext)
    dst_comp = loader.get_class(ext)
    dst_path = path[: -len(src_ext)] + ext
    print("Repacking %s -> %s" % (path, dst_path))
    with src_comp(path, "r") as src, dst_comp(dst_path, "w") as dst:
        dst.write(src.read())
    os.unlink(path)
