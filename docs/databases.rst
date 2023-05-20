Data Sources
============

The app uses different data sources and scripts to work on them. They are listed here.

Databases
---------

The following SQL-Databases are found under ``./source/database-name.db/``.

Database Profiles
~~~~~~~~~~~~~~~~~
This database is called ``database_profiles.db`` and contains the following tables:

.. csv-table::
   :header: "Table Name", "Description"

   "devices", "All devices predefined in the app with their properties."
   "device_custom", "All power profile which can be added at a specific time."
   "device_preset", "All power profile which has a length of one day."
   "device_csv_connection", "Connection between power profiles and source csv in the :ref:`Tracebase dataset  <target_tracebase>`."

The following columns exist in the table ``devices``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "type", "TEXT", "Yes", "The unique type string of a device"
   "standard_room", "TEXT", "No", "The standard room of the device, in which room menu it should appear"
   "name", "TEXT", "No", "Displayed name of the device (german)"
   "menu_type", "TEXT", "No", "``device_custom`` or ``device_preset``, defining the type of power profiles"
   "icon", "TEXT", "No", "The icon reference from Iconify"
   "power_options", "TEXT", "No", "String representation of a python dictionary with all power profiles of this device"

The following columns exist in the table ``device_custom``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a custom profile"
   "type", "TEXT", "No", "Device type which can use this profile"
   "standby_power", "FLOAT", "No", "Standby power of device when no in use"
   "step_0", "FLOAT", "No", "First timestep of power profile, power in Watts"
   "...", "...", "...", "One step per minute"
   "step_1439", "FLOAT", "No", "Last timestep of power profile, power in Watts"

The following columns exist in the table ``device_preset``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a preset profile"
   "type", "TEXT", "No", "Device type which can use this profile"
   "step_0", "FLOAT", "No", "First timestep of power profile, power in Watts"
   "...", "...", "...", "One step per minute"
   "step_1439", "FLOAT", "No", "Last timestep of power profile, power in Watts"

The following columns exist in the table ``device_csv_connection`` (see :ref:`Tracebase dataset  <target_tracebase>`):

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a profile"
   "csv_filename", "TEXT", "No", "The filename of the source file of the profile"


Database Households
~~~~~~~~~~~~~~~~~~~
This database is called ``database_izes_reduced.db`` and contains the following tables:

.. csv-table::
   :header: "Table Name", "Description"

   "load_1min", "Measured household power profiles with a time resolution of 1min for 1 year"

The following columns exist in the table ``load_1min``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "month", "INT", "No", "Month in year"
   "day", "INT", "No", "Day in month"
   "profile_4", "INT", "No", "First household profile"
   "...", "...", "...", "A total of 27 profiles, not each id is exisiting"
   "profile_73", "INT", "No", "Last household profile"

The profiles contain one year of power in Watts in 1 minute resolution. They are a selection from a dataset provided by the Institute for Future Energy Systems (IZES). The dataset and its documentation can be found `here`_. The following list of profiles is included in the reduced dataset:

``4, 7, 9, 14, 15, 16, 17, 18, 19, 20, 22, 23, 27, 28, 32, 33, 39, 41, 46, 73, 42, 45, 47, 58, 61, 62, 65``

.. _here: https://solar.htw-berlin.de/elektrische-lastprofile-fuer-wohngebaeude/

Database PV
~~~~~~~~~~~
This database is called ``database_pv.db`` and contains the following tables:

.. csv-table::
   :header: "Table Name", "Description"

   "plz_data", "Coordinates of each postcode in Germany"

The following columns exist in the table ``plz_data``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "loc_id", "INT", "No", "Location id"
   "postcode", "INT", "No", "German postcode"
   "lon", "FLOAT", "No", "Longitude of postcode"
   "lat", "FLOAT", "No", "Latitude of postcode"
   "city", "TEXT", "No", "Name of city of the postcode"

The source of this data is a data dump of the old "OpenGeoDB"-project (`Here on Github`_).

.. _Here on Github: https://github.com/brnbio/opengeodb/tree/main


SQL Modules
----------------

.. automodule:: sql_modules
   :members:

Renewables.ninja
----------------

The solar power data is fetched from the `Renewables.ninja`_ service. This is done with an API key. 

.. note:: The number of requests is limited to 50/hour.

The code for getting the data can be found in :meth:`modules.save_settings_pv`:

.. code-block:: python
   :linenos:

   token_rn = 'your-api-token'   # Authorization renewables.ninja
   sess = requests.session()
   sess.headers = {'Authorization': 'Token ' + token_rn}
   url = 'https://www.renewables.ninja/api/data/pv'
   query_params = {
      # Set all parameters in here (see source code)
   }
   response = sess.get(url, params=query_params)   # Send the GET request and get the response

.. _Renewables.ninja: https://www.renewables.ninja/

.. _target_tracebase:

Tracebase Dataset
-----------------

"The tracebase data set is a collection of power consumption traces which can be used in energy analytics research. Traces have been collected from individual electrical appliances, at an average reporting rate of one sample per second." - Readme of Tracebase

You can find the documentation and data in the |github-icon| `Tracebase Github repsitory`_. The complete reference is given :ref:`here  <target_references>`

.. _Tracebase Github repsitory: https://github.com/areinhardt/tracebase

.. |github-icon| image:: _static/github-mark.png
   :scale: 8 %

The resolution of in average one second is way to high for this project. This is why the used profiles were resampled to 1min resolution using ``pandas.DataFrame.resample``. You can find an example for the resampling in :meth:`house_callbacks.add_new_device`.

