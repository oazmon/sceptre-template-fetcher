---
layout: docs
---

# Get Started

## Install

This tutorial assumes that you have installed Sceptre . Instructions on how to do this are found in the section on [installation]({{ site.url }}{{ site.baseurl }}/docs/install.html).

## Directory Structure

Create the following directory structure in a clean directory named `sceptre-example`:

```shell
.
└── config
    └── import.yaml
```

On Unix systems, this can be done with the following commands:

```
$ mkdir config
$ touch config/import.yaml
```

### import.yaml

Add the following config to `import.yaml`:

```yaml
imports:
  - provider: github
    from: cloudreach/sceptre
    branch: master
    to: github/sceptre
```

This directive fetches the Sceptre repo into the shared-templates/github/sceptre directory.


## Commands


### Import stack

We can import a stack with the following command:

```shell
$ sceptre-template-fetcher fetch-shared-templates
```

This command must be run from the `sceptre-examples` directory.


## Next Steps

Further details can be found in the full [documentation]({{ site.url }}{{ site.baseurl }}/docs).
