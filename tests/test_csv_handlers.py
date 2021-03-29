"""Test the DAP handler, which forms the core of the client."""

import numpy as np

from pydap_extras.handlers.csv import CSVHandler
from pydap.handlers.dap import DAPHandler


def test_open(simple_data, simple_data_file):
    """Test that dataset has the correct data proxies for grids."""
    dataset = DAPHandler("http://localhost:8001/",
                         CSVHandler(simple_data_file)).dataset
    seq = dataset['sequence']
    dtype = [('index', '<i4'),
             ('temperature', '<f8'),
             ('site', 'S40')]
    retrieved_data = [line for line in seq]

    np.testing.assert_array_equal(np.array(retrieved_data, dtype=dtype),
                                  np.array(simple_data, dtype=dtype))


def test_combined_slice(simple_data, simple_data_file):
    """Test that dataset has the correct data proxies for grids."""
    dataset = CSVHandler(simple_data_file).dataset
    seq = dataset['sequence']
    retrieved_data = [line for line
                      in seq[seq['index'] > 10]['temperature', 'site']]

    dtype = [('temperature', '<f8'),
             ('site', 'S40')]

    np.testing.assert_array_equal(
                np.array(retrieved_data, dtype=dtype),
                np.array([item[1:] for item in simple_data[1:]],
                         dtype=dtype))


def test_constrained(simple_data, simple_data_file):
    """Test that dataset has the correct data proxies for grids."""
    dataset = CSVHandler(simple_data_file).dataset
    seq = dataset['sequence']
    retrieved_data = [line for line
                      in seq[seq['index'] > 10]['site'][::2]]

    dtype = 'S40'

    np.testing.assert_array_equal(
                np.array(retrieved_data, dtype=dtype),
                np.array([simple_data[idx][-1] for idx in [1, 3]],
                         dtype=dtype))