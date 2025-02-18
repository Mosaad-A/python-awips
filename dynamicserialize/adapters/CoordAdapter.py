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


#
# Adapter for org.locationtech.jts.geom.Coordinate
#  
#    
#     SOFTWARE HISTORY
#    
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    01/20/11                      dgilling      Initial Creation.
#    
# 
#

from dynamicserialize.dstypes.org.locationtech.jts.geom import Coordinate

ClassAdapter = 'org.locationtech.jts.geom.Coordinate'

def serialize(context, coordinate):
    context.writeDouble(coordinate.getX())
    context.writeDouble(coordinate.getY())

def deserialize(context):
    x = context.readDouble()
    y = context.readDouble()
    coord = Coordinate()
    coord.setX(x)
    coord.setY(y)
    return coord

