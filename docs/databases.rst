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

The following column exist in the table ``devices``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "type", "TEXT", "Yes", "The unique type string of a device"
   "standard_room", "TEXT", "No", "The standard room of the device, in which room menu it should appear"
   "name", "TEXT", "No", "Displayed name of the device (german)"
   "menu_type", "TEXT", "No", "``device_custom`` or ``device_preset``, defining the type of power profiles"
   "icon", "TEXT", "No", "The icon reference from Iconify"
   "power_options", "TEXT", "No", "String representation of a python dictionary with all power profiles of this device"

The following column exist in the table ``device_custom``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a custom profile"
   "type", "TEXT", "No", "Device type which can use this profile"
   "standby_power", "FLOAT", "No", "Standby power of device when no in use"
   "step_0", "FLOAT", "No", "First timestep of power profile, power in Watts"
   "...", "...", "...", "One step per minute"
   "step_1439", "FLOAT", "No", "Last timestep of power profile, power in Watts"

The following column exist in the table ``device_preset``:

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a preset profile"
   "type", "TEXT", "No", "Device type which can use this profile"
   "step_0", "FLOAT", "No", "First timestep of power profile, power in Watts"
   "...", "...", "...", "One step per minute"
   "step_1439", "FLOAT", "No", "Last timestep of power profile, power in Watts"

The following column exist in the table ``device_csv_connection`` (see :ref:`Tracebase dataset  <target_tracebase>`):

.. csv-table::
   :header: "Name", "Datatype", "Primary Key", "Description"
   
   "series_id", "TEXT", "No", "The unique string id of a profile"
   "csv_filename", "TEXT", "No", "The filename of the source file of the profile"


Database Households
~~~~~~~~~~~~~~~~~~~

Database PV
~~~~~~~~~~~

Database Scripts
----------------

Renewables.ninja
----------------

.. _target_tracebase:
Tracebase Dataset
-----------------

.. _database-documentation:

Database Documentation
=======================

This document contains documentation for an existing SQL database. The documentation includes a summary of each table, column, and constraint in the database.

.. note::
   This documentation was generated automatically and may not be up-to-date or complete. Use with caution.

Table Summaries
---------------

The following tables exist in the database:

.. csv-table::
   :header: "Table Name", "Description"

   "users", "Table containing user account information."
   "posts", "Table containing blog posts."
   "comments", "Table containing comments on blog posts."

Column Summaries
----------------

The following columns exist in the database:

.. csv-table::
   :header: "Table Name", "Column Name", "Data Type", "Nullable", "Description"

   "users", "id", "INTEGER", "NO", "Primary key of the user record."
   "users", "username", "VARCHAR(64)", "NO", "Username of the user."
   "users", "password", "VARCHAR(128)", "NO", "Password hash of the user."
   "users", "email", "VARCHAR(120)", "NO", "Email address of the user."
   "users", "created_on", "TIMESTAMP", "NO", "Date/time the user record was created."
   "users", "last_login", "TIMESTAMP", "YES", "Date/time the user last logged in."
   "users", "is_admin", "BOOLEAN", "NO", "Flag indicating if the user is an administrator."
   "posts", "id", "INTEGER", "NO", "Primary key of the blog post record."
   "posts", "title", "VARCHAR(100)", "NO", "Title of the blog post."
   "posts", "body", "TEXT", "NO", "Body of the blog post."
   "posts", "created_on", "TIMESTAMP", "NO", "Date/time the blog post record was created."
   "posts", "author_id", "INTEGER", "NO", "Foreign key referencing the user who authored the blog post."
   "comments", "id", "INTEGER", "NO", "Primary key of the comment record."
   "comments", "body", "TEXT", "NO", "Body of the comment."
   "comments", "created_on", "TIMESTAMP", "NO", "Date/time the comment record was created."
   "comments", "author_id", "INTEGER", "NO", "Foreign key referencing the user who authored the comment."
   "comments", "post_id", "INTEGER", "NO", "Foreign key referencing the blog post on which the comment was made."

Constraint Summaries
--------------------

The following constraints exist in the database:

.. csv-table::
   :header: "Table Name", "Constraint Name", "Type", "Columns"

   "users", "users_pkey", "Primary Key", "id"
   "posts", "posts_pkey", "Primary Key", "id"
   "comments", "comments_pkey", "Primary Key", "id"
   "posts", "posts_author_id_fkey", "Foreign Key", "author_id"
   "comments", "comments_author_id_fkey", "Foreign Key", "author_id"
   "comments", "comments_post_id_fkey", "Foreign Key", "post_id"

