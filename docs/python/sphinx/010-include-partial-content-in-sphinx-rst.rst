***********************************************************
Include (full or partial) Content from File into Sphinx RST
***********************************************************

.. contents:: :local:


``:include:`` for concatenating RST for rendering
=================================================



Code:


.. code-block:: rst

    .. include:: partials/example-inclusion.rstinc


Rendered:

    .. include:: partials/example-inclusion.rstinc


Reference: https://docutils.sourceforge.io/docs/ref/rst/directives.html#include




``:literalinclude:`` for including file as code block
=====================================================




Code:


.. code-block:: rst

    .. literalinclude:: partials/example-inclusion.rstinc
       :language: rst


Rendered:

    .. literalinclude:: partials/example-inclusion.rstinc
       :language: rst


Reference: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude



Including code block excerpts
-----------------------------

.. code-block:: rst

    .. literalinclude:: events.py
       :language: python
       :emphasize-lines: 3,6-8
       :linenos:

It is possible to include only Python objects, line ranges etc. Check the `documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude>`__ for more details.

