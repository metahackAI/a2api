"""The a-commerce scoring port reproduces xtask/src/run_eval.rs's own unit tests."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples/acommerce'))
from scoring import numbers, score, shown  # noqa: E402


class ScoringPortTests(unittest.TestCase):
    def test_numbers_in_facts_are_found_as_people_write_them(self):
        self.assertEqual(numbers('41 reviews, average 4.6.'), ['41', '4.6'])
        self.assertEqual(numbers('refund $2,463.00 for 9'), ['2463', '9'])
        self.assertEqual(numbers('#20366, #20409 and 4,5'), ['20366', '20409', '4', '5'])
        self.assertEqual(numbers('cus_4431 at 08:31 on Nov 07, parka x2'), ['4431', '8', '31', '7', '2'])
        self.assertEqual(numbers('UPS 1ZNW271840001'), ['1znw271840001'])
        seen = shown('Here are 41 reviews (4.6 stars) and $2,463.00 for 9 refunds')
        self.assertTrue(all(n in seen for n in numbers('41 reviews, average 4.60; $2463 back')))

    def test_a_number_inside_an_id_a_bigger_number_or_a_utc_offset_is_not_shown(self):
        blocks = [{'ui': 'product_table', 'block_id': 'blk_01m68d4gm4xs1z0x67n8drh2fn',
                   'data': {'rows': [{'id': 'promo_autumn_knit', 'stock': 17, 'valid_from': '2026-11-01T00:00:00-04:00'}]}}]
        seen = shown('Four promotions run this weekend.', blocks)
        for n in ['7', '4', '8']:
            self.assertNotIn(n, seen)
        self.assertTrue(all(n in seen for n in ['17', '2026', '11', '1']))
        seen = shown('', [{'data': {'rows': [{'stock': 4, 'valid_until': '2026-11-07T23:59:30-05:00'}]}}])
        self.assertTrue(all(n in seen for n in ['4', '7', '23', '59', '30']))
        self.assertNotIn('5', seen)

    def test_a_run_is_done_only_when_tools_change_set_and_facts_hold(self):
        task = {'tools': {'required': ['search_products']}, 'expect': {'facts': ['3 items left'],
                'must_not_call': ['send_customer_message'],
                'change_set': {'state': 'drafting', 'items': [{'tool': 'set_sale_prices', 'args': {'percent': 20}}]}}}
        cs = {'state': 'waiting_for_approval', 'items': [{'tool': 'set_sale_prices', 'input': {'percent': 20}, 'checks': []}]}
        done, missing, *_ = score(task, tool_names_scored=True, reply='3 items left', blocks=[],
                                  tools=[('search_products', True)], change_set=cs)
        self.assertTrue(done, missing)
        done, missing, *_ = score(task, tool_names_scored=True, reply='13 items left', blocks=[],
                                  tools=[('search_products', False), ('send_customer_message', True)], change_set=None)
        self.assertFalse(done)
        self.assertEqual(missing, ['tool search_products', 'change set', 'called send_customer_message',
                                   'fact "3 items left" (3 not shown)'])
        done, missing, *_ = score(task, tool_names_scored=False, reply='3 items left', blocks=[], tools=[], change_set=None)
        self.assertTrue(done, missing)


if __name__ == '__main__':
    unittest.main()
