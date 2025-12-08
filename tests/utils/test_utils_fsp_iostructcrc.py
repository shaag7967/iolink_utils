import pytest

from iolink_utils.utils.fsp_ioStruct import createFSP_IOStructDescription
from iolink_utils.exceptions import InvalidProcessDataDefinition


def test_utils_fsp_iostructcrc_exampleIodd():
    # process data definition from IO-Link_Safety_System-Extensions_10092_D1.1.5-02_2025-06-01/IODD_Example/
    # IO-Link-Safety_001201-20250508-IODD1.1.xml
    pdd = {None: {'id': 'P_FSP_ProcessData',
                  'pdIn': {'bitLength': 112,
                           'dataFormat': [{'bitOffset': 104,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_1',
                                                    'FS-PD Boolean State 1'),
                                           'subIndex': 1},
                                          {'bitOffset': 105,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_2',
                                                    'FS-PD Boolean State 2'),
                                           'subIndex': 2},
                                          {'bitOffset': 106,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_3',
                                                    'FS-PD Boolean State 3'),
                                           'subIndex': 3},
                                          {'bitOffset': 107,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_4',
                                                    'FS-PD Boolean State 4'),
                                           'subIndex': 4},
                                          {'bitOffset': 108,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_5',
                                                    'FS-PD Boolean State 5'),
                                           'subIndex': 5},
                                          {'bitOffset': 109,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_6',
                                                    'FS-PD Boolean State 6'),
                                           'subIndex': 6},
                                          {'bitOffset': 110,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_7',
                                                    'FS-PD Boolean State 7'),
                                           'subIndex': 7},
                                          {'bitOffset': 111,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_8',
                                                    'FS-PD Boolean State 8'),
                                           'subIndex': 8},
                                          {'bitOffset': 96,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_9',
                                                    'FS-PD Boolean State 9'),
                                           'subIndex': 9},
                                          {'bitOffset': 97,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_10',
                                                    'FS-PD Boolean State 10'),
                                           'subIndex': 10},
                                          {'bitOffset': 98,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_11',
                                                    'FS-PD Boolean State 11'),
                                           'subIndex': 11},
                                          {'bitOffset': 99,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_12',
                                                    'FS-PD Boolean State 12'),
                                           'subIndex': 12},
                                          {'bitOffset': 100,
                                           'data': {'bitLength': 1,
                                                    'type': bool},
                                           'name': ('TN_V_FST_X_State_13',
                                                    'FS-PD Boolean State 13'),
                                           'subIndex': 13},
                                          {'bitOffset': 80,
                                           'data': {'bitLength': 16,
                                                    'type': int},
                                           'name': ('TN_V_FST_X_Integer16Value',
                                                    'FS-PD Integer 16 Value'),
                                           'subIndex': 14},
                                          {'bitOffset': 32,
                                           'data': {'bitLength': 48,
                                                    'type': bytearray},
                                           'name': ('TN_V_FSP_SafetyCode',
                                                    'FS Safety Code'),
                                           'subIndex': 127},
                                          {'bitOffset': 0,
                                           'data': {'bitLength': 32,
                                                    'type': int},
                                           'name': ('TN_V_X_Revolutions', 'Revolutions'),
                                           'subIndex': 128}],
                           'id': 'PI_FSP_PDin',
                           'name': ('TN_PI_FSP_PDin', 'PD Input')},
                  'pdOut': {'bitLength': 48,
                            'dataFormat': [{'bitOffset': 0,
                                            'data': {'bitLength': 48,
                                                     'type': bytearray},
                                            'name': ('TN_V_FSP_SafetyCode',
                                                     'FS Safety Code'),
                                            'subIndex': 127}],
                            'id': 'PO_FSP_PDout',
                            'name': ('TN_PO_FSP_PDout', 'PD Output')}}}

    ioStruct = createFSP_IOStructDescription(pdd)
    assert ioStruct.calculateFSPIOStructCRC() == 39464


def test_utils_fsp_iostructcrc_int32():
    pdd = {None: {'id': 'P_FSP_ProcessData',
                  'pdIn': {'bitLength': 80,
                           'dataFormat': [{'bitOffset': 48,
                                           'data': {'bitLength': 32,
                                                    'type': int},
                                           'name': ('TN_V_FST_X_Integer32Value',
                                                    'FS-PD Integer 32 Value'),
                                           'subIndex': 1},
                                          {'bitOffset': 0,
                                           'data': {'bitLength': 48,
                                                    'type': bytearray},
                                           'name': ('TN_V_FSP_SafetyCode',
                                                    'FS Safety Code'),
                                           'subIndex': 127}],
                           'id': 'PI_FSP_PDin',
                           'name': ('TN_PI_FSP_PDin', 'PD Input')},
                  'pdOut': {'bitLength': 48,
                            'dataFormat': [{'bitOffset': 0,
                                            'data': {'bitLength': 48,
                                                     'type': bytearray},
                                            'name': ('TN_V_FSP_SafetyCode',
                                                     'FS Safety Code'),
                                            'subIndex': 127}],
                            'id': 'PO_FSP_PDout',
                            'name': ('TN_PO_FSP_PDout', 'PD Output')}}}

    ioStruct = createFSP_IOStructDescription(pdd)
    assert ioStruct.calculateFSPIOStructCRC() == 12968


def test_utils_fsp_iostructcrc_invalid():
    # no definition
    with pytest.raises(InvalidProcessDataDefinition):
        createFSP_IOStructDescription({})

    # single definition, but no None key
    pdd1 = {
        0: {
            'pdIn': {},
            'pdOut': {}
        }
    }
    with pytest.raises(InvalidProcessDataDefinition):
        createFSP_IOStructDescription(pdd1)

    # multiple definitions
    pdd2 = {
        0: {
            'pdIn': {},
            'pdOut': {}
        },
        1: {
            'pdIn': {},
            'pdOut': {}
        }
    }
    with pytest.raises(InvalidProcessDataDefinition):
        createFSP_IOStructDescription(pdd2)

    # invalid bitLength of data element
    pdd3 = {
        None: {
            'pdIn': {'bitLength': 48,
                     'dataFormat': [{'bitOffset': 0,
                                     'data': {'bitLength': 48,
                                              'type': bytearray},
                                     'name': ('NAME_1', 'Name 1'),
                                     'subIndex': 127}]},
            'pdOut': {'bitLength': 112,
                      'dataFormat': [{'bitOffset': 48,
                                      'data': {'bitLength': 64,  # INVALID
                                               'type': int},
                                      'name': ('NAME_2', 'Name 2'),
                                      'subIndex': 1},
                                     {'bitOffset': 0,
                                      'data': {'bitLength': 48,
                                               'type': bytearray},
                                      'name': ('NAME_3', 'Name 3'),
                                      'subIndex': 127}]}
        }
    }
    with pytest.raises(InvalidProcessDataDefinition):
        createFSP_IOStructDescription(pdd3)
