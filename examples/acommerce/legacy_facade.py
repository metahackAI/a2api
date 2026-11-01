"""What a person converting a-commerce's screen-shaped facade (crates/facade) learns from its code.

Only what the legacy code itself says is used: the field doc comments (`/// Claim status code.`)
for readable names, the code tables in `codes.rs` for words, and each screen's body (which back-end
read or write it runs, paging, the `…Cnt` twin, row status meaning) for its summary. Nothing comes
from the A-Commerce tools, the task set or the store's rules; rules that live only in people's heads
stay unknown, as they would in a real conversion.
"""

from __future__ import annotations

import re

# codes.rs, as {legacy field: {code: word}}. The words are the back end's own (`word()`).
CODES = {
    'sellStatCd': {'10': 'in_stock', '20': 'out_of_stock', '30': 'pre_order', '40': 'back_order', '90': 'discontinued'},
    'prmtStatCd': {'00': 'draft', '10': 'scheduled', '20': 'running', '30': 'paused', '90': 'ended'},
    'mbrStatCd': {'10': 'active', '20': 'dormant', '30': 'blocked', '80': 'pending_withdrawal', '90': 'withdrawn'},
    'clmStatCd': {'R10': 'requested', 'R11': 'charge_due', 'R15': 'photos_requested', 'R20': 'approved',
                  'R30': 'pickup_instructed', 'R40': 'picked_up', 'R50': 'inspected', 'R60': 'reship_requested',
                  'R90': 'completed', 'R91': 'declined', 'R92': 'withdrawn', 'R93': 'converted'},
    'clmRsnCd': {'01': 'defect', '02': 'damaged_in_transit', '03': 'not_as_described', '04': 'wrong_item_sent',
                 '05': 'wrong_option_sent', '06': 'missing_parts', '11': 'wrong_size', '12': 'different_option_wanted',
                 '13': 'changed_mind'},
    'rspbCd': {'S': 'store_fault', 'L': 'seller_fault', 'C': 'customer_fault', 'D': 'carrier_fault', 'N': 'none'},
    'rtnDlvCstCd': {'1': 'free_return', '2': 'return_fees_customer_responsibility', '3': 'return_shipping_fees'},
    'msgTpCd': {'M01': 'ask_for_photos', 'M02': 'decline', 'M03': 'refund_done', 'M99': 'custom'},
    'sndChnlCd': {'1': 'email', '2': 'sms', '3': 'push', '4': 'in_app'},
    'cpnAplyTpCd': {'01': 'automatic_at_checkout', '02': 'code_entry', '03': 'download'},
    'dupAplyCd': {'N': 'no_tier_coupons', 'Y': 'with_tier_coupons', 'X': 'no_other_coupons'},
    'payMthdCd': {'10': 'credit_card', '20': 'bank_transfer', '30': 'virtual_account', '40': 'loyalty_points',
                  '50': 'store_credit'},
    'cmprBaseCd': {'1': 'same_weekday_last_4_weeks', '2': 'previous_period'},
    'dispPageCd': {'01': 'main', '02': 'category', '03': 'product', '04': 'search'},
    'cornerTpCd': {'H': 'hero', 'B': 'banner_board', 'G': 'product_grid', 'S': 'brand_strip', 'C': 'collection_feed'},
    'dispStatCd': {'00': 'draft', '10': 'scheduled', '20': 'active', '90': 'ended'},
    'rfndMthdCd': {'01': 'original_payment', '02': 'bank_account', '03': 'store_credit'},
    'aplyTgtCd': {'C': 'category', 'P': 'products'},
    'rowStat': {'I': 'insert', 'U': 'update', 'D': 'delete'},
    # codes.rs `prmt_tp`: the discount layer and whether the promotion is for one tier.
    'prmtTpCd': {'T01': 'item_price_everyone', 'T02': 'order_discount', 'T03': 'item_price_one_grade',
                 'T04': 'add_on', 'T05': 'other'},
    # clm.rs `clm_tp`.
    'clmTpCd': {'R': 'return', 'C': 'cancel', 'X': 'exchange', '9': 'other'},
    # codes.rs OrdStatCd (order and order line status) and DlvStatCd (a-commerce PR #103).
    'ordStatCd': {'10': 'payment_due', '20': 'processing', '30': 'in_transit', '40': 'delivered', '50': 'returned',
                  '80': 'problem', '90': 'cancelled'},
    'ordDtlStatCd': {'10': 'payment_due', '20': 'processing', '30': 'in_transit', '40': 'delivered', '50': 'returned',
                     '80': 'problem', '90': 'cancelled'},
    'dlvStatCd': {'10': 'awaiting_stock', '20': 'ship_instructed', '30': 'packed', '40': 'label_created',
                  '50': 'picked_up', '60': 'in_transit', '70': 'delivered', '80': 'delivery_failed', '90': 'cancelled'},
}

# The field doc comments, as names. Inputs and outputs share one table, as the screens share fields.
RENAME = {
    # search forms and paging
    'pageNo': 'page', 'pageSize': 'page_size', 'srchKwd': 'keyword', 'totCnt': 'total',
    # products
    'prdNo': 'product_id', 'prdNm': 'product_name', 'ctgNo': 'category_id', 'brndNo': 'brand_id',
    'sellStatCd': 'availability', 'stkQtyFrom': 'min_stock', 'stkQtyTo': 'max_stock', 'stkQty': 'stock',
    'aplyMbrGrdCd': 'price_for_member_grade', 'aplyDtm': 'price_as_of', 'salePrc': 'price', 'mbrPrc': 'member_price',
    'costPrc': 'cost', 'prdStatCd': 'approval_status', 'optList': 'variants', 'optNo': 'variant_id',
    'optVal1': 'color', 'optVal2': 'size', 'attrList': 'attributes', 'attrNm': 'attribute', 'attrVal': 'value',
    'unitCd': 'unit',
    # members and grades
    'prgmNo': 'loyalty_program_id', 'mbrGrdCd': 'member_grade', 'mbrGrdNm': 'grade_name', 'mbrCnt': 'member_count',
    'sortSeq': 'rank', 'mbrStatCd': 'member_status', 'mbrNo': 'member_id', 'mbrNm': 'member_name', 'emailAddr': 'email',
    # promotions and coupons
    'prmtNo': 'promotion_id', 'prmtNm': 'promotion_name', 'prmtTpCd': 'promotion_type', 'prmtStatCd': 'promotion_status',
    'tgtMbrGrdCd': 'target_member_grade', 'srchStrtDtm': 'active_from', 'srchEndDtm': 'active_until',
    'strtDtm': 'starts_at', 'endDtm': 'ends_at', 'aplyTgtCd': 'applies_to', 'prdNoList': 'product_ids',
    'dcRt': 'percent_off', 'rowStat': 'row_action', 'cpnCd': 'coupon_code', 'cpnAplyTpCd': 'coupon_application',
    'dupAplyCd': 'stacking', 'cpnNo': 'coupon_id',
    # display
    'dispPageCd': 'page_type', 'cornerTpCd': 'corner_type', 'cornerNo': 'corner_id', 'cornerNm': 'corner_name',
    'bnrList': 'banners', 'dispNo': 'booking_id', 'bnrTitl': 'headline', 'bnrSubTitl': 'eyebrow', 'btnNm': 'button_label',
    'lnkUrl': 'link_url', 'imgPrdNo': 'image_product_id', 'imgClrNm': 'image_color', 'imgNo': 'image_id',
    'dispStatCd': 'display_status',
    # claims, refunds, messages
    'clmNo': 'claim_id', 'clmStatCd': 'claim_status', 'clmRsnCd': 'claim_reason', 'clmAmtFrom': 'min_claim_amount',
    'ordNo': 'order_id', 'clmQty': 'claim_quantity', 'clmAmt': 'claim_amount', 'clmRsnCntt': 'reason_text',
    'atchFileCnt': 'photo_count', 'dlvCmplDt': 'delivered_at', 'clmReqDtm': 'requested_at', 'clmTpCd': 'claim_type',
    'rspbCd': 'liability', 'rtnDlvCstCd': 'return_fees', 'rfndAmt': 'refund_estimate', 'rfndNo': 'refund_id',
    'dlvCmplDtm': 'delivery_completed_at', 'payMthdCd': 'payment_method', 'cardNo': 'card_last4', 'prdList': 'items',
    'ordSeq': 'order_line_id', 'ordQty': 'order_quantity', 'dcAmt': 'discount', 'rfndMthdCd': 'refund_method',
    'msgTpCd': 'message_type', 'sndChnlCd': 'channel', 'msgTitl': 'subject', 'msgCntt': 'text', 'msgNo': 'message_id',
    # orders (ord.rs OrdSrchIn, the order grid and the order detail popup)
    'ordStatCd': 'order_status', 'ordDtmFrom': 'ordered_from', 'ordDtmTo': 'ordered_to', 'ordDtm': 'ordered_at',
    'ordAmt': 'order_total', 'ordDtlStatCd': 'line_status', 'totPrdAmt': 'items_total', 'dlvCst': 'shipping_fee',
    'totPayAmt': 'total_paid', 'rcvrNm': 'recipient', 'zipNo': 'postal_code', 'baseAddr': 'street_address',
    'dtlAddr': 'city_region_country', 'dlvStatCd': 'delivery_status', 'dlvCoNm': 'carrier', 'invcNo': 'tracking_number',
    'dlvStrtDtm': 'shipped_at', 'clmList': 'claims',
    # sales analysis
    'srchStrtDt': 'from_date', 'srchEndDt': 'to_date', 'cmprBaseCd': 'compare_to', 'saleAmt': 'revenue',
    'ordCnt': 'order_count', 'cmprSaleAmt': 'compare_revenue', 'cmprOrdCnt': 'compare_order_count',
    'diffAmt': 'revenue_change', 'diffRt': 'change_rate',
    # save results
    'resultCd': 'result_code', 'resultMsg': 'result_message', 'procCnt': 'saved_rows', 'rowNo': 'row',
}

GRADE = 'Member grade code: G00 is every shopper, then G01, G02… by tier rank (the member grade list has them).'
DESCRIBE = {
    'tgtMbrGrdCd': GRADE, 'mbrGrdCd': GRADE, 'aplyMbrGrdCd': 'Price for this member grade. ' + GRADE,
    'clmAmtFrom': 'Claims of at least this amount (store currency).',
    'aplyDtm': 'Prices as of this date-time.',
    'srchStrtDtm': 'Promotions active at any time from this date-time.',
    'srchEndDtm': 'Promotions active at any time until this date-time.',
    'dcRt': 'Percent off.',
    # screens/mod.rs Paging::new: page numbers start at 1; at most 100 rows a page, 20 when not sent.
    'pageNo': 'Page number, from 1.',
    'pageSize': 'Rows per page, 1 to 100 (20 when not sent).',
    'rowStat': 'insert adds a row; update changes the status of an existing row; delete ends it.',
    'prmtStatCd': 'Promotion status. In a save row with row_action update: paused pauses it, ended ends it.',
    # ord.rs: the popup reads get_order with ordNo as the order key (a bare number is not found there;
    # the gateway looks the number up, see HANDLES).
    'ordNo': 'Order key such as ord_20402 (order_id in order and claim rows).',
    'ordDtmFrom': 'Orders placed on or after this day (YYYY-MM-DD, store time).',
    'ordDtmTo': 'Orders placed on or before this day (YYYY-MM-DD, store time).',
    'dlvStrtDtm': "When the parcel left: the carrier's first scan.",
}

# Each screen's body, as one sentence (summary) and the words people use for it (keywords).
SCREENS = {
    'getPrdGridList': ('Search products by keyword, category, availability, stock range, member-grade price and '
                       'date; one page of rows (no total).', ['product', 'stock', 'inventory', 'price', 'catalog']),
    'getPrdGridListCnt': ('Count the products a product search would return.', ['product', 'count', 'how many']),
    'getPrdDtlInfo': ('One product: price, member price, stock, availability, cost, approval status.', ['product', 'detail']),
    'getPrdDtlInfoV2': ('One product with its variants (color, size, stock each) and attributes (for example fit, '
                        'material).', ['product', 'variant', 'size', 'color', 'attribute', 'detail']),
    'getMbrGrdList': ('List member grades (tiers) with their grade codes, names, member counts and rank.',
                      ['tier', 'grade', 'loyalty', 'member']),
    'getPrmtTgtMbrList': ('Search members (customers) by grade, status or keyword; one page of rows.',
                          ['member', 'customer', 'shopper']),
    'getPrmtTgtMbrListCnt': ('Count the members a member search would return.', ['member', 'customer', 'count']),
    'getPrmtGridList': ('Search promotions (sales, discounts) by status, name, target grade and active period; '
                        'one page of rows.', ['promotion', 'sale', 'discount', 'campaign', 'running']),
    'getPrmtGridListCnt': ('Count the promotions a promotion search would return.', ['promotion', 'count']),
    'savePrmtList': ('Save promotion rows at once: insert creates a percent-off sale price promotion for a category '
                     'or products (types item_price_everyone or item_price_one_grade); update pauses or ends one; '
                     'delete ends one. Runs immediately.', ['promotion', 'sale', 'discount', 'markdown', 'pause', 'end']),
    'saveCpnList': ('Create coupons (insert rows only) for a promotion and member grade. Runs immediately.',
                    ['coupon', 'code', 'voucher']),
    'getDispCornerList': ('List the display corners (slots) of a page type and their scheduled banners in a period.',
                          ['banner', 'hero', 'display', 'homepage', 'slot']),
    'saveDispBnrList': ('Schedule banners into display corners (insert rows only). Runs immediately.',
                        ['banner', 'hero', 'display', 'schedule']),
    'getClmGridList': ('Search return claims by status, reason and minimum amount; one page of rows (no total).',
                       ['return', 'claim', 'refund', 'request']),
    'getClmGridListCnt': ('Count the claims a claim search would return.', ['return', 'claim', 'count']),
    'getRfndPopInitData': ('One claim before refunding it: liability, return fees, claim and refund estimate, '
                           'payment method, delivery date, claimed items.', ['refund', 'claim', 'return', 'detail']),
    'saveRfndProc': ('Refund one return claim to the original payment. Runs immediately.', ['refund', 'return', 'claim']),
    'saveCustMsgSend': ('Send a message to a customer (optionally about an order). Runs immediately.',
                        ['message', 'customer', 'email', 'notify', 'photos']),
    'getSaleAnlsGridList': ('Sales (revenue, order count) of a date range against a comparison basis, with the '
                            'change.', ['sales', 'revenue', 'orders', 'compare', 'drop']),
    'getOrdGridList': ('Search orders by status, order day range, member or keyword (a number finds that order '
                       'number, anything else the orderer by name, email or phone); one page of rows (no total).',
                       ['order', 'orders', 'status', 'purchase']),
    'getOrdGridListCnt': ('Count the orders an order search would return.', ['order', 'orders', 'count', 'how many']),
    'getOrdDtlPopInitData': ('One order: lines, totals, payment method, delivery address, the parcel (delivery status, '
                             'carrier, tracking number, shipped and delivered times) and the claims on it.',
                             ['order', 'detail', 'delivery', 'shipment', 'tracking', 'address', 'parcel']),
    'getCartList': ("The shopper's cart.", ['cart']),
    'saveCartList': ("Change the shopper's cart lines. Runs immediately.", ['cart']),
    'getOrdShtInitData': ("Prepare the shopper's order from the cart.", ['order', 'checkout']),
}

VOCABULARY = {'rename': RENAME, 'codes': CODES, 'describe': DESCRIBE}

# Fields that take a screen's key where people give the number they see: ord.rs reads get_order with
# ordNo as the key (`20402` is not found), and the order grid's keyword finds an order by its number.
# The gateway looks such a number up first: {screen: {field: (lookup screen, its search field, key field)}}.
HANDLES = {
    'getOrdDtlPopInitData': {'ordNo': ('getOrdGridList', 'srchKwd', 'ordNo')},
    'saveCustMsgSend': {'ordNo': ('getOrdGridList', 'srchKwd', 'ordNo')},
}

# The abbreviations in the screen names, spelled out as the field names above spell them
# (ToolCatalogImporter words): getOrdGridListCnt -> get_order_grid_list_count.
WORDS = {'clm': 'claim', 'cnt': 'count', 'disp': 'display', 'mbr': 'member', 'grd': 'grade', 'ord': 'order',
         'dtl': 'detail', 'pop': 'popup', 'prd': 'product', 'prmt': 'promotion', 'tgt': 'target', 'rfnd': 'refund',
         'anls': 'analysis', 'cpn': 'coupon', 'cust': 'customer', 'msg': 'message', 'bnr': 'banner', 'proc': 'process'}


def facade_options(items):
    """convert() operation options for the screens in a facade manifest."""
    options = {}
    for item in items:
        summary, keywords = SCREENS.get(item['tool'], (item.get('summary') or item['tool'], []))
        options[item['tool']] = {'effect': 'read' if item.get('kind') == 'read' else 'write', 'summary': summary,
                                 'keywords': keywords}
    return options


def error_detail(status, body):
    """The back end's sentence (and the tool it suggests next, on the A-Commerce tools). Screen field
    names it quotes (`tgtMbrGrdCd`) are shown by their readable names, as the model knows them."""
    error = body.get('error') if isinstance(body, dict) else None
    if not isinstance(error, dict) or not isinstance(error.get('message'), str):
        return None
    hint = f" Next: {error['next_tool']}." if isinstance(error.get('next_tool'), str) and error['next_tool'] else ''
    message = re.sub(r'`([A-Za-z][A-Za-z0-9]*)`', lambda match: '`' + RENAME.get(match[1], match[1]) + '`', error['message'])
    return message + hint
