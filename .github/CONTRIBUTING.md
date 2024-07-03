# Contributing to QUIC Explorer

It's great to hear that you want to contribute to this project.
The contribution guidelines are not yet written, so if you want to contribute, just do anything you consider useful and create a PR.

## Basic HowTo's

### Add A Feature

These is no automated way to achieve that yet, so just go to [`data/features.json`](../data/features.json) and copy an existing entry. Make sure to adjust name/date and to add a new and valid UUIDv4. You can use [uuidgenerator.net](https://www.uuidgenerator.net/version4) to quickly generate one. Take a look at [`data/features.schema.json`](../data/features.schema.json) to understand the schema used. Your IDE might also be able to lint the json files for you.

### Add An Implementation

Just read the paragraph above and replace "feature" with "implementation" for basic instructions.

### Add Information

This is where it gets (a little more) convenient. Run [`cli/simple_cli.py`](../cli/simple_cli.py) and enter the information the script asks you for. The script should run out-of-the-box with Python 3.

## Other Contributions

Feel free to create a PR or an issue with arbitrary content! No matter if you fixed a typo or completely rewrote the whole thing, just create a PR.