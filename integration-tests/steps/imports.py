from behave import given, when, then
import os
import shutil

from sceptre_template_fetcher.template_fetcher import TemplateFetcher


@given(u'"{directory}" directory does not exist')  # noqa: F811
def step_impl(context, directory):
    dir_path = os.path.join(
        context.sceptre_dir,
        directory
    )
    shutil.rmtree(
        dir_path,
        True
    )
    assert not os.path.isdir(dir_path)


@when(u'the user runs fetch templates with "{path}" file')  # noqa: F811
def step_impl(context, path):
    # run fetch from the specified file
    fetcher = TemplateFetcher(
        sceptre_dir=context.sceptre_dir
    )
    fetcher.fetch(path)


@then(u'"{directory}" directory exists')  # noqa: F811
def step_impl(context, directory):
    assert os.path.isdir(os.path.join(
            context.sceptre_dir,
            directory
        )
    )


@then(u'"{file}" file exists')  # noqa: F811
def step_impl(context, file):
    path = os.path.join(
        context.sceptre_dir,
        file
    )
    assert os.path.isfile(path)
