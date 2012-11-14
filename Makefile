actors:

	bin/export-actors.py --objects json/objects --actors json/actors

csv:
	bin/generate-csv-actors.py

glossary:
	bin/generate-glossary.py --objects objects --glossary meta/objects-glossary.json
	bin/publish-glossary.py --glossary meta/objects-glossary.json --markdown meta/objects-glossary.md

	bin/generate-glossary.py --objects actors --glossary meta/actors-glossary.json
	bin/publish-glossary.py --glossary meta/actors-glossary.json --markdown meta/actors-glossary.md
