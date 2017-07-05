#!/usr/bin/env python3
import data as d


def test_get_dolphin_id():
    s = './aaa/bbb/ccc/ddd/123'
    assert d.get_dolphin_id(s) == 'ddd_123'

    s = '/aaa/bbb/ccc/Ku N123'
    assert d.get_dolphin_id(s) == 'ku_123'

    s = '/aaa/bbb/ccc/Ku123'
    assert d.get_dolphin_id(s) == 'ku_123'
