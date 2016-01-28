##django_schema_explorer

django_schema_explorer is a Django-based simple tool to visualize the structure of a relational database.
For each table in the database it displays the description of the table, a summary table with column names, django model field names, data types, field/column descriptions and the list of related tables.
The summary and table relationships are further visualized on a SVG format diagram.

A working example of django_schema_explorer can be found here: [Geoscience collections of Estonia](https://schema.geokogud.info)

django_schema_explorer can be used side by side with an existing Django-based application by utilizing its already-defined models. Alternatively, if using it as a standalone application, you can let Django to introspect your existing database and create models for you (see instructions [here](https://docs.djangoproject.com/en/1.8/howto/legacy-databases/#auto-generate-the-models)).



####Installation
Running the example code requires the following software to be installed (tested on software versions specified below):

Python 3

django 1.8 ([https://docs.djangoproject.com/en/1.8/topics/](https://docs.djangoproject.com/en/1.8/topics/))

pygraphviz 1.3.1 ([http://pygraphviz.github.io](http://pygraphviz.github.io), requires graphviz [www.graphviz.org/](http://www.graphviz.org/))

If you have copied the code to your server, make sure that your browser (e.g. user 'www-data' in Ubuntu) has write rights in django_schema_explorer/static/schema_imgs directory and apps/schema/graph.dot file.

The code utilizes an example models.py located in apps/schema/. Replace it with your own models.py file or use one from your existing Django application. For that, register your existing application in django_schema_explorer/settings.py at INSTALLED_APPS next to apps.schema and change import statement in apps/schema/views.py from 'from apps.schema import models' to 'from apps.*your_model* import models'.

In django_schema_explorer/local_settings.py fill in the data for your database connections.

For displaying optional descriptions of tables and fields use models DbTables and TableFields from example models.py file. Also, create database tables db_tables and table_fields with appropriate structure and fill with data. In settings.py define DbTables and TableFields in settings TABLE_DESCRIPTION_MODEL and FIELD_DESCRIPTION_MODEL, respectively. If not using this feature, leave the parameter strings empty (' '). Displaying the Description column in the summary table is then disabled.

Other settings in Custom settings section in settings.py:

EXCLUDE_LIST: models defined here will not appear in the django_schema_explorer, including lists of referencing tables and fields of other models that refer to them.

URL_ROOT: the root part of resource urls. For example, if set to 'schema.example.com', resources appear at 'schema.example.com/*table_name*'.





 
