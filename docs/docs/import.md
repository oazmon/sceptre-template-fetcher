---
layout: docs
---

# Import Config

Import config stores config related to any import of files, directories, and archives into the 'shared-template' directory.

## Structure

An import config file is a yaml object of key-value pairs configuring a list of imports. 
All import configuration must appear under the **import** key. The import key values is 
list of import directives and each element in the list is composed of the key-value pairs, such as:
- **[provider](#supported-providers)** *(optional, defaults to **github**)*
- **from** *(required)*
- **to** *(required)*

For example:

```yaml
import:
  - provider: local
    from: /absolute/path/to/template.yaml
    to: relative/path/to/template.yaml
  - provider: github
    from: organization/repo
    to: github/repo
```

### Supported Providers

The name of one of the support providers that knows how to fetch a file, directory, or archive.
The following are the supported providers included with the base package:
* **[local](#local-provider)** fetches a file and/or a directory tree from an absolute path on the local machine.
* **[github](#github-provider).** fetches a repo from Github (public and enterprise) by branch, tag, or commit id
* **[nexus](#nexus-provider)** fetches an artifact from a Sonotype Nexus repository.
* **[artifactory](#artifactory-provider)** fetches an artifact from a JFrog Artifactory repository.

The default provider is **github**.

### Local Provider
The local provider support the following keys:
* **[from](#local-from)** *(required)*
* **[to](#local-to)** *(required)*

#### Local: from
The source location for the local provider must be an absolute path to a file or directory.

#### Local: to
The target location relative to the ``shared-templates`` directory.
* For files, this is the file's relative path and name.
* For directories, this is the directory where the content of the source directory is placed.


### Gihub Provider
The Github provider support the following keys:
* **[from](#github-from)** *(required)*
* **[to](#github-to)** *(required)*
* **[github](#github-github)** *(optional)*
* **[oath](#github-oath)** *(optional)*

#### Github: from
The source location organization/repository-name to fetch. If not specified, it is fetch from ``github.com``.

#### Github: to
The target location relative to the ``shared-templates`` directory into which the context of repository is placed.

#### Github: github
An optional key to specify the url to the github to use. The default is ``https://github.com``.

#### Github: oath
An optional key to specify the oauth token to use to authenticate against Github API. This key support the following sub-keys:

* **file**:
An optional value that specify the file where the oauth token may be found. The default is ``$HOME/.ssh/sceptre_import.yaml``.

* **key**: Required, if the ``oauth`` key is used. It specify the key in the yaml file where the oauth token may be found.


### Nexus Provider
The Nexus provider support the following keys:
* **[from](#nexus-from)** *(required)*
* **[to](#nexus-to)** *(required)*
* **[repo_url](#nexus-repo_url)** *(optional)*

#### Nexus: from
The g:a:v or g:a:p:c:v for of a Nexus artifact. The default packaging is assumed to be ``jar``.

#### Nexus: to
The target location relative to the ``shared-templates`` directory into which the context of artifact is placed. If the artifact is a ``jar``, ``zip`` or ``tar`` archive, it is exploded into this location.

#### Nexus: repo_url
The optional url to the Nexus Repository. The default is ``https://repo.maven.apache.org/maven2``.

### Artifactory Provider
The Nexus provider support the following keys:
* **[from](#artifactory-from)** *(required)*
* **[to](#artifactory-to)** *(required)*

#### Artifactory: from
The Artifactory path identifying the resource to an Artifactory service.

### Artifactory: to
The target location relative to the ``shared-templates`` directory into which the context of artifact is placed. If the artifact is a ``zip`` or ``tar`` archive, it is exploded into this location.