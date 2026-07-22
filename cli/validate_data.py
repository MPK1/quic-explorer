#!/usr/bin/env python3
"""Validate the QUIC Explorer dataset.

Runs two layers of checks over ``data/*.json``:

1. **Schema validation** — each data file must conform to its
   ``data/*.schema.json`` (JSON Schema).
2. **Referential integrity & consistency** — beyond what the schemas can
   express:
   * implementation/feature UUIDs are well-formed and unique,
   * every entry references an existing implementation and feature,
   * there is at most one entry per (implementation, feature) pair,
   * each entry's ``value`` matches the ``value_type`` of its feature.

Exits non-zero (and prints every problem found) if anything fails.

Usage::

    python cli/validate_data.py

Used by CI (``.github/workflows/json-linter.yml``) and the pre-commit hook
(``.pre-commit-config.yaml``).
"""

import json
import os
import sys
import uuid

from jsonschema import Draft7Validator

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)

# label -> (data file, schema file)
FILES = {
    "implementations": ("implementations.json", "implementations.schema.json"),
    "features": ("features.json", "features.schema.json"),
    "entries": ("entries.json", "entries.schema.json"),
}

# feature value_type -> predicate the entry ``value`` must satisfy.
# Note: bool is a subclass of int in Python, so integer/number exclude it.
VALUE_TYPE_CHECKS = {
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "string": lambda v: isinstance(v, str),
    "array": lambda v: isinstance(v, list),
    # enum values are stored as strings; membership is validated below when
    # the feature's value_meta lists the allowed options.
    "enum": lambda v: isinstance(v, str),
}


def is_valid_uuid(value):
    """True if ``value`` is a well-formed UUID string."""
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def load(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)


def schema_errors(data, schema, label):
    errors = []
    validator = Draft7Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"[{label}] schema: {loc}: {err.message}")
    return errors


def enum_options(feature):
    """Return the allowed values for an enum feature, or None if unspecified."""
    meta = feature.get("value_meta")
    if isinstance(meta, dict):
        for key in ("options", "values", "enum"):
            if isinstance(meta.get(key), list):
                return meta[key]
    return None


def main():
    errors = []

    # ---- 1. Load + schema validation --------------------------------------
    loaded = {}
    parse_failed = False
    for label, (data_file, schema_file) in FILES.items():
        try:
            data = load(data_file)
        except json.JSONDecodeError as exc:
            errors.append(f"[{label}] invalid JSON in {data_file}: {exc}")
            parse_failed = True
            continue
        schema = load(schema_file)
        loaded[label] = data
        errors += schema_errors(data, schema, label)

    # Referential checks need all three files parsed.
    if parse_failed:
        return report(errors)

    impl_items = loaded["implementations"].get("items", [])
    feat_items = loaded["features"].get("items", [])
    ent_items = loaded["entries"].get("items", [])

    # ---- 2a. Unique UUIDs -------------------------------------------------
    impl_ids = {}
    for idx, impl in enumerate(impl_items):
        uid = impl.get("uuid")
        if not is_valid_uuid(uid):
            errors.append(f"[implementations[{idx}]] uuid {uid!r} is not a valid UUID")
        if uid in impl_ids:
            errors.append(
                f"[implementations] duplicate uuid {uid} "
                f"(items {impl_ids[uid]} and {idx})"
            )
        else:
            impl_ids[uid] = idx

    feat_by_id = {}
    for idx, feat in enumerate(feat_items):
        uid = feat.get("uuid")
        if not is_valid_uuid(uid):
            errors.append(f"[features[{idx}]] uuid {uid!r} is not a valid UUID")
        if uid in feat_by_id:
            errors.append(f"[features] duplicate uuid {uid}")
        else:
            feat_by_id[uid] = feat

    # ---- 2b. Entry referential integrity + value typing -------------------
    seen_pairs = {}
    for idx, ent in enumerate(ent_items):
        label = f"entries[{idx}]"
        impl_uuid = ent.get("implementation_uuid")
        feat_uuid = ent.get("feature_uuid")

        if not is_valid_uuid(impl_uuid):
            errors.append(
                f"[{label}] implementation_uuid {impl_uuid!r} is not a valid UUID"
            )
        elif impl_uuid not in impl_ids:
            errors.append(f"[{label}] implementation_uuid {impl_uuid} does not exist")
        if not is_valid_uuid(feat_uuid):
            errors.append(f"[{label}] feature_uuid {feat_uuid!r} is not a valid UUID")
        elif feat_uuid not in feat_by_id:
            errors.append(f"[{label}] feature_uuid {feat_uuid} does not exist")

        pair = (impl_uuid, feat_uuid)
        if pair in seen_pairs:
            errors.append(
                f"[{label}] duplicate entry for this "
                f"(implementation, feature); first seen at entries[{seen_pairs[pair]}]"
            )
        else:
            seen_pairs[pair] = idx

        feature = feat_by_id.get(feat_uuid)
        if feature is not None and "value" in ent:
            vtype = feature.get("value_type")
            fname = feature.get("short_name", feat_uuid)
            check = VALUE_TYPE_CHECKS.get(vtype)
            value = ent["value"]
            if check is None:
                errors.append(
                    f"[{label}] feature '{fname}' has unknown value_type '{vtype}'"
                )
            elif not check(value):
                errors.append(
                    f"[{label}] value {value!r} does not match value_type "
                    f"'{vtype}' of feature '{fname}'"
                )
            elif vtype == "enum":
                options = enum_options(feature)
                if options is not None and value not in options:
                    errors.append(
                        f"[{label}] value {value!r} is not one of the allowed "
                        f"options {options} for feature '{fname}'"
                    )

    return report(errors, impl_items, feat_items, ent_items)


def report(errors, impl_items=None, feat_items=None, ent_items=None):
    if errors:
        print(
            f"❌ Data validation failed with {len(errors)} error(s):\n",
            file=sys.stderr,
        )
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(
        "✅ Data validation passed: "
        f"{len(impl_items)} implementations, "
        f"{len(feat_items)} features, {len(ent_items)} entries."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
