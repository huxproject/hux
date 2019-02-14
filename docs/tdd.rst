======================
Test-drive development
======================
unittest
--------
Unit test can make sure your package's API is compatible and is very useful
when you need to refactor your project. Since it is optional, it is better
than no choice.

unittest.mock
-------------
Mock takes an important role in test case which rarely happend or consume lots
of resource. A mock can easily make up any resource you intend to test. For
example, if you want to test you application how to handle exception, there
are not alway exception happend, you can mock something bad happend.

doctest
-------
I personally thought that doctest is a good company with unittest, and usually
perform as a bridge between TDD and DDD. One more thing need pay attension,
as document, it is better practice that show the correct usage than exception,
therefore, I prefer to put the exception test in unittest and the usage in
doctest.

Why not nose/pytest?
--------------------
Since ``unittest`` and ``doctest`` provide all the features I need currently,
there are no need to introduce new packages.
