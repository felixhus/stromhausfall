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


Database Scripts
----------------

Renewables.ninja
----------------

.. _target_tracebase:
Tracebase Dataset
-----------------