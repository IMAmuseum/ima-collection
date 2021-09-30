# This project is no longer active, and the repo has been archived.

## Collection Metadata for the Indianapolis Museum of Art

What you see before you is the attempt to make the collection metadata for the IMA accessible in an extremely simple format.

Each json file represents a single work of art. The objects are sorted into folders by zero-padding their unique identifiers (`irn`).

Given an object's unique identifier, you can load its webpage with the following URL template:

    http://imamuseum.org/mercury/load-artwork/{irn}

Image information is coming soon, but you can easily grab the URL of the primary image for an object using the CSS selector `img.primary-mercury-image` on the objects webpage.
