## Generated by pyxsdgen

from xml.etree import ElementTree as ET

# types

class OrderedStpType(object):
    def __init__(self, order, stp):
        self.order = order  # int
        self.stp = stp  # StpIdType -> string

    @classmethod
    def build(self, element):
        return OrderedStpType(
                element.get('order'),
                element.findtext('stp')
               )

    def xml(self, elementName):
        r = ET.Element(elementName, attrib={'order' : str(self.order)})
        ET.SubElement(r, 'stp').text = self.stp
        return r


class TypeValueType(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    @classmethod
    def build(self, element):
        return TypeValueType(
                element.get('type'),
                element.text
               )

    def xml(self, elementName):
        r = ET.Element(elementName, attrib={'type' : self.type_})
        r.text = self.value
        return r


class P2PServiceBaseType(object):
    def __init__(self, capacity, directionality, symmetricPath, sourceSTP, destSTP, ero, parameter):
        self.capacity = capacity  # long
        self.directionality = directionality  # DirectionalityType -> string
        self.symmetricPath = symmetricPath  # boolean
        self.sourceSTP = sourceSTP  # StpIdType -> string
        self.destSTP = destSTP  # StpIdType -> string
        self.ero = ero  # [ OrderedStpType ]
        self.parameter = parameter  # [ TypeValueType ]

    @classmethod
    def build(self, element):
        return P2PServiceBaseType(
                int(element.findtext('capacity')),
                element.findtext('directionality'),
                True if element.findtext('symmetricPath') == 'true' else False if element.find('symmetricPath') is not None else None,
                element.findtext('sourceSTP'),
                element.findtext('destSTP'),
                [ OrderedStpType.build(e) for e in element.find('ero') ] if element.find('ero') is not None else None,
                [ TypeValueType.build(e) for e in element.findall('parameter') ] if element.find('parameter') is not None else None
               )

    def xml(self, elementName):
        r = ET.Element(elementName)
        ET.SubElement(r, 'capacity').text = str(self.capacity)
        ET.SubElement(r, 'directionality').text = self.directionality
        if self.symmetricPath is not None:
            ET.SubElement(r, 'symmetricPath').text = 'true' if self.symmetricPath else 'false'
        ET.SubElement(r, 'sourceSTP').text = self.sourceSTP
        ET.SubElement(r, 'destSTP').text = self.destSTP
        if self.ero is not None:
            ET.SubElement(r, 'ero').extend( [ e.xml('ero') for e in self.ero ] )
        if self.parameter is not None:
            for p in self.parameter:
                ET.SubElement(r, 'parameter',  attrib={'type': p.type_}).text = p.value
        return r


POINT2POINT_NS = 'http://schemas.ogf.org/nsi/2013/12/services/point2point'

p2ps        = ET.QName(POINT2POINT_NS, 'p2ps')
capacity    = ET.QName(POINT2POINT_NS, 'capacity')
parameter   = ET.QName(POINT2POINT_NS, 'parameter')

def parse(input_):

    root = ET.fromstring(input_)

    return parseElement(root)


def parseElement(element):

    type_map = {
        str(p2ps)       : P2PServiceBaseType,
        str(parameter)  : TypeValueType
    }

    if not element.tag in type_map:
        raise ValueError('No type mapping for tag %s' % element.tag)

    type_ = type_map[element.tag]
    return type_.build(element)