---
layout: page
---

# About

Sceptre Template Fetcher is a tool to import templates from external locations into Sceptre. Currently, the tool imports from the local machine, 
a GitHub repo, a Nexus repo, and an Artifactory Repo.
The tool is accessible as a CLI tool, or as a Python module.


## Motivation

Some templates are used by many independent projects, like security groups and bastion hosts. To help avoid copy-paste the fetcher is designed 
to fetch templates from a more central location.

The fetcher was developed separate from Sceptre (it imports Sceptre internally) to so that users that don't need it, don't have it.


## Overview

The import tool by default is driven by the ``config/import.yaml`` file and places the results in the ``shared-templates`` directory. After it is run,
Sceptre configurations can refer to the templates so fetched.

For a tutorial on using Sceptre, see [Get Started](https://sceptre.cloudreach.com/latest/docs/get_started.html).


## Code

Sceptre Template Fetchter source code can be found on [Github](https://github.intuit.com/SBSEG-EPIC/sceptre-template-fetcher).

Bugs and feature requests should be raised via our [Issues](https://github.intuit.com/SBSEG-EPIC/sceptre-template-fetcher/issues) page.
