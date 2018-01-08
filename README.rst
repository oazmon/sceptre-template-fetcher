=============================
Sceptre Tempalte Fetcher Tool
=============================

.. image:: https://circleci.com/gh/intuit/sceptre_template_fetcher.png?style=shield

About
-----

Sceptre Tempalte Fetcher Tool is an add-on tool for Sceptre that automates fetching 
shared templates from various types of repositories, such as github, nexus, and artifactory
into the Sceptre directory tree.

Features:

- Import based files and archives into a shared-templates directory.


Example
-------

Given how Sceptre organises configuration and templates.  Here, we have an empty environment named ``dev``::

  $ tree
  .
  ├── config
  │   └── dev
  │       └── config.yaml
  ├── templates
  └── shared-templates


Some templates are used by many project. By placing them in a shared location, such as a Github Repo, or a Nexus or Artifactory repository,
we can't keep our project DRY (Do Not Repeat). To automate the fetching and re-fetching (updates) this tool implements the ``fetch-shared-templates`` command.
Assuming an existing import configuration file ``config/import.yaml`` with a local copy configuration:

  $ sceptre_template_fetcher fetch-shared-templates
  sceptre_template_fetcher.template_fetcher - Importing templates into '.../sceptre-project/shared-templates'
  sceptre_template_fetcher.template_fetcher - Using import config '.../sceptre-project/config/import.yaml'
  sceptre_template_fetcher.fetchers - Local Copy: from=.../resources/dummy_template.yaml to=.../sceptre-project/shared-templates/local/dummy_template.yaml


Usage
-----

Sceptre Template Fetcher too can be used from the CLI, or imported as a Python package.

CLI::

    Usage: sceptre_template_fetcher [OPTIONS] COMMAND [ARGS]...
    
      Implements sceptre_template_fetcher's CLI.
    
    Options:
      --version            Show the version and exit.
      --debug              Turn on debug logging.
      --dir TEXT           Specify sceptre_migration_tool directory.
      --var TEXT           A variable to template into config files.
      --var-file FILENAME  A YAML file of variables to template into config files.
      --help               Show this message and exit.
    
    Commands:
      fetch-shared-templates  Import templates.


Python:

.. code-block:: python

  from template_fetcher import TemplateFetcher
  
  fetcher = TemplateFetcher(
     sceptre_dir='sceptre-dir'
  )
  fetcher.fetch()

A full API description of the sceptre template fetcher package can be found in the `Documentation <docs/index.html>`__.


Install
-------

::

  $ pip install sceptre_template_fetcher

More information on installing sceptre template fetcher can be found in our `Installation Guide <docs/install.html>`_.


Tutorial and Documentation
--------------------------

- `Get Started <docs/get_started.html>`_
- `Documentation <docs/index.html>`__


Contributions
-------------

See our `Contributing Guide <CONTRIBUTING.rst>`_.
