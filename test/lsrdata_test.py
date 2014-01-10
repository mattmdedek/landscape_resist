#!/usr/bin/python

import unittest
import os
import sys

sys.path.append('../script')
import lsrdata

class TestLsrDataModuleFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_dist_metric_path(self):
        self.assertRaises(
          lsrdata.ConfigFileMissingError,
          lsrdata.get_dist_metric_path,
          'some', 'thing', 'never', 'happens'
        )

        self.assertEqual(
          lsrdata.get_dist_metric_path(
            'testsite', 'tmetric', 'tspec', 'matrix', 'data/'
          ),
          (
            'matrix',
            os.path.join(
              'data/sites/testsite/' +
              '_'.join(['testsite', 'tmetric', 
                        'tspec', 'matrix_resistances'])
            )
          )
        )

        self.assertEqual(
          lsrdata.get_dist_metric_path(
            'testsite', 'tmetric', 'tspec', 'columnar', 'data/'
          ),
          (
            'columnar', 
            os.path.join(
              'data/sites/testsite/' + 
              '_'.join(['testsite', 'tmetric', 
                        'tspec', 'columnar_resistances_3columns'])
            )
          )
        )

    def test_get_dist_path(self):
        self.assertRaises(
          lsrdata.ConfigFileMissingError,
          lsrdata.get_dist_path,
          'never', 'happens'
        )

        self.assertEqual(
          lsrdata.get_dist_path(
            'testsite', 'euclidean', 'data/'
          ),
          (
            'matrix',
            os.path.join('data/sites/', 'euclidean.txt')
          )
        )

    def test_get_gdist_path(self):
        self.assertRaises(
          lsrdata.ConfigFileMissingError,
          lsrdata.get_gdist_path,
          'never', 'happens', 'ever'
        )

        self.assertEqual(
          lsrdata.get_gdist_path(
            'testsite', 'tspecies', 'rousset', 'data/'
          ),
          (
            'matrix',
            os.path.join(
              'data/samples/genetic_dist/' +
              '_'.join(['testsite', 'tspecies', 'rousset.txt'])
            )
          )
        )

    def test_sample_arrays_to_dict(self):
        test_ret = ( {
                    "TestSample1": {
                        "SampleID": "TestSample1",
                        "FieldSiteID": "TestSite1",
                        "ArrayID": "TestArray1"
                    },
                    "TestSample2": {
                        "SampleID": "TestSample2",
                        "FieldSiteID": "TestSite2",
                        "ArrayID": "TestArray2"
                    }
                  } )
        self.assertEqual(
                lsrdata.sample_arrays_to_dict("data/samples/sample_arrays_ok.txt"),
                test_ret
                )

        self.assertEqual(
                lsrdata.sample_arrays_to_dict("data/samples/sample_arrays_no_head.txt"),
                test_ret
                )

        self.assertRaises(lsrdata.ConfigFileMissingError,
                lsrdata.sample_arrays_to_dict,
                "data/samples/not_a_file.txt")

        self.assertRaises(lsrdata.DuplicateConfigKeyError,
                lsrdata.sample_arrays_to_dict,
                "data/samples/sample_arrays_dup.txt")

if __name__=='__main__':
    unittest.main()

