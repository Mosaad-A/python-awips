##
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
#
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
#
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
#
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
##


from awips.dataaccess import DataAccessLayer as DAL

from dynamicserialize.dstypes.com.raytheon.uf.common.dataquery.requests import RequestConstraint
from . import baseDafTestCase

#
# Test DAF support for sfcobs data
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    01/19/16        4795          mapeters       Initial Creation.
#    04/11/16        5548          tgurney        Cleanup
#    04/18/16        5548          tgurney        More cleanup
#    06/09/16        5587          bsteffen       Add getIdentifierValues tests
#    06/13/16        5574          tgurney        Add advanced query tests
#    06/30/16        5725          tgurney        Add test for NOT IN
#    01/20/17        6095          tgurney        Add null identifiers test
#
#


class SfcObsTestCase(baseDafTestCase.DafTestCase):
    """Test DAF support for sfcobs data"""

    datatype = "sfcobs"

    def testGetAvailableParameters(self):
        req = DAL.newDataRequest(self.datatype)
        self.runParametersTest(req)

    def testGetAvailableLocations(self):
        req = DAL.newDataRequest(self.datatype)
        self.runLocationsTest(req)

    def testGetAvailableTimes(self):
        req = DAL.newDataRequest(self.datatype)
        req.setLocationNames("14547")
        self.runTimesTest(req)

    def testGetGeometryData(self):
        req = DAL.newDataRequest(self.datatype)
        req.setLocationNames("14547")
        req.setParameters("temperature", "seaLevelPress", "dewpoint")
        self.runGeometryDataTest(req)

    def testGetGeometryDataNullIdentifiers(self):
        req = DAL.newDataRequest(self.datatype)
        req.setLocationNames("14547")
        req.setParameters("temperature", "seaLevelPress", "dewpoint")
        req.identifiers = None
        self.runGeometryDataTest(req)

    def testGetIdentifierValues(self):
        req = DAL.newDataRequest(self.datatype)
        optionalIds = set(DAL.getOptionalIdentifiers(req))
        self.runGetIdValuesTest(optionalIds)

    def testGetInvalidIdentifierValuesThrowsException(self):
        self.runInvalidIdValuesTest()

    def testGetNonexistentIdentifierValuesThrowsException(self):
        self.runNonexistentIdValuesTest()

    def _runConstraintTest(self, key, operator, value):
        req = DAL.newDataRequest(self.datatype)
        constraint = RequestConstraint.new(operator, value)
        req.addIdentifier(key, constraint)
        req.setParameters("temperature", "reportType")
        return self.runGeometryDataTest(req)

    def testGetDataWithEqualsString(self):
        geometryData = self._runConstraintTest('reportType', '=', '1004')
        for record in geometryData:
            self.assertEqual(record.getString('reportType'), '1004')

    def testGetDataWithEqualsInt(self):
        geometryData = self._runConstraintTest('reportType', '=', 1004)
        for record in geometryData:
            self.assertEqual(record.getString('reportType'), '1004')

    # No float test because no float identifiers are available

    def testGetDataWithEqualsNone(self):
        geometryData = self._runConstraintTest('reportType', '=', None)
        for record in geometryData:
            self.assertEqual(record.getType('reportType'), 'NULL')

    def testGetDataWithNotEquals(self):
        geometryData = self._runConstraintTest('reportType', '!=', 1004)
        for record in geometryData:
            self.assertNotEqual(record.getString('reportType'), '1004')

    def testGetDataWithNotEqualsNone(self):
        geometryData = self._runConstraintTest('reportType', '!=', None)
        for record in geometryData:
            self.assertNotEqual(record.getType('reportType'), 'NULL')

    def testGetDataWithGreaterThan(self):
        geometryData = self._runConstraintTest('reportType', '>', 1004)
        for record in geometryData:
            self.assertGreater(record.getString('reportType'), '1004')

    def testGetDataWithLessThan(self):
        geometryData = self._runConstraintTest('reportType', '<', 1004)
        for record in geometryData:
            self.assertLess(record.getString('reportType'), '1004')

    def testGetDataWithGreaterThanEquals(self):
        geometryData = self._runConstraintTest('reportType', '>=', 1004)
        for record in geometryData:
            self.assertGreaterEqual(record.getString('reportType'), '1004')

    def testGetDataWithLessThanEquals(self):
        geometryData = self._runConstraintTest('reportType', '<=', 1004)
        for record in geometryData:
            self.assertLessEqual(record.getString('reportType'), '1004')

    def testGetDataWithInTuple(self):
        collection = ('1004', '1005')
        geometryData = self._runConstraintTest('reportType', 'in', collection)
        for record in geometryData:
            self.assertIn(record.getString('reportType'), collection)

    def testGetDataWithInList(self):
        collection = ['1004', '1005']
        geometryData = self._runConstraintTest('reportType', 'in', collection)
        for record in geometryData:
            self.assertIn(record.getString('reportType'), collection)

    def testGetDataWithInGenerator(self):
        collection = ('1004', '1005')
        generator = (item for item in collection)
        geometryData = self._runConstraintTest('reportType', 'in', generator)
        for record in geometryData:
            self.assertIn(record.getString('reportType'), collection)

    def testGetDataWithNotInList(self):
        collection = ['1004', '1005']
        geometryData = self._runConstraintTest('reportType', 'not in', collection)
        for record in geometryData:
            self.assertNotIn(record.getString('reportType'), collection)

    def testGetDataWithInvalidConstraintTypeThrowsException(self):
        with self.assertRaises(ValueError):
            self._runConstraintTest('reportType', 'junk', '1004')

    def testGetDataWithInvalidConstraintValueThrowsException(self):
        with self.assertRaises(TypeError):
            self._runConstraintTest('reportType', '=', {})

    def testGetDataWithEmptyInConstraintThrowsException(self):
        with self.assertRaises(ValueError):
            self._runConstraintTest('reportType', 'in', [])

    def testGetDataWithNestedInConstraintThrowsException(self):
        collection = ('1004', '1005', ())
        with self.assertRaises(TypeError):
            self._runConstraintTest('reportType', 'in', collection)
