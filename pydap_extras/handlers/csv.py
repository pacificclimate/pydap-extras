import os
import csv
import re
import time
import copy
from stat import ST_MTIME
from email.utils import formatdate

from pydap.handlers.lib import BaseHandler, IterData, build_filter
from pydap.model import *
from pydap.lib import quote
from pydap.exceptions import OpenFileError


class CSVHandler(BaseHandler):

    """This is a simple handler for CSV files.
    Here's a standard dataset for testing sequential data:
        >>> data = [
        ... (10, 15.2, 'Diamond_St'),
        ... (11, 13.1, 'Blacktail_Loop'),
        ... (12, 13.3, 'Platinum_St'),
        ... (13, 12.1, 'Kodiak_Trail')]
        >>> import csv
        >>> temp_file = getfixture('tmpdir').join('test.csv')
        >>> with open(str(temp_file), 'w') as f:
        ...     writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        ...     row_length = writer.writerow(['index', 'temperature', 'site'])
        ...     row_length = [writer.writerow(row) for row in data]
    Iteraring over the sequence returns data:
        >>> seq = CSVHandler(str(temp_file)).dataset['sequence']
        >>> for line in seq:
        ...     print(line)
        (10.0, 15.2, 'Diamond_St')
        (11.0, 13.1, 'Blacktail_Loop')
        (12.0, 13.3, 'Platinum_St')
        (13.0, 12.1, 'Kodiak_Trail')
    The order of the variables can be changed:
        >>> for line in seq['temperature', 'site', 'index']:
        ...     print(line)
        (15.2, 'Diamond_St', 10.0)
        (13.1, 'Blacktail_Loop', 11.0)
        (13.3, 'Platinum_St', 12.0)
        (12.1, 'Kodiak_Trail', 13.0)
    We can iterate over children:
        >>> for line in seq['temperature']:
        ...     print(line)
        15.2
        13.1
        13.3
        12.1
    We can filter the data:
        >>> for line in seq[ seq.index > 10 ]:
        ...     print(line)
        (11.0, 13.1, 'Blacktail_Loop')
        (12.0, 13.3, 'Platinum_St')
        (13.0, 12.1, 'Kodiak_Trail')
        >>> for line in seq[ seq.index > 10 ]['site']:
        ...     print(line)
        Blacktail_Loop
        Platinum_St
        Kodiak_Trail
        >>> for line in seq[['site', 'temperature']][ seq.index > 10 ]:
        ...     print(line)
        ('Blacktail_Loop', 13.1)
        ('Platinum_St', 13.3)
        ('Kodiak_Trail', 12.1)
    Or slice it:
        >>> for line in seq[::2]:
        ...     print(line)
        (10.0, 15.2, 'Diamond_St')
        (12.0, 13.3, 'Platinum_St')
        >>> for line in seq[ seq.index > 10 ][::2]['site']:
        ...     print(line)
        Blacktail_Loop
        Kodiak_Trail
        >>> for line in seq[ seq.index > 10 ]['site'][::2]:
        ...     print(line)
        Blacktail_Loop
        Kodiak_Trail
    Finally, delete the data file:
        >>> temp_file.remove()
    """

    extensions = re.compile(r"^.*\.csv$", re.IGNORECASE)

    def __init__(self, filepath):
        BaseHandler.__init__(self)

        try:
            with open(filepath, 'Ur') as fp:
                reader = csv.reader(fp, quoting=csv.QUOTE_NONNUMERIC)
                vars = next(reader)
        except Exception as exc:
            message = f'Unable to open file {filepath}: {exc}'
            raise OpenFileError(message)

        self.additional_headers.append(
                ('Last-modified', (formatdate(time.mktime(time.localtime(os.stat(filepath)[ST_MTIME]))))))

        # build dataset
        name = os.path.split(filepath)[1]
        self.dataset = DatasetType(name)

        # add sequence and children for each column
        seq = self.dataset['sequence'] = SequenceType('sequence')
        for var in vars:
            seq[var] = BaseType(var)

        # set the data
        seq.data = CSVData(filepath, copy.copy(seq))

        # add extra attributes
        metadata = "{0}.json".format(filepath)
        if os.path.exists(metadata):
            with open(metadata) as fp:
                attributes = json.load(fp)
            add_attributes(self.dataset, attributes)


class CSVData(IterData):

    """Emulate a Numpy structured array using CSV files.

    Here's a standard dataset for testing sequential data:
        >>> data = [
        ... (10, 15.2, 'Diamond_St'),
        ... (11, 13.1, 'Blacktail_Loop'),
        ... (12, 13.3, 'Platinum_St'),
        ... (13, 12.1, 'Kodiak_Trail')]
        >>> import csv
        >>> temp_file = getfixture('tmpdir').join('test.csv')
        >>> with open(str(temp_file), 'w') as f:
        ...     writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        ...     row_length = writer.writerow(['index', 'temperature', 'site'])
        ...     row_length = [writer.writerow(row) for row in data]
    Iteraring over the sequence returns data:
        >>> seq = SequenceType('example')
        >>> seq['index'] = BaseType('index')
        >>> seq['temperature'] = BaseType('temperature')
        >>> seq['site'] = BaseType('site')
        >>> seq.data = CSVData(str(temp_file), copy.copy(seq))
        >>> for line in seq:
        ...     print(line)
        (10.0, 15.2, 'Diamond_St')
        (11.0, 13.1, 'Blacktail_Loop')
        (12.0, 13.3, 'Platinum_St')
        (13.0, 12.1, 'Kodiak_Trail')
    The order of the variables can be changed:
        >>> for line in seq['temperature', 'site', 'index']:
        ...     print(line)
        (15.2, 'Diamond_St', 10.0)
        (13.1, 'Blacktail_Loop', 11.0)
        (13.3, 'Platinum_St', 12.0)
        (12.1, 'Kodiak_Trail', 13.0)
    We can iterate over children:
        >>> for line in seq['temperature']:
        ...     print(line)
        15.2
        13.1
        13.3
        12.1
    We can filter the data:
        >>> for line in seq[ seq.index > 10 ]:
        ...     print(line)
        (11.0, 13.1, 'Blacktail_Loop')
        (12.0, 13.3, 'Platinum_St')
        (13.0, 12.1, 'Kodiak_Trail')
        >>> for line in seq[ seq.index > 10 ]['site']:
        ...     print(line)
        Blacktail_Loop
        Platinum_St
        Kodiak_Trail
        >>> for line in seq['site', 'temperature'][ seq.index > 10 ]:
        ...     print(line)
        ('Blacktail_Loop', 13.1)
        ('Platinum_St', 13.3)
        ('Kodiak_Trail', 12.1)
    Or slice it:
        >>> for line in seq[::2]:
        ...     print(line)
        (10.0, 15.2, 'Diamond_St')
        (12.0, 13.3, 'Platinum_St')
        >>> for line in seq[ seq.index > 10 ][::2]['site']:
        ...     print(line)
        Blacktail_Loop
        Kodiak_Trail
        >>> for line in seq[ seq.index > 10 ]['site'][::2]:
        ...     print(line)
        Blacktail_Loop
        Kodiak_Trail
    Finally, delete the data file:
        >>> temp_file.remove()

    """
    def __init__(self, filepath, template, ifilter=None, imap=None,
                 islice=None, level=0):
        self.filepath = filepath
        self.template = template
        self.level = level

        self.ifilter = ifilter or []
        self.imap = imap or []
        self.islice = islice or []

    @property
    def stream(self):
        """Generator that yield lines of the file."""
        try:
            fp = open(self.filepath, 'Ur')
        except Exception as exc:
            message = f'Unable to open file {self.filepath}: {exc}'
            raise OpenFileError(message)

        reader = csv.reader(fp, quoting=csv.QUOTE_NONNUMERIC)
        next(reader)  # consume var names
        for row in reader:
            yield row
        fp.close()

    def __copy__(self):
        """Return a lightweight copy."""
        return self.__class__(self.filepath, copy.copy(self.template),
                              self.ifilter[:], self.imap[:], self.islice[:],
                              self.level)


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    import sys
    from werkzeug.serving import run_simple

    _test()

    application = CSVHandler(sys.argv[1])
    from pydap.wsgi.ssf import ServerSideFunctions
    application = ServerSideFunctions(application)
    run_simple('localhost', 8001, application, use_reloader=True)