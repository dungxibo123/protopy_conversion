# protopy_conversion
A simplest version from *.proto to *.py

While doing projects at company, I fought with the Google Pub/Sub and had to start to handle Prototype message. The project led me directly into using the `proto-plus`. However, when using the `proto-plus` package, we have to have a message schema inside a `*.py` file then import it directly into the pulling services. After few hours searched the solution for converting the `*.proto` to `*.py`, I decided to wrote simple script to handle this conversion. Please take a look into the `nestedObjectParser` function inside `extract_proto.py` file and see its usages.

Feel free to contribute PRs.


Thanks!
