#!/usr/bin/env python

import json

import model

implementations, features, entries = model.get_all_data()

filename = "Implementations.json"

output = implementations

feat_remove_fields = [
    "created_at",
    "created_by",
    "value_meta",
    "value_type",
    "uuid",
    "feature_uuid",
]
prepared_features = [
    {**e, **f} for e in entries for f in features if e["feature_uuid"] == f["uuid"]
]
prepared_features = [
    {k: v for k, v in f.items() if k not in feat_remove_fields}
    for f in prepared_features
]

output = [
    {
        **o,
        "features": [
            {k: v for k, v in f.items() if k != "implementation_uuid"}
            for f in list(filter(
                lambda x: x["implementation_uuid"] == o["uuid"], prepared_features
            ))
        ],
    }
    for o in output
]

impl_remove_fields = ["uuid", "created_at", "created_by", "logo_url"]
output = [{k: v for k, v in o.items() if k not in impl_remove_fields} for o in output]

json.dump(output, open(filename, "w"), indent=4)
