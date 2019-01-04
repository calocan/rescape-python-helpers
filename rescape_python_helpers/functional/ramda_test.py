from snapshottest import TestCase

from rescape_python_helpers.functional.ramda import to_dict_deep, all_pass_dict
from . import ramda as R

class TestRamda(TestCase):

    def test_filter_dict(self):
        dct = R.filter_dict(lambda keyvalue: keyvalue[0] == 'a', dict(a=1, b=2))
        assert dct == dict(a=1)

    def test_all_pass_dict(self):
        assert all_pass_dict(lambda k, v: v, dict(a=1, b=1))
        assert not all_pass_dict(lambda k, v: v, dict(a=1, b=None))
        assert not all_pass_dict(lambda k, v: v == 2, dict(a=1, b=1))

    def test_map_prop_value_as_index(self):
        res = R.map_prop_value_as_index(
            'province',
            [
                dict(province="Alberta"),
                dict(province="Manitoba")
            ]
        )
        assert res == dict(Alberta=dict(province="Alberta"), Manitoba=dict(province="Manitoba"))

    def test_item_path_or(self):
        assert R.item_path_or('racehorse', ['one', 'one', 'was'], dict(one=dict(one=dict(was='a')))) == 'a'
        assert R.item_path_or('racehorse', ['one', 'one', 'is'], dict(one=dict(one=dict(was='a')))) == 'racehorse'
        assert R.item_path_or('racehorse', 'one.one.was', dict(one=dict(one=dict(was='a')))) == 'a'

        # Try with a mix of dict and obj
        class Fellow(object):
            def __init__(self, one):
                self.one = one
        assert R.item_path_or('racehorse', 'one.one.was', dict(one=Fellow(one=dict(was='a')))) == 'a'

    def test_omit_deep(self):
        omit_keys = ['foo', 'bar']
        dct = dict(foo=1, bar=2, car=dict(foo=3, bar=4, tar=5, pepper=[[dict(achoo=1, bar=2), dict(kale=1, foo=2)]]))
        assert R.omit_deep(omit_keys, dct) == dict(car=dict(tar=5, pepper=[[dict(achoo=1), dict(kale=1)]]))

    def test_filter_deep(self):
        # This should pass
        params1 = dict(
            foo=1,
            car=dict(foo=3)
        )
        # This should fail
        params2 = dict(
            foo=1,
            car=dict(tool=3)
        )
        # This should pass
        params3 = dict(
        )
        # This should pass
        params4 = dict(
            car=dict(
                pepper=[
                    [
                        dict(achoo=1),
                        dict(kale=1)
                    ]
                ]
            )
        )
        # This should fail
        params5 = dict(
            car=dict(
                pepper=[
                    [
                        dict(achoo=1),
                        dict(kale=1),
                        dict(shoe=1)
                    ]
                ]
            )
        )

        dct = dict(
            foo=1,
            bar=2,
            car=dict(
                foo=3,
                bar=4,
                tar=5,
                pepper=[
                    [
                        dict(achoo=1, bar=2),
                        dict(kale=1, foo=2)]
                ]
            )
        )
        assert R.dict_matches_params_deep(params1, dct)
        assert not R.dict_matches_params_deep(params2, dct)
        assert R.dict_matches_params_deep(params3, dct)
        assert R.dict_matches_params_deep(params4, dct)
        assert not R.dict_matches_params_deep(params5, dct)

    def test_prop(self):
        assert R.prop('obazda', dict(obazda='dip')) == 'dip'

        # Try with a mix of dict and obj
        class Radish(object):
            def __init__(self, cut):
                self.garnish = cut
        assert R.prop('garnish', Radish('spiraled')) == 'spiraled'

    def test_merge_deep_all(self):
        assert R.merge_deep_all([
            dict(a=1, zoo=dict(a=2, b=2)),
            dict(a=2, zoo=dict(a=3, c=4, pen=dict(bull=False)), nursery=[1]),
            dict(zoo=dict(d=4, e=4, pen=dict(cow=True)), nursery=[2]),
        ]) == dict(
            a=2,
            zoo=dict(a=3, b=2, c=4, d=4, e=4, pen=dict(bull=False, cow=True)),
            nursery=[1,2]
        )

    def test_to_dict_deep(self):
        class Beobazte(object):
            def __init__(self):
                self.cream = 'yummy'
        class Radish(object):
            def __init__(self, cut):
                self.garnish = Beobazte()
                self.cut = cut
        assert to_dict_deep(Radish('spiraled')) == dict(garnish=dict(cream='yummy'), cut='spiraled')
