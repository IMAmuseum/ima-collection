actors:

	bin/export-actors.py

csv:
	bin/generate-csv-actors.py

glossary:
	bin/generate-glossary.py --objects json/objects --glossary meta/objects-glossary.json
	bin/publish-glossary.py --glossary meta/objects-glossary.json --markdown meta/objects-glossary.md

	bin/generate-glossary.py --objects json/actors --glossary meta/actors-glossary.json
	bin/publish-glossary.py --glossary meta/actors-glossary.json --markdown meta/actors-glossary.md
