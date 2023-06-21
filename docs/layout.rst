.. _target_layout:

Layout Dash App
===============

The layout of the app is mostly rendered at the first loading of the app, some components are created dynamically while running. You can find information on the different component in the comments in the code or from the following sources:

* DBC: `Dash Bootstrap Components`_
* DCC: `Dash Core Components`_
* DMC: `Dash Mantine Components`_ (Including Dash Iconify)

.. _Dash Bootstrap Components: https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/
.. _Dash Core Components: https://dash.plotly.com/dash-core-components/
.. _Dash Mantine Components: https://www.dash-mantine-components.com/

The layout is defined in ``layout.py``, whichs gets all the dash components from ``dash_components.py``.

Main Layout
-----------

.. automodule:: layout
   :members:

Dash Components
---------------

.. automodule:: dash_components
   :members:

Stylesheets
-----------

.. automodule:: stylesheets

More information can be found in the `dash documentation on stylesheets`_.

.. _dash documentation on stylesheets: https://dash.plotly.com/external-resources
