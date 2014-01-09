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

if __name__=='__main__':
    unittest.main()

