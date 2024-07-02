#!/usr/bin/env python
 
import subprocess

import model

try:
    username = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
    email = subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
except subprocess.CalledProcessError:
    username, email = "Anonymous", "anonymous@example.com"

user = f"{username} <{email}>"
    
implementations = model.QUICImplementation._data["items"]
features = model.QUICFeature._data["items"]

print("\nUse this tool to add a new info entry to the database.")
print("\nStep 1 - Select the implementation for which you want to add information:")

print("\n\tImplementations:")
for index, implementation in enumerate(implementations):
    print(f"\t\t[{index+1}] {implementation['name']} by {implementation['maintainer']} ({implementation['repo_url']})")

try:
    selected_implementation = implementations[int(input("\nSelect an implementation by entering its index: "))-1]
except:
    print("\nInvalid input. Please try again.")
    exit()

print(f"\nYou have selected: {selected_implementation['name']}")

print("\nStep 2 - Select the feature for which you want to add information:")

print("\n\tFeatures:")
for index, feature in enumerate(features):
    print(f"\t\t[{index+1}] {feature['name']} ({feature['description']})")

try:
    selected_feature = features[int(input("\nSelect a feature by entering its index: "))-1]
except:
    print("\nInvalid input. Please try again.")
    exit()

print(f"\nYou have selected: {selected_feature['name']}")

exists = len([i for i in model.QUICInfo._data["items"] if i["implementation_uuid"] == selected_implementation["uuid"] and i["feature_uuid"] == selected_feature["uuid"]]) > 0
if exists:
    overwrite = input("\nATTENTION: An entry for this implementation and feature already exists. It will be overwritten. Do you want to continue? [Y/n]")
    if (overwrite.lower() == "n"):
        exit()

feature_type = selected_feature["value_type"]
print("\nStep 3 - Enter the value for the feature. The value should be of the following type:", feature_type)
if feature_type == "boolean":
    value = input("\nEnter 'Y' for yes or 'N' for no: ").lower() in ["y", "t", "1"]
if feature_type == "string":
    value = input("\nEnter any string: ")
if feature_type == "number":
    try:
        value = float(input("\nEnter any number: "))
    except:
        print("\nThis does not look like a number. Please try again. Valid examples include: 1, 1.25, 1e-3")
        exit()
if feature_type == "integer":
    try:
        value = int(input("\nEnter any integer: "))
    except:
        print("\nThis does not look like an integer. Please try again.")
        exit()

if feature_type == "array":
    try:
        value = input("\nEnter a list of strings, separated by a comma (example: 'CUBIC, BBR'): ")
        value = [v.strip() for v in value.split(",")]
        value = list(map(lambda v: int(v) if v.isdigit() else v, value))
    except:
        print("\nThis does not look like an array. Please try again.")
        exit()
print("\nYou have entered:", value)

print("\nStep 4 - Enter the source of the information:")

source_url = input("\nEnter the source URL that proves this information: ")
source = input("\nEnter the type of the source (e.g. 'Repo' or 'Blog'): ")

print("\nStep 5 - Confirm and save the entry:")

print("\nYou have entered the following information:")
print(f"\n\tImplementation: {selected_implementation['name']}")
print(f"\tFeature: {selected_feature['name']}")
print(f"\tValue: {value}")
print(f"\tSource: {source}")
print(f"\tSource URL: {source_url}")

if input("\nPress Enter to save the entry. Press Ctrl+C to cancel.") == "":
    item = model.QUICInfo(
                    selected_implementation["uuid"],
                    selected_feature["uuid"],
                    value,
                    source,
                    source_url,
                    user=user
                )
    item.save_to_json()
    print("\nEntry saved successfully.")
    print("\nDon't forget to commit and push the changes to the repository.\n")
    