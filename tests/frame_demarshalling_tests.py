# coding=utf-8
import unittest2 as unittest

import pamqp


class DemarshallingTests(unittest.TestCase):

    def protocol_header_test(self):

        # Decode the frame and validate lengths
        frame_data = 'AMQP\x00\x00\t\x01'
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 8,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 8))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'ProtocolHeader',
                         ('Frame was of wrong type, expected ProtocolHeader, '
                          'received %s' % frame_obj.name))

        self.assertEqual((frame_obj.major_version,
                          frame_obj.minor_version,
                          frame_obj.revision),
                          (0, 9, 1),
                          "Protocol version is incorrect")

    def heartbeat_test(self):
        frame_data = '\x08\x00\x00\x00\x00\x00\x00\xce'
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 7,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 7))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Heartbeat',
                         ('Frame was of wrong type, expected Heartbeat, '
                          'received %s' % frame_obj.name))

    def basic_ack_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00\x00\x00' \
                     '\x00\x00\x01\x00\xce'
        expectation = {'multiple': False, 'delivery_tag': 1}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Ack',
                         ('Frame was of wrong type, expected Basic.Ack, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_cancel_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07ctag1.0\x00\xce'
        expectation = {'consumer_tag': 'ctag1.0', 'nowait': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name,
                         'Basic.Cancel',
                         ('Frame was of wrong type, expected Basic.Cancel, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_cancelok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07ctag1.0\xce'
        expectation = {'consumer_tag': 'ctag1.0'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name,
                         'Basic.CancelOk',
                         ('Frame was of wrong type, expected Basic.CancelOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_consume_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x18\x00<\x00\x14\x00\x00\x04test'
                      '\x07ctag1.0\x00\x00\x00\x00\x00\xce')
        expectation = {'exclusive': False,
                       'nowait': False,
                       'no_local': False,
                       'consumer_tag': 'ctag1.0',
                       'queue': 'test',
                       'arguments': {},
                       'ticket': 0,
                       'no_ack': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 31,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 31))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name,
                         'Basic.Consume',
                          ('Frame was of wrong type, expected Basic.Consume, '
                           'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_consumeok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x15\x07ctag1.0\xce'
        expectation = {'consumer_tag': 'ctag1.0'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name,
                         'Basic.ConsumeOk',
                         ('Frame was of wrong type, expected Basic.ConsumeOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_deliver_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x1b\x00<\x00<\x07ctag1.0\x00'
                      '\x00\x00\x00\x00\x00\x00\x01\x00\x00\x04test\xce')

        expectation = {'consumer_tag': 'ctag1.0',
                       'delivery_tag': 1,
                       'redelivered': False,
                       'exchange': '',
                       'routing_key': 'test'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 34,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 34))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Deliver',
                         ('Frame was of wrong type, expected Basic.Deliver, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_get_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x0c\x00<\x00F\x00\x00\x04test'
                      '\x00\xce')
        expectation = {'queue': 'test', 'ticket': 0, 'no_ack': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Get',
                         ('Frame was of wrong type, expected Basic.Get, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_getempty_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00<\x00H\x00\xce'
        expectation = {'cluster_id': u''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.GetEmpty',
                         ('Frame was of wrong type, expected Basic.GetEmpty, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_getok_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x17\x00<\x00G\x00\x00\x00\x00'
                      '\x00\x00\x00\x10\x00\x00\x04test\x00\x00\x12\x06\xce')
        expectation = {'message_count': 4614,
                       'redelivered': False,
                       'routing_key': 'test',
                       'delivery_tag': 16,
                       'exchange': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 30,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 30))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.GetOk',
            ('Frame was of wrong type, expected Basic.GetOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_nack_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00x\x00\x00\x00\x00'
                      '\x00\x00\x00\x01\x00\xce')
        expectation = {'requeue': False, 'multiple': False, 'delivery_tag': 1}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Nack',
            ('Frame was of wrong type, expected Basic.Nack, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_publish_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00(\x00\x00\x00\x04test'
                      '\x00\xce')
        expectation = {'ticket': 0, 'mandatory': False, 'routing_key': 'test',
                       'immediate': False, 'exchange': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Publish',
                         ('Frame was of wrong type, expected Basic.Publish, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_qos_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x0b\x00<\x00\n\x00\x00\x00\x00'
                      '\x00\x01\x00\xce')
        expectation = {'prefetch_count': 1, 'prefetch_size': 0,
                       'global_': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 18,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 18))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Qos',
            ('Frame was of wrong type, expected Basic.Qos, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_qosok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00<\x00\x0b\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.QosOk',
            ('Frame was of wrong type, expected Basic.QosOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_reject_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00Z\x00\x00\x00\x00\x00'
                      '\x00\x00\x10\x01\xce')
        expectation = {'requeue': True, 'delivery_tag': 16}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Reject',
            ('Frame was of wrong type, expected Basic.Reject, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_recover_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00<\x00n\x00\xce'
        expectation = {'requeue': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Recover',
                         ('Frame was of wrong type, expected Basic.Recover, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_recoverasync_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00<\x00d\x00\xce'
        self.assertRaises(DeprecationWarning, pamqp.frame.demarshal, frame_data)

    def basic_recoverok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00<\x00o\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.RecoverOk',
            ('Frame was of wrong type, expected Basic.RecoverOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_reject_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00Z\x00\x00\x00\x00\x00'
                      '\x00\x00\x10\x01\xce')
        expectation = {'requeue': True, 'delivery_tag': 16}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 20,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 20))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Reject',
            ('Frame was of wrong type, expected Basic.Reject, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def basic_return_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00"\x00<\x002\x00\xc8\x0fNormal '
                      'shutdown\x03foo\x07foo.bar\xce')
        expectation = {'reply_code': 200, 'reply_text': 'Normal shutdown',
                       'routing_key': 'foo.bar', 'exchange': 'foo'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 41,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 41))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Basic.Return',
            ('Frame was of wrong type, expected Basic.Return, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def channel_close_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x1a\x00\x14\x00(\x00\xc8\x0f'
                      'Normal shutdown\x00\x00\x00\x00\xce')
        expectation = {'class_id': 0, 'method_id': 0, 'reply_code': 200,
                       'reply_text': 'Normal shutdown'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 33,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 33))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.Close',
            ('Frame was of wrong type, expected Channel.Close, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def channel_closeok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00\x14\x00)\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.CloseOk',
            ('Frame was of wrong type, expected Channel.CloseOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def channel_flow_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\x14\x01\xce'
        expectation = {'active': True}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.Flow',
            ('Frame was of wrong type, expected Channel.Flow, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)


    def channel_flowok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\x15\x01\xce'
        expectation = {'active': True}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.FlowOk',
            ('Frame was of wrong type, expected Channel.FlowOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def channel_open_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\n\x00\xce'
        expectation = {'out_of_band': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.Open',
            ('Frame was of wrong type, expected Channel.Open, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)


    def channel_openok_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x08\x00\x14\x00\x0b\x00\x00\x00'
                      '\x00\xce')
        expectation = {'channel_id': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Channel.OpenOk',
            ('Frame was of wrong type, expected Channel.OpenOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def confirm_select_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00U\x00\n\x00\xce'
        expectation = {'nowait': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Confirm.Select',
            ('Frame was of wrong type, expected Confirm.Select, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def confirm_selectok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00U\x00\x0b\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Confirm.SelectOk',
            ('Frame was of wrong type, expected Confirm.SelectOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_close_test(self):
        frame_data = ('\x01\x00\x00\x00\x00\x00\x1a\x00\n\x002\x00\xc8\x0f'
                      'Normal shutdown\x00\x00\x00\x00\xce')
        expectation = {'class_id': 0, 'method_id': 0, 'reply_code': 200,
                       'reply_text': 'Normal shutdown'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 33,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 33))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.Close',
            ('Frame was of wrong type, expected Connection.Close, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_closeok_test(self):
        frame_data = '\x01\x00\x00\x00\x00\x00\x04\x00\n\x003\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.CloseOk',
            ('Frame was of wrong type, expected Connection.CloseOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_open_test(self):
        frame_data = '\x01\x00\x00\x00\x00\x00\x08\x00\n\x00(\x01/\x00\x01\xce'
        expectation = {'insist': True, 'capabilities': '', 'virtual_host': '/'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.Open',
            ('Frame was of wrong type, expected Connection.Open, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_openok_test(self):
        frame_data = '\x01\x00\x00\x00\x00\x00\x05\x00\n\x00)\x00\xce'
        expectation = {'known_hosts': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 12,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 12))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.OpenOk',
            ('Frame was of wrong type, expected Connection.OpenOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_secure_test(self):
        frame_data = '\x01\x00\x00\x00\x00\x00\x08\x00\n\x00\x14\x00\x00\x00' \
                     '\x00\xce'
        expectation = {'challenge': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.Secure',
            ('Frame was of wrong type, expected Connection.Secure, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_secureok_test(self):
        frame_data = '\x01\x00\x00\x00\x00\x00\x08\x00\n\x00\x15\x00\x00\x00' \
                     '\x00\xce'
        expectation = {'response': ''}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.SecureOk',
            ('Frame was of wrong type, expected Connection.SecureOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_start_test(self):
        frame_data = ('\x01\x00\x00\x00\x00\x01G\x00\n\x00\n\x00\t\x00\x00\x01'
                      '"\x0ccapabilitiesF\x00\x00\x00X\x12publisher_confirmst'
                      '\x01\x1aexchange_exchange_bindingst\x01\nbasic.nackt\x01'
                      '\x16consumer_cancel_notifyt\x01\tcopyrightS\x00\x00\x00'
                      '$Copyright (C) 2007-2011 VMware, Inc.\x0binformationS'
                      '\x00\x00\x005Licensed under the MPL.  See http://www.ra'
                      'bbitmq.com/\x08platformS\x00\x00\x00\nErlang/OTP\x07pro'
                      'ductS\x00\x00\x00\x08RabbitMQ\x07versionS\x00\x00\x00'
                      '\x052.6.1\x00\x00\x00\x0ePLAIN AMQPLAIN\x00\x00\x00\x05'
                      'en_US\xce')
        expectation = {'server_properties':
                               {'information': ('Licensed under the MPL.  '
                                                'See http://www.rabbitmq.com/'),
                                'product': 'RabbitMQ',
                                'copyright': ('Copyright (C) 2007-2011 '
                                              'VMware, Inc.'),
                                'capabilities':
                                        {'exchange_exchange_bindings': True,
                                         'consumer_cancel_notify': True,
                                         'publisher_confirms': True,
                                         'basic.nack': True},
                                'platform': 'Erlang/OTP', 'version': '2.6.1'},
                       'version_minor': 9, 'mechanisms': 'PLAIN AMQPLAIN',
                       'locales': 'en_US', 'version_major': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 334,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 334))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.Start',
            ('Frame was of wrong type, expected Connection.Start, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_startok_test(self):
        frame_data = ('\x01\x00\x00\x00\x00\x00\xf4\x00\n\x00\x0b\x00\x00\x00'
                      '\xd0\x08platformS\x00\x00\x00\x0cPython 2.7.1\x07produ'
                      'ctS\x00\x00\x00\x1aPika Python Client Library\x07versi'
                      'onS\x00\x00\x00\n0.9.6-pre0\x0ccapabilitiesF\x00\x00'
                      '\x00;\x16consumer_cancel_notifyt\x01\x12publisher_conf'
                      'irmst\x01\nbasic.nackt\x01\x0binformationS\x00\x00\x00'
                      '\x1aSee http://pika.github.com\x05PLAIN\x00\x00\x00'
                      '\x0c\x00guest\x00guest\x05en_US\xce')
        expectation = {'locale': 'en_US',
                       'mechanism': 'PLAIN',
                       'client_properties':
                               {'platform': 'Python 2.7.1',
                                'product': 'Pika Python Client Library',
                                'version': '0.9.6-pre0',
                                'capabilities': {'consumer_cancel_notify': True,
                                                 'publisher_confirms': True,
                                                 'basic.nack': True},
                                'information': 'See http://pika.github.com'},
                       'response': '\x00guest\x00guest'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 251,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 251))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.StartOk',
            ('Frame was of wrong type, expected Connection.StartOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_tune_test(self):
        frame_data = ('\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1e\x00\x00\x00'
                      '\x02\x00\x00\x00\x00\xce')
        expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.Tune',
            ('Frame was of wrong type, expected Connection.Tune, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def connection_tuneok_test(self):
        frame_data = ('\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1f\x00\x00\x00'
                      '\x02\x00\x00\x00\x00\xce')
        expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 0,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Connection.TuneOk',
            ('Frame was of wrong type, expected Connection.TuneOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def content_body_frame_test(self):
        frame_data = ('\x03\x00\x01\x00\x00\x00#Hello World #0:'
                      '1316899165.75516605\xce')

        expectation = "Hello World #0:1316899165.75516605"

        # Decode the frame and validate lengths
        consumed, channel, data = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 41,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 41))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the demarshalled data matches the expectation
        self.assertEqual(data, expectation)

    def exchange_bind_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x15\x00(\x00\x1e\x00\x00\x00'
                      '\x00\x07foo.bar\x00\x00\x00\x00\x00\xce')
        expectation = {'arguments': {}, 'source': u'', 'ticket': 0,
                       'destination': u'', 'nowait': False,
                       'routing_key': u'foo.bar'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 28,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 28))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.Bind',
            ('Frame was of wrong type, expected Exchange.Bind, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_bindok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x1f\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.BindOk',
            ('Frame was of wrong type, expected Exchange.BindOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_declare_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00%\x00(\x00\n\x00\x00\x12'
                      'pika_test_exchange\x06direct\x00\x00\x00\x00\x00\xce')
        expectation = {'nowait': False,
                       'exchange': 'pika_test_exchange',
                       'durable': False,
                       'passive': False,
                       'internal': False,
                       'arguments': {},
                       'ticket': 0,
                       'type': 'direct',
                       'auto_delete': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 44,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 44))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.Declare',
                         ('Frame was of wrong type, expected Exchange.Declare, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_declareok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x0b\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.DeclareOk',
                         ('Frame was of wrong type, expected Exchange.'
                          'DeclareOk, received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_delete_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x1a\x00(\x00\x14\x00\x00\x12'
                      'pika_test_exchange\x00\xce')
        expectation = {'ticket': 0,
                       'if_unused': False,
                       'nowait': False,
                       'exchange': 'pika_test_exchange'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 33,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 33))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.Delete',
                         ('Frame was of wrong type, expected Exchange.Delete, '
                           'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_deleteok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x15\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.DeleteOk',
                         ('Frame was of wrong type, expected Exchange.DeleteOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_unbind_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x15\x00(\x00(\x00\x00\x00\x00'
                      '\x07foo.bar\x00\x00\x00\x00\x00\xce')
        expectation = {'arguments': {}, 'source': u'', 'ticket': 0,
                       'destination': u'', 'nowait': False,
                       'routing_key': u'foo.bar'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 28,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 28))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.Unbind',
            ('Frame was of wrong type, expected Exchange.Unbind, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def exchange_unbindok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x003\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Exchange.UnbindOk',
            ('Frame was of wrong type, expected Exchange.UnbindOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_bind_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00?\x002\x00\x14\x00\x00\x0fpika_'
                      'test_queue\x12pika_test_exchange\x10test_routing_key'
                      '\x00\x00\x00\x00\x00\xce')
        expectation = {'nowait': False,
                       'exchange': 'pika_test_exchange',
                       'routing_key': 'test_routing_key',
                       'queue': 'pika_test_queue',
                       'arguments': {},
                       'ticket': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 70,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 70))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.Bind',
                         ('Frame was of wrong type, expected Queue.Bind, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_bindok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x002\x00\x15\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.BindOk',
            ('Frame was of wrong type, expected Queue.BindOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_declare_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x10\x002\x00\n\x00\x00\x04test'
                      '\x02\x00\x00\x00\x00\xce')
        expectation = {'passive': False,
                       'nowait': False,
                       'exclusive': False,
                       'durable': True,
                       'queue': 'test',
                       'arguments': {},
                       'ticket': 0,
                       'auto_delete': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 23,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 23))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.Declare',
            ('Frame was of wrong type, expected Queue.Declare, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_declareok_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x11\x002\x00\x0b\x04test'
                      '\x00\x00\x12\x07\x00\x00\x00\x00\xce')
        expectation = {'queue': 'test', 'message_count': 4615,
                       'consumer_count': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 24,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 24))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.DeclareOk',
                         ('Frame was of wrong type, expected Queue.DeclareOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_delete_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x17\x002\x00(\x00\x00\x0f'
                      'pika_test_queue\x00\xce')
        expectation = {'queue': 'pika_test_queue',
                       'ticket': 0,
                       'if_empty': False,
                       'nowait': False,
                       'if_unused': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 30,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 30))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.Delete',
            ('Frame was of wrong type, expected Queue.Delete, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_deleteok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x08\x002\x00)\x00\x00\x00\x00' \
                     '\xce'
        expectation = {'message_count': 0}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.DeleteOk',
            ('Frame was of wrong type, expected Queue.DeleteOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_purge_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x0c\x002\x00\x1e\x00\x00\x04test'
                      '\x00\xce')
        expectation = {'queue': 'test', 'ticket': 0, 'nowait': False}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 19,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 19))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.Purge',
                         ('Frame was of wrong type, expected Queue.Purge, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_purgeok_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00\x08\x002\x00\x1f\x00\x00\x00'
                      '\x01\xce')
        expectation = {'message_count': 1}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 15,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 15))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.PurgeOk',
            ('Frame was of wrong type, expected Queue.PurgeOk, '
             'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_unbind_test(self):
        frame_data = ('\x01\x00\x01\x00\x00\x00>\x002\x002\x00\x00\x0fpika_test'
                      '_queue\x12pika_test_exchange\x10test_routing_key\x00\x00'
                      '\x00\x00\xce')
        expectation = {'queue': 'pika_test_queue',
                       'arguments': {},
                       'ticket': 0,
                       'routing_key': 'test_routing_key',
                       'exchange': 'pika_test_exchange'}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 69,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 69))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.Unbind',
                         ('Frame was of wrong type, expected Queue.Unbind, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def queue_unbindok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x002\x003\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Queue.UnbindOk',
                         ('Frame was of wrong type, expected Queue.UnbindOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_commit_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x14\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.Commit',
                         ('Frame was of wrong type, expected Tx.Commit, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_commitok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x15\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.CommitOk',
                         ('Frame was of wrong type, expected Tx.CommitOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_rollback_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x1e\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.Rollback',
                         ('Frame was of wrong type, expected Tx.Rollback, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_rollbackok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x1f\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.RollbackOk',
                         ('Frame was of wrong type, expected Tx.RollbackOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_select_test(self):
        frame_data =  '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\n\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.Select',
                         ('Frame was of wrong type, expected Tx.Select, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def tx_selectok_test(self):
        frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x0b\xce'
        expectation = {}

        # Decode the frame and validate lengths
        consumed, channel, frame_obj = pamqp.frame.demarshal(frame_data)

        self.assertEqual(consumed, 11,
                         'Bytes consumed did not match expectation: %i, %i' %
                         (consumed, 11))

        self.assertEqual(channel, 1,
                         'Channel number did not match expectation: %i, %i' %
                         (channel, 1))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Tx.SelectOk',
                         ('Frame was of wrong type, expected Tx.SelectOk, '
                          'received %s' % frame_obj.name))

        # Validate the demarshalled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)
