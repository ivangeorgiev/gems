import io
import unittest

class TestInMemoryTextIO(unittest.TestCase):
    """StringIO"""

    def test_read_Should_ReadFromString_Given_StringIOCreatedWithString(self):
        string_data = 'Little bird'
        with io.StringIO(string_data) as input_file:
            data_read = input_file.read()
        self.assertEqual('Little bird', data_read)

    def test_getvalue_Should_ReturnDataWritten_Given_DataIsWrittenToFile(self):
        with io.StringIO() as output_file:
            output_file.write('Welcome\n')
            output_file.write('back\n')
            data_written = output_file.getvalue()
        self.assertEqual('Welcome\nback\n', data_written)

    def test_getvalue_Should_RaiseException_Given_OutputFileIsClosed(self):
        with io.StringIO() as output_file:
            output_file.write('Welcome\n')
            output_file.write('back\n')
        with self.assertRaises(ValueError) as excinfo:
            data_written = output_file.getvalue()
        self.assertEqual('I/O operation on closed file', str(excinfo.exception))

class TestInMemoryBytesIO(unittest.TestCase):

    def test_read_Should_ReadFromBytes_Given_BytesIOObjectIsCreatedWithBytes(self):
        bytes_data = b'pretty bytes'
        with io.BytesIO(bytes_data) as input_file:
            data_read = input_file.read()
        self.assertEqual(b'pretty bytes', data_read)

    def test_getvalue_Should_ReturnBytesWritten_Given_BytesAreWrittenToBytesIO(self):
        bytes_data = b'pretty bytes'
        with io.BytesIO() as output_file:
            output_file.write(b'new bytes')
            bytes_written = output_file.getvalue()
        self.assertEqual(b'new bytes', bytes_written)

if __name__ == "__main__":
    unittest.main(verbosity=2)

