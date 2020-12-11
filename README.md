scte
====

Python library to work with SCTE standards.

License
-------

Commercial and private use are permitted. Distribution, modification, and sublicensing are all forbidden. Copyright details can be found in the file LICENSE.md.


Install
-------

Install the library and command-line utilities with <code>pip install scte</code>


Documentation
-------------

v1.1.2 includes a partial implementation of a SCTE-35 decoder that accepts as input:
- base64 strings
- hex strings
- dictionary objects representing a SpliceEvent

v1.1.2 supports Splice Insert and Time Signal messages

The decoder implementation follows [SCTE-35 2017](https://www.scte.org/SCTEDocs/Standards/SCTE%2035%202017.pdf)


Contribute
----------

Please fork the GitHub project (https://github.com/jamesfining/scte), add tests, make any changes, commit and push to GitHub, and submit a pull request.


Contact
-------

This project was initiated by James Fining.

* Email:
  * james.fining@nbcuni.com
* Github:
  * https://github.com/jamesfining
