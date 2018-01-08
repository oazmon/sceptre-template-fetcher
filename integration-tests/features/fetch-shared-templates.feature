Feature: Fetch Templates

  # LOCAL
  Scenario: fetch a template file from local file system into shared-templates directory
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_local_file.yaml" file
    Then "shared-templates/local/dummy_template.yaml" file exists

  Scenario: fetch a template dir from local file system into shared-templates directory
    Given "shared_templates" directory does not exist
    When the user runs fetch templates with "resources/import_local_dir.yaml" file
    Then "shared-templates/local/dummy_template_dir" directory exists
    and "shared-templates/local/dummy_template_dir/dummy_template.yaml" file exists

  # GITHUB
  Scenario: fetch a template repo from public Github by branch
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_github_branch.yaml" file
    Then "shared-templates/github/Makefile" file exists

  Scenario: fetch a template repo from public Github by tag
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_github_tag.yaml" file
    Then "shared-templates/github/Makefile" file exists

  Scenario: fetch a template repo from Github by commit id
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_github_commit_id.yaml" file
    Then "shared-templates/github/Makefile" file exists

  Scenario: fetch a template repo from Github using Github API
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_github_api.yaml" file
    Then "shared-templates/github/Makefile" file exists

  #Sonotype Nexus
  Scenario: fetch a template repo from Nexus
    Given "shared-templates" directory does not exist
    When the user runs fetch templates with "resources/import_sonotype_nexus.yaml" file
    Then "shared-templates/nexus/META-INF/MANIFEST.MF" file exists

  #Artifactory
  ## Can't test as we don't have one yet
