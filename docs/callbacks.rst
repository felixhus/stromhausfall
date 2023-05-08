Dash Callbacks
==============

This page contains all callbacks which are the backbone of the dash application. They are called by their ``inputs``, get their data with ``states`` and return to properties of dash components with ``outputs``.

An example callback, which takes on input and returns the values of the in put and the state to display in the output component is shown below.
More information on dash callbacks can be found in the `Dash User Guide`_, `here for basic callbacks`_ and `here for more advanced callbacks`_.

.. _Dash User Guide: https://dash.plotly.com/
.. _here for basic callbacks: https://dash.plotly.com/basic-callbacks
.. _here for more advanced callbacks: https://dash.plotly.com/advanced-callbacks

.. code-block:: python
   :linenos:

   @app.callback(
       Output('my-output', 'children'),
       Input('my-input', 'value'),
       State('my-state', 'value'),
   )
   def update_output_div(input_value, state_value):
       return f'Output: {input_value + state_value}'


.. note::
   The automatic documentation of the callback files is not as straightforward as for the others, because of nested functions. See how to do it in :ref:`Tools  <target_tools>`.

.. contents:: There are different files to structure the callbacks:

General Callbacks
-----------------

.. automodule:: general_callbacks
.. autofunction:: save_props_action

Grid Callbacks
--------------