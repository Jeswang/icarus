from __future__ import division
import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
import collections

import numpy as np

import icarus.models as cache

class TestLinkedSet(unittest.TestCase):
    
    def link_consistency(self, linked_set):
        """Checks that links of a linked set are consistent iterating from top
        or from bottom.
        
        This method depends on the internal implementation of the LinkedSet
        class
        """
        topdown = collections.deque()
        bottomup = collections.deque()
        cur = linked_set._top
        while cur:
            topdown.append(cur.val)
            cur = cur.down
        cur = linked_set._bottom
        while cur:
            bottomup.append(cur.val)
            cur = cur.up
        bottomup.reverse()
        if topdown != bottomup:
            return False
        return list(reversed(list(linked_set))) == list(reversed(linked_set))
        
    def test_append_top(self):
        c = cache.LinkedSet()
        c.append_top(1)
        self.assertEqual(len(c), 1)
        self.assertEqual(list(c), [1])
        c.append_top(2)
        self.assertEqual(len(c), 2)
        self.assertEqual(list(c), [2, 1])
        c.append_top(3)
        self.assertEqual(len(c), 3)
        self.assertEqual(list(c), [3, 2, 1])
        self.assertTrue(self.link_consistency(c))
        self.assertRaises(KeyError, c.append_top, 2)

    def test_append_bottom(self):
        c = cache.LinkedSet()
        c.append_bottom(1)
        self.assertEqual(len(c), 1)
        self.assertEqual(list(c), [1])
        c.append_bottom(2)
        self.assertEqual(len(c), 2)
        self.assertEqual(list(c), [1, 2])
        c.append_bottom(3)
        self.assertEqual(len(c), 3)
        self.assertEqual(list(c), [1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        self.assertRaises(KeyError, c.append_top, 2)

    def test_move_to_top(self):
        c = cache.LinkedSet()
        c.append_top(1)
        c.move_to_top(1)
        self.assertEqual(list(c), [1])
        c.append_bottom(2)
        c.move_to_top(1)
        self.assertEqual(list(c), [1, 2])
        c.move_to_top(2)
        self.assertEqual(list(c), [2, 1])
        c.append_bottom(3)
        c.move_to_top(1)
        self.assertEqual(list(c), [1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        
    def test_move_to_bottom(self):
        c = cache.LinkedSet()
        c.append_top(1)
        c.move_to_bottom(1)
        self.assertEqual(list(c), [1])
        c.append_bottom(2)
        c.move_to_bottom(2)
        self.assertEqual(list(c), [1, 2])
        c.move_to_bottom(1)
        self.assertEqual(list(c), [2, 1])
        c.append_top(3)
        c.move_to_bottom(1)
        self.assertEqual(list(c), [3, 2, 1])
        self.assertTrue(self.link_consistency(c))
    
    def test_move_up(self):
        c = cache.LinkedSet()
        c.append_bottom(1)
        c.move_up(1)
        self.assertEqual(list(c), [1])
        c.append_bottom(2)
        c.move_up(1)
        self.assertEqual(list(c), [1, 2])
        c.move_up(2)
        self.assertEqual(list(c), [2, 1])
        c.append_bottom(3)
        c.move_up(3)
        self.assertEqual(list(c), [2, 3, 1])
        c.move_up(3)
        self.assertEqual(list(c), [3, 2, 1])
        self.assertTrue(self.link_consistency(c))
        self.assertRaises(KeyError, c.move_up, 4)
        
    def test_move_down(self):
        c = cache.LinkedSet()
        c.append_top(1)
        c.move_down(1)
        self.assertEqual(list(c), [1])
        c.append_top(2)
        c.move_down(1)
        self.assertEqual(list(c), [2, 1])
        c.move_down(2)
        self.assertEqual(list(c), [1, 2])
        c.move_down(2)
        self.assertEqual(list(c), [1, 2])
        c.append_top(3)
        self.assertEqual(list(c), [3, 1, 2])
        c.move_down(3)
        self.assertEqual(list(c), [1, 3, 2])
        c.move_down(3)
        self.assertEqual(list(c), [1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        self.assertRaises(KeyError, c.move_down, 4)
        
    def test_pop_top(self):
        c = cache.LinkedSet([1, 2, 3])
        evicted = c.pop_top()
        self.assertEqual(evicted, 1)
        self.assertEqual(list(c), [2, 3])
        self.assertTrue(self.link_consistency(c))
        evicted = c.pop_top()
        self.assertEqual(evicted, 2)
        self.assertEqual(list(c), [3])    
        self.assertTrue(self.link_consistency(c))
        evicted = c.pop_top()
        self.assertEqual(evicted, 3)
        self.assertEqual(list(c), [])
        evicted = c.pop_top()
        self.assertEqual(evicted, None)
        self.assertEqual(list(c), [])

    def test_pop_bottom(self):
        c = cache.LinkedSet([1, 2, 3])
        evicted = c.pop_bottom()
        self.assertEqual(evicted, 3)
        self.assertEqual(list(c), [1, 2])
        self.assertTrue(self.link_consistency(c))
        evicted = c.pop_bottom()
        self.assertEqual(evicted, 2)
        self.assertEqual(list(c), [1])
        self.assertTrue(self.link_consistency(c))
        evicted = c.pop_bottom()
        self.assertEqual(evicted, 1)
        self.assertEqual(list(c), [])
        evicted = c.pop_bottom()
        self.assertEqual(evicted, None)
        self.assertEqual(list(c), [])

    def test_insert_above(self):
        c = cache.LinkedSet([3])
        c.insert_above(3, 2)
        self.assertEqual(list(c), [2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_above(2, 1)
        self.assertEqual(list(c), [1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_above(1, 'a')
        self.assertEqual(list(c), ['a', 1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_above(2, 'b')
        self.assertEqual(list(c), ['a', 1, 'b', 2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_above(3, 'c')
        self.assertEqual(list(c), ['a', 1, 'b', 2, 'c', 3])
        self.assertTrue(self.link_consistency(c))

    def test_insert_below(self):
        c = cache.LinkedSet([1])
        c.insert_below(1, 2)
        self.assertEqual(list(c), [1, 2])
        self.assertTrue(self.link_consistency(c))
        c.insert_below(2, 3)
        self.assertEqual(list(c), [1, 2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_below(1, 'a')
        self.assertEqual(list(c), [1, 'a', 2, 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_below(2, 'b')
        self.assertEqual(list(c), [1, 'a', 2, 'b', 3])
        self.assertTrue(self.link_consistency(c))
        c.insert_below(3, 'c')
        self.assertEqual(list(c), [1, 'a', 2, 'b', 3, 'c'])
        self.assertTrue(self.link_consistency(c))
        
    def test_clear(self):
        c = cache.LinkedSet()
        c.append_top(1)
        c.append_top(2)
        self.assertEqual(len(c), 2)
        c.clear()
        self.assertEqual(len(c), 0)
        self.assertEqual(list(c), [])
        c.clear()

    def test_duplicated_elements(self):
        self.assertRaises(ValueError, cache.LinkedSet, iterable=[1, 1, 2])
        self.assertRaises(ValueError, cache.LinkedSet, iterable=[1, None, None])
        self.assertIsNotNone(cache.LinkedSet(iterable=[1, 0, None]))
class TestLruCache(unittest.TestCase):

    def test_lru(self):
        c = cache.LruCache(4)
        c.put(0)
        self.assertEquals(len(c), 1)
        c.put(2)
        self.assertEquals(len(c), 2)
        c.put(3)
        self.assertEquals(len(c), 3)
        c.put(4)
        self.assertEquals(len(c), 4)
        self.assertEquals(c.dump(), [4, 3, 2, 0])
        self.assertEquals(c.put(5), 0)
        self.assertEquals(c.put(5), None)
        self.assertEquals(len(c), 4)
        self.assertEquals(c.dump(), [5, 4, 3, 2])
        c.get(2)
        self.assertEquals(c.dump(), [2, 5, 4, 3])
        c.get(4)
        self.assertEquals(c.dump(), [4, 2, 5, 3])
        c.clear()
        self.assertEquals(len(c), 0)
        self.assertEquals(c.dump(), [])
        
    def test_remove(self):
        c = cache.LruCache(4)
        c.put(1)
        c.put(2)
        c.put(3)
        c.remove(2)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.dump(), [3, 1])
        c.put(4)
        c.put(5)
        self.assertEqual(c.dump(), [5, 4, 3, 1])
        c.remove(5)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [4, 3, 1])
        c.remove(1)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.dump(), [4, 3])
        
    def test_position(self):
        c = cache.LruCache(4)
        c.put(4)
        c.put(3)
        c.put(2)
        c.put(1)
        self.assertEqual(c.dump(), [1, 2, 3, 4])
        self.assertEqual(c.position(1), 0)
        self.assertEqual(c.position(2), 1)
        self.assertEqual(c.position(3), 2)
        self.assertEqual(c.position(4), 3)

class TestSlruCache(unittest.TestCase):

    def test_put_get(self):
        c = cache.SegmentedLruCache(9, 3)
        self.assertEqual(c.maxlen, 9)
        c.put(1)
        self.assertEqual(c.dump(), [[], [], [1]])
        c.put(2)
        self.assertEqual(c.dump(), [[], [], [2, 1]])
        c.put(3)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [[], [], [3, 2, 1]])
        c.get(2)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [[], [2], [3, 1]])
        c.get(2)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [[2], [], [3, 1]])
        c.put(4)
        self.assertEqual(len(c), 4)
        self.assertEqual(c.dump(), [[2], [], [4, 3, 1]])
        evicted = c.put(5)
        self.assertEqual(evicted, 1)
        self.assertEqual(len(c), 4)
        self.assertEqual(c.dump(), [[2], [], [5, 4, 3]])
        c.get(5)
        self.assertEqual(len(c), 4)
        self.assertEqual(c.dump(), [[2], [5], [4, 3]])
        c.put(6)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2], [5], [6, 4, 3]])
        c.get(6)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2], [6, 5], [4, 3]])
        c.get(3)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2], [3, 6, 5], [4]])
        c.get(4)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2], [4, 3, 6], [5]])
        c.get(4)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[4, 2], [3, 6], [5]])
        c.get(2)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2, 4], [3, 6], [5]])
        c.get(3)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[3, 2, 4], [6], [5]])
        c.get(3)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[3, 2, 4], [6], [5]])
        c.get(2)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[2, 3, 4], [6], [5]])
        c.get(6)
        self.assertEqual(len(c), 5)
        self.assertEqual(c.dump(), [[6, 2, 3], [4], [5]])
    
    def test_remove(self):
        c = cache.SegmentedLruCache(4, 2)
        c.put(2)
        c.put(2)
        c.put(1)
        c.put(1)
        c.put(4)
        c.put(3)
        self.assertEqual(c.dump(), [[1, 2], [3, 4]])
        c.remove(2)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [[1], [3, 4]])
        c.remove(1)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.dump(), [[], [3, 4]])
        c.remove(4)
        self.assertEqual(len(c), 1)
        self.assertEqual(c.dump(), [[], [3]])
        c.remove(3)
        self.assertEqual(len(c), 0)
        self.assertEqual(c.dump(), [[], []])
        
    def test_position(self):
        c = cache.SegmentedLruCache(4, 2)
        c.put(2)
        c.put(2)
        c.put(1)
        c.put(1)
        c.put(4)
        c.put(3)
        self.assertEqual(c.dump(), [[1, 2], [3, 4]])
        self.assertEqual(c.position(1), 0)
        self.assertEqual(c.position(2), 1)
        self.assertEqual(c.position(3), 2)
        self.assertEqual(c.position(4), 3)
        
    def test_has(self):
        c = cache.SegmentedLruCache(4, 2)
        c.put(2)
        c.put(2)
        c.put(1)
        c.put(1)
        c.put(4)
        c.put(3)
        self.assertEqual(c.dump(), [[1, 2], [3, 4]])
        self.assertTrue(c.has(1))
        self.assertTrue(c.has(2))
        self.assertTrue(c.has(3))
        self.assertTrue(c.has(4))
        self.assertFalse(c.has(5))

class TestFifoCache(unittest.TestCase):

    def test_fifo(self):
        c = cache.FifoCache(4)
        self.assertEquals(len(c), 0)
        c.put(1)
        self.assertEquals(len(c), 1)
        c.put(2)
        self.assertEquals(len(c), 2)
        c.put(3)
        self.assertEquals(len(c), 3)
        c.put(4)
        self.assertEquals(len(c), 4)
        self.assertEquals(c.dump(), [4, 3, 2, 1])
        c.put(5)
        self.assertEquals(len(c), 4)
        self.assertEquals(c.dump(), [5, 4, 3, 2])
        c.get(2)
        self.assertEquals(c.dump(), [5, 4, 3, 2])
        c.get(4)
        self.assertEquals(c.dump(), [5, 4, 3, 2])
        c.put(6)
        self.assertEquals(c.dump(), [6, 5, 4, 3])
        c.clear()
        self.assertEquals(len(c), 0)
        self.assertEquals(c.dump(), [])
    
    def test_remove(self):
        c = cache.FifoCache(4)
        c.put(1)
        c.put(2)
        c.put(3)
        c.remove(2)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.dump(), [3, 1])
        c.put(4)
        c.put(5)
        self.assertEqual(c.dump(), [5, 4, 3, 1])
        c.remove(5)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [4, 3, 1])
        

class TestRandCache(unittest.TestCase):
    
    def test_rand(self):
        c = cache.RandEvictionCache(4)
        self.assertEquals(len(c), 0)
        c.put(1)
        self.assertEquals(len(c), 1)
        c.put(2)
        self.assertEquals(len(c), 2)
        c.put(3)
        self.assertEquals(len(c), 3)
        c.put(4)
        self.assertEquals(len(c), 4)
        self.assertEquals(len(c.dump()), 4)
        for v in (1, 2, 3, 4):
            self.assertTrue(c.has(v))
        c.get(3)
        for v in (1, 2, 3, 4):
            self.assertTrue(c.has(v))
        c.put(5)
        self.assertEquals(len(c), 4)
        self.assertTrue(c.has(5))
        c.clear()
        self.assertEquals(len(c), 0)
        self.assertEquals(c.dump(), [])

    def test_remove(self):
        c = cache.RandEvictionCache(4)
        c.put(1)
        c.put(2)
        c.put(3)
        c.remove(2)
        self.assertEqual(len(c), 2)
        for v in (3, 1):
            self.assertTrue(c.has(v))
        c.put(4)
        c.put(5)
        for v in (5, 4, 3, 1):
            self.assertTrue(c.has(v))
        c.remove(5)
        self.assertEqual(len(c), 3)
        for v in (4, 3, 1):
            self.assertTrue(c.has(v))


class TestLfuCache(unittest.TestCase):

    def test_lfu(self):
        c = cache.LfuCache(4)
        self.assertEquals(len(c), 0)
        c.put(1)
        self.assertEquals(len(c), 1)
        c.put(2)
        self.assertEquals(len(c), 2)
        c.put(3)
        self.assertEquals(len(c), 3)
        c.put(4)
        self.assertEquals(len(c), 4)
        self.assertEquals(len(c.dump()), 4)
        for v in (1, 2, 3, 4):
            self.assertTrue(c.has(v))
        c.get(1)
        c.get(1)
        c.get(1)
        c.get(2)
        c.get(2)
        c.get(3)
        c.put(5)
        self.assertEquals(c.dump(), [1, 2, 3, 5])
        self.assertEquals(len(c), 4)
        self.assertTrue(c.has(5))
        c.clear()
        self.assertEquals(len(c), 0)
        self.assertEquals(c.dump(), [])
        
    def test_remove(self):
        c = cache.FifoCache(4)
        c.put(1)
        c.put(2)
        c.put(3)
        c.remove(2)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.dump(), [3, 1])
        c.put(4)
        c.put(5)
        self.assertEqual(c.dump(), [5, 4, 3, 1])
        c.remove(5)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dump(), [4, 3, 1])
        
        
class TestRandInsert(unittest.TestCase):
    
    def test_rand_insert(self):
        n = 100000
        p1 = 0.01
        p2 = 0.1
        rc1 = cache.rand_insert_cache(cache.LruCache(n), p1)
        rc2 = cache.rand_insert_cache(cache.LruCache(n), p2)
        for i in range(n):
            rc1.put(i)
            rc2.put(i)
        self.assertLess(len(rc1) - n*p1, 200)
        self.assertLess(len(rc2) - n*p2, 200)
        self.assertEqual(rc1.put.__name__, 'put')
        self.assertGreater(len(rc1.put.__doc__), 0)


class TestKetValCache(unittest.TestCase):
    
    def test_key_val_cache(self):
        c = cache.keyval_cache(cache.FifoCache(3))
        c.put(1,11)
        self.assertEqual(c.get(1), 11)
        c.put(1, 12)
        self.assertEqual(c.get(1), 12)
        self.assertEqual(c.dump(), [(1, 12)])
        c.put(2, 21)
        self.assertTrue(c.has(1))
        self.assertTrue(c.has(2))
        c.put(3, 31)
        k, v = c.put(4, 41)
        self.assertEqual((k, v), (1, 12))
        c.clear()
        self.assertEqual(len(c), 0)
        self.assertEqual(c.get.__name__, 'get')
        self.assertEqual(c.put.__name__, 'put')
        self.assertEqual(c.dump.__name__, 'dump')
        self.assertEqual(c.clear.__name__, 'clear')