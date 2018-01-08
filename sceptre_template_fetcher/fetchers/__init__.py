# -*- coding: utf-8 -*-
import abc
import io
import logging
from os import path
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
    def __init__(self, sceptre_dir, shared_template_dir):
        self.logger = logging.getLogger(__name__)
        self.sceptre_dir = sceptre_dir
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
        target = import_spec['to']
        target = path.join(
            self.shared_template_dir,
            target
        )
        self.logger.info("to=%s", target)
        if source_extension in ["zip"]:
            with ZipFile(io.BytesIO(source_content)) as zf:
                for f in zf.filelist:
                    f.filename = self.process_filename(f.filename)
                    if f.filename:
                        zf.extract(f, target)
        elif source_extension in ["tar", "tar.gz", "tgz"]:
            with tarfile.open(
                mode='r:*',
                fileobj=io.BytesIO(source_content)
            ) as tf:
                for f in tf.get_members():
                    f.name = self.process_filename(f.name)
                    if f.name:
                        tf.extractfile(f, target)
        else:
            with open(target, 'wb') as fobj:
                fobj.write(source_content)

    # To allow sub-classes to modify filename before unzip/untar
    def process_filename(self, filename):
        return filename


class FetcherMap(object):
    def __init__(self, sceptre_dir, shared_template_dir):
        self.logger = logging.getLogger(__name__)
        self.sceptre_dir = sceptre_dir
        self.shared_template_dir = shared_template_dir
        self._map = {}
        for entry_point in iter_entry_points(
            "sceptre_template_fetcher.fetchers"
        ):
            name = entry_point.name.split('=')[0]
            self._map[name] = entry_point.load()
            self.logger.info('loaded fetcher: %s', name)

    def fetch(self, import_spec):
        fetcher_name = import_spec.get('provider', 'git')
        if fetcher_name not in self._map:
            raise KeyError(
                '{} is not a valid fetcher: {}'.format(
                    fetcher_name, self._map.keys()
                )
            )
        fetcher_class = self._map[fetcher_name]
        fetcher = fetcher_class(self.sceptre_dir, self.shared_template_dir)
        fetcher.fetch(import_spec)
