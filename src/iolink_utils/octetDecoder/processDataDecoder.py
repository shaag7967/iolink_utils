
class BinaryProcessDataHelper:
    @staticmethod
    def createPDInDecoderClass(json_process_data_def, condition=None):
        attributes = {
            "__init__": BinaryProcessDataHelper.__init
        }

        pd_def = json_process_data_def[condition]
        if 'pdIn' in pd_def:
            cls_name = pd_def['pdIn']['id']
            attributes["pdin_format"] = pd_def['pdIn']['dataFormat']
            attributes["pdin_length"] = pd_def['pdIn']['bitLength']
            attributes["decodePDIn"] = BinaryProcessDataHelper.__decodePDIn
        else:
            cls_name = 'NoPDIn'
            attributes["pdin_length"] = 0

        cls = type(
            cls_name,
            (object,),
            attributes
        )
        return cls

    @staticmethod
    def createPDOutDecoderClass(json_process_data_def, condition=None):
        attributes = {
            "__init__": BinaryProcessDataHelper.__init
        }

        pd_def = json_process_data_def[condition]
        if 'pdOut' in pd_def:
            cls_name = pd_def['pdOut']['id']
            attributes["pdout_format"] = pd_def['pdOut']['dataFormat']
            attributes["pdout_length"] = pd_def['pdOut']['bitLength']
            attributes["decodePDOut"] = BinaryProcessDataHelper.__decodePDOut
        else:
            cls_name = 'NoPDOut'
            attributes["pdout_length"] = 0

        cls = type(
            cls_name,
            (object,),
            attributes
        )
        return cls

    @staticmethod
    def __init(self):
        # init with zero
        if getattr(self, 'pdin_length', None) is not None:
            BinaryProcessDataHelper.__decodePDIn(self, bytes(int(self.pdin_length / 8)))
        if getattr(self, 'pdout_length', None) is not None:
            BinaryProcessDataHelper.__decodePDOut(self, bytes(int(self.pdout_length / 8)))

    @staticmethod
    def __decodeBinaryProcessData(self, data_format, raw_bytes):
        for element in data_format:
            name = element['name'][0] # using textId as name
            offset = element['bitOffset']
            value_type = element['data']['type']
            length = element['data']['bitLength']

            if value_type == bytearray:
                start_pos = int(offset / 8)
                end_pos = int(start_pos + (length / 8))
                setattr(self, name, raw_bytes[start_pos:end_pos])
            else:
                value = int.from_bytes(raw_bytes, byteorder="big")
                mask = 2 ** length - 1
                setattr(self, name, value_type((value >> offset) & mask))

    @staticmethod
    def __decodePDIn(self, raw_bytes):
        if self.pdin_length != (len(raw_bytes)*8):
            raise ValueError(f"Raw data size ({len(raw_bytes)*8} bits) does not match PDIn size ({self.pdin_length} bits).")
        BinaryProcessDataHelper.__decodeBinaryProcessData(self, self.pdin_format, raw_bytes)

    @staticmethod
    def __decodePDOut(self, raw_bytes):
        if self.pdout_length != (len(raw_bytes)*8):
            raise ValueError(f"Raw data size ({len(raw_bytes)*8} bits) does not match PDOut size ({self.pdout_length} bits).")
        BinaryProcessDataHelper.__decodeBinaryProcessData(self, self.pdout_format, raw_bytes)
