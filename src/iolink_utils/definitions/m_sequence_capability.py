from dataclasses import dataclass
from typing import Tuple, Union


@dataclass(frozen=True)
class MSequenceCapability:
    value: int

    @property
    def isdu_supported(self) -> bool:
        return bool(self.value & 0b00000001)

    @property
    def operate_code(self) -> int:
        return (self.value >> 1) & 0b111

    @property
    def preoperate_code(self) -> int:
        return (self.value >> 4) & 0b11

    def __repr__(self):
        return (f"MSequenceCapability("
                f"isdu={self.isdu_supported}, "
                f"operate={self.operate_code}, "
                f"preoperate={self.preoperate_code})")


class ODOctetCount:
    # Table A.8  - M-sequence types for the PREOPERATE mode
    __preoperate = {
        # m-sequence code: On-request data, type
        0: (1, 'TYPE_0'), # not recommenced
        1: (2, 'TYPE_1_2'),
        2: (8, 'TYPE_1_V'),
        3: (32, 'TYPE_1_V')
    }

    @dataclass(frozen=True)
    class MSeqPDSizeCombination:
        m_sequence_code: int = 0
        size_PDin: Union[int, range] = 0
        size_PDout: Union[int, range] = 0

        def matches(self, m_sequence_code: int, size_PDin: int, size_PDout: int) -> bool:
            match_code = m_sequence_code == self.m_sequence_code
            match_PDin = size_PDin in self.size_PDin if type(self.size_PDin) == range else size_PDin == self.size_PDin
            match_PDout = size_PDout in self.size_PDout if type(self.size_PDout) == range else size_PDout == self.size_PDout
            return match_code and match_PDin and match_PDout

    # Table A.10 - M-sequence types for the OPERATE mode
    __operate = {
        # m-sequence code, PDin, PDout: On-request data, type
        MSeqPDSizeCombination(0, 0, 0): (1, 'TYPE_0'),
        MSeqPDSizeCombination(1, 0, 0): (2, 'TYPE_1_2'),
        MSeqPDSizeCombination(6, 0, 0): (8, 'TYPE_1_V'),
        MSeqPDSizeCombination(7, 0, 0): (32, 'TYPE_1_V'),
        MSeqPDSizeCombination(0, range(3, 32 + 1), range(0, 32 + 1)): (2, 'TYPE_1_1'),
        MSeqPDSizeCombination(0, range(0, 32 + 1), range(3, 32 + 1)): (2, 'TYPE_1_1'),
        MSeqPDSizeCombination(0, 1, 0): (1, 'TYPE_2_1'),
        MSeqPDSizeCombination(0, 2, 0): (1, 'TYPE_2_2'),
        MSeqPDSizeCombination(0, 0, 1): (1, 'TYPE_2_3'),
        MSeqPDSizeCombination(0, 0, 2): (1, 'TYPE_2_4'),
        MSeqPDSizeCombination(0, 1, 1): (1, 'TYPE_2_5'),
        MSeqPDSizeCombination(0, 2, range(1, 2 + 1)): (1, 'TYPE_2_V'),
        MSeqPDSizeCombination(0, range(1, 2 + 1), 2): (1, 'TYPE_2_V'),
        MSeqPDSizeCombination(4, range(0, 32 + 1), range(3, 32 + 1)): (1, 'TYPE_2_V'),
        MSeqPDSizeCombination(4, range(3, 32 + 1), range(0, 32 + 1)): (1, 'TYPE_2_V'),
        MSeqPDSizeCombination(5, range(1, 32 + 1), range(0, 32 + 1)): (2, 'TYPE_2_V'),
        MSeqPDSizeCombination(5, range(0, 32 + 1), range(1, 32 + 1)): (2, 'TYPE_2_V'),
        MSeqPDSizeCombination(6, range(1, 32 + 1), range(0, 32 + 1)): (8, 'TYPE_2_V'),
        MSeqPDSizeCombination(6, range(0, 32 + 1), range(1, 32 + 1)): (8, 'TYPE_2_V'),
        MSeqPDSizeCombination(7, range(1, 32 + 1), range(0, 32 + 1)): (32, 'TYPE_2_V'),
        MSeqPDSizeCombination(7, range(0, 32 + 1), range(1, 32 + 1)): (32, 'TYPE_2_V')
    }

    @staticmethod
    def in_preoperate(m_sequence_code: int) -> Tuple[int, str]:
        return ODOctetCount.__preoperate[m_sequence_code]

    @staticmethod
    def in_operate(m_sequence_code: int, size_PDin: int, size_PDout: int) -> Tuple[int, str]:
        for combination, value in ODOctetCount.__operate.items():
            if combination.matches(m_sequence_code, size_PDin, size_PDout):
                return value
        raise KeyError(f"Invalid combination of m-sequence code and PD size ({m_sequence_code}, {size_PDin}, {size_PDout})")
