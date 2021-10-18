"""Test cmr_association_diff module"""

import json
import os
import unittest
import sys
from io import StringIO

import cmr
from mock import patch
from podaac import cmr_association_diff


class Capturing(list):
    """Class to capture print stdout"""

    def __enter__(self):
        self._stdout = sys.stdout  # pylint: disable=W0201
        sys.stdout = self._stringio = StringIO()  # pylint: disable=W0201
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class MockArgs():  # pylint: disable=R0903
    """Class to mock arguments"""

    def __init__(self, concept_id, umm_type):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.env = 'ops'
        self.concept_id = concept_id
        self.type = umm_type
        self.assoc = dir_path + '/association.txt'


class TestCmrAssociationDiff(unittest.TestCase):
    """Class to test cmr_association_diff module"""

    @patch('cmr.queries.ToolQuery.get')
    def test_pull_tool_concept_id(self, mock_method):
        """test pull concept id for tool"""

        mock_method.return_value = [{'concept_id': 'T1234'}]
        tool_concept_id = cmr_association_diff.pull_concept_id(
            cmr.queries.CMR_OPS, 'test', 'test', 'tool')
        self.assertEqual(tool_concept_id, 'T1234')

    @patch('cmr.queries.ToolQuery.get')
    def test_pull_tool_concept_id_multiple(self, mock_method):
        """test pull concept id for tool return multiple"""

        mock_method.return_value = [
            {'concept_id': 'T1234'}, {'concept_id': 'T1234'}]
        with self.assertRaises(Exception):
            cmr_association_diff.pull_concept_id(
                cmr.queries.CMR_OPS, 'test', 'test', 'tool')

    @patch('cmr.queries.ToolQuery.get')
    def test_pull_tool_concept_id_none(self, mock_method):
        """test pull concept id for tool none return"""

        mock_method.return_value = []
        with self.assertRaises(Exception):
            cmr_association_diff.pull_concept_id(
                cmr.queries.CMR_OPS, 'test', 'test', 'tool')

    @patch('cmr.queries.ServiceQuery.get')
    def test_pull_service_concept_id(self, mock_method):
        """test pull concept id for service"""

        mock_method.return_value = [{'concept_id': 'S1234'}]
        service_concept_id = cmr_association_diff.pull_concept_id(
            cmr.queries.CMR_OPS, 'test', 'test', 'service')
        self.assertEqual(service_concept_id, 'S1234')

    @patch('cmr.queries.ServiceQuery.get')
    def test_pull_service_concept_id_multiple(self, mock_method):
        """test pull concept id for service return multiple"""

        mock_method.return_value = [
            {'concept_id': 'S1234'}, {'concept_id': 'S1234'}]
        with self.assertRaises(Exception):
            cmr_association_diff.pull_concept_id(
                cmr.queries.CMR_OPS, 'test', 'test', 'service')

    @patch('cmr.queries.ServiceQuery.get')
    def test_pull_service_concept_id_none(self, mock_method):
        """test pull concept id for service return none"""

        mock_method.return_value = []
        with self.assertRaises(Exception):
            cmr_association_diff.pull_concept_id(
                cmr.queries.CMR_OPS, 'test', 'test', 'service')

    def test_cmr_environment_url_ops(self):
        """test getting ops cmr environment"""

        ops_env = cmr_association_diff.cmr_environment('ops')
        self.assertEqual(ops_env, cmr.queries.CMR_OPS)

    def test_cmr_environment_url_uat(self):
        """test getting uat cmr environment"""

        uat_env = cmr_association_diff.cmr_environment('uat')
        self.assertEqual(uat_env, cmr.queries.CMR_UAT)

    def test_cmr_environment_url_exception(self):
        """test getting invalid cmr environment"""

        with self.assertRaises(Exception):
            cmr_association_diff.cmr_environment('Exception')

    @patch('cmr.queries.CollectionQuery.get')
    def test_current_association_tool(self, mock_method):
        """test getting current association for tool"""

        mock_method.return_value = [
            {'id': 'T1234'}, {'id': 'T2234'}, {'id': 'T3334'}]
        tool_concept_ids = cmr_association_diff.current_association(
            'T1234', cmr.queries.CMR_OPS, 'tool')
        self.assertEqual(['T1234', 'T2234', 'T3334'], tool_concept_ids)

    @patch('cmr.queries.CollectionQuery.get')
    def test_current_association_service(self, mock_method):
        """test getting current association for service"""

        mock_method.return_value = [
            {'id': 'S1234'}, {'id': 'S2234'}, {'id': 'S3334'}]
        service_concept_ids = cmr_association_diff.current_association(
            'S1234', cmr.queries.CMR_OPS, 'service')
        self.assertEqual(['S1234', 'S2234', 'S3334'], service_concept_ids)

    @patch('podaac.cmr_association_diff.parse_args')
    @patch('podaac.cmr_association_diff.current_association')
    def test_run_tool(self, mock_current_association, mock_parse):
        """test run for tool"""

        fake_args = MockArgs('T1234', 'tool')
        mock_parse.return_value = fake_args
        mock_current_association.return_value = ['T5555']
        with Capturing() as output:
            cmr_association_diff.run()
        self.assertEqual(json.loads(output[0]), ['T5555'])

    @patch('podaac.cmr_association_diff.parse_args')
    @patch('podaac.cmr_association_diff.current_association')
    def test_run_service(self, mock_current_association, mock_parse):
        """test run for service"""

        fake_args = MockArgs('S1234', 'service')
        mock_parse.return_value = fake_args
        mock_current_association.return_value = ['S5555']
        with Capturing() as output:
            cmr_association_diff.run()
        self.assertEqual(json.loads(output[0]), ['S5555'])

    @patch('podaac.cmr_association_diff.parse_args')
    def test_run_invalid_concept_id(self, mock_method):
        """test run invalid concept id"""

        fake_args = MockArgs('C1234', 'service')
        mock_method.return_value = fake_args
        with self.assertRaises(Exception):
            cmr_association_diff.run()
