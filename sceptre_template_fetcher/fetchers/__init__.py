# -*- coding: utf-8 -*-
import abc
import io
import logging
from pkg_resources import iter_entry_points
import six
import tarfile
from zipfile import ZipFile


@six.add_metaclass(abc.ABCMeta)
class Fetcher():
    """
    Fetcher is an abstract base class that should be inherited by all
    fetchers.

    """
    def __init__(self, shared_template_dir):
        self.logger = logging.getLogger(__name__)
        self.shared_template_dir = shared_template_dir

    @abc.abstractmethod
    def fetch(self, import_spec):
        """
        An abstract method which must be overwritten by all inheriting classes.
        This method is called to fetch a templete into the shared-templates
        directory.
        Implementation of this method in subclasses must fetch the requested
        template/s or raise an Exception to indicate they are unable to
        resolve.

        :param import_spec: Arguments to pass to the resolver.
        :type import_spec: dict
        """
        pass  # pragma: no cover


@six.add_metaclass(abc.ABCMeta)
class RemoteFetcher(Fetcher):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(RemoteFetcher, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def remote_fetch(self, import_spec):
        """
        An abstract method which must be overwritten by all inheriting classes.
        This method is called to fetch a template from a remote location..
        Implementation of this method in subclasses must fetch the requested
        template/s or raise an Exception to indicate they are unable to
        resolve.

        :param import_spec: Arguments to pass to the resolver.
        :type import_spec: dict
        """
        pass  # pragma: no cover

    def fetch(self, import_spec):
        source_extension, source_content = self.remote_fetch(import_spec)
        target_name = import_spec['to']
        if source_extension in ["zip"]:
            with ZipFile(io.BytesIO(source_content)) as zf:
                zf.extractall(target_name)
        elif source_extension in ["tar", "tar.gz", "tgz"]:
            with tarfile.open(
                mode='r:*',
                fileobj=io.BytesIO(source_content)
            ) as tf:
                tf.extractall(target_name)
        else:
            with open(target_name, 'wb') as fobj:
                fobj.write(source_content)


class FetcherMap(object):
    def __init__(self, shared_template_dir):
        self.logger = logging.getLogger(__name__)
        self.shared_template_dir = shared_template_dir
        self._map = {}
        for entry_point in iter_entry_points(
            "sceptre_template_fetcher.fetchers"
        ):
            self._map[entry_point.name] = entry_point.load()

    def fetch(self, import_spec):
        fetcher_name = import_spec.get('provider', 'git')
        fetcher_class = self._map[fetcher_name]
        fetcher = fetcher_class(self.shared_template_dir)
        fetcher.fetch(import_spec)