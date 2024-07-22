#!/usr/bin/env python

import model

implementations, features, entries = model.get_all_data()

filename = "Implementations.md"

with open(filename, "w") as f:
    f.write("# QUIC Implementations\n\n")
    for implementation in implementations:
        f.write(f"## [{implementation['name']}]({implementation['repo_url']})\n\n")
        f.write(f"### General Information\n\n")
        f.write(f"- **Maintainer:** {implementation['maintainer']}\n")
        f.write(f"- **Language:** {implementation['language']}\n\n")
        implementation_features = list(filter(lambda x: x["implementation_uuid"] == implementation["uuid"], entries))
        if len(implementation_features) > 0:
            f.write(f"### Feature Information\n\n")
            for entry in implementation_features:
                feature = list(filter(lambda x: x["uuid"] == entry["feature_uuid"], features))[0]
                if feature["value_type"] == "boolean":
                    value = "Yes" if entry["value"] == "1" else "No"
                elif feature["value_type"] == "array":
                    value = ", ".join(entry["value"])
                else:
                    value = entry["value"]
                f.write(f"- **{feature['name']}**: {value}\n")
            f.write("\n")
