from behave import *
import os
import shutil

from sceptre_template_fetcher.template_fetcher import TemplateFetcher


@given(u'"{directory}" directory does not exist')
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
    
@when(u'the user runs fetch templates with "{path}" file')
def step_impl(context, path):
    # run fetch from the specified file
    fetcher = TemplateFetcher(  
        sceptre_dir=context.sceptre_dir
    )
    fetcher.fetch(path)

@then(u'"{directory}" directory exists')
def step_impl(context, directory):
    assert os.path.isdir(os.path.join(
            context.sceptre_dir,
            directory
        )
    )

@then(u'"{file}" file exists')
def step_impl(context, file):
    path = os.path.join(
        context.sceptre_dir,
        file
    )
    print( "file exists: ", path)
    assert os.path.isfile(path)