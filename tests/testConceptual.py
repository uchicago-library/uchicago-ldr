import unittest
from uchicagoldr.keyvaluepair import KeyValuePair as KVP
from uchicagoldr.keyvaluepairlist import KeyValuePairList as KVPList
from uchicagoldr.family import Family


class TestKeyValuePair(unittest.TestCase):
    def testMintSingle(self):
        kvp = KVP('test key', 'test value')
        self.assertTrue(kvp)

    def testMintMany(self):
        many = []
        for i in range(100):
            kvp = KVP('key_'+str(i), 'value_'+str(i))
            self.assertTrue(kvp)
            many.append(kvp)
        self.assertEqual(len(many), 100)

    def testJustKey(self):
        kvp = KVP('key')
        self.assertTrue(kvp)

    def testGoodKey(self):
        kvp = KVP('this key is a string', 'test value')
        self.assertTrue(kvp)
        kvp = KVP('this key is still a string', 5)
        self.assertTrue(kvp)

    def testBadKey(self):
        with self.assertRaises(TypeError):
            kvp = KVP(1, 'test')
        with self.assertRaises(TypeError):
            kvp = KVP([], 'test')
        with self.assertRaises(TypeError):
            kvp = KVP({}, 'test')
        with self.assertRaises(TypeError):
            kvp = KVP(float(1), 'test')

    def testBadValue(self):
        with self.assertRaises(TypeError):
            kvp = KVP('test', [])
        with self.assertRaises(TypeError):
            kvp = KVP('test', {})
        with self.assertRaises(TypeError):
            kvp = KVP('test', KVP())

    def testGoodValueStr(self):
        kvp = KVP('test', 'string')
        self.assertTrue(kvp)

    def testgoodValueInt(self):
        kvp = KVP('test', 1)
        self.assertTrue(kvp)

    def testGoodValueFloat(self):
        kvp = KVP('test', float(1))
        self.assertTrue(kvp)

    def testGoodValueComplex(self):
        kvp = KVP('test', complex(1))
        self.assertTrue(kvp)

    def testEqual(self):
        kvp1=KVP('this', 'that')
        kvp2=KVP('this', 'that')
        kvp3=KVP('test', 1)
        kvp4=KVP('test', 1)
        self.assertTrue((kvp1 == kvp2) and (kvp3 == kvp4))

    def testNotEqual(self):
        kvp1=KVP('this', 'that')
        kvp2=KVP('this', 'again')
        kvp3=KVP('test', 1)
        self.assertFalse(kvp1 == kvp3)
        self.assertFalse(kvp1 == kvp2)

    def testGetKey(self):
        kvp1=KVP('test_key', 'test_value')
        self.assertEqual(kvp1.get_key(),'test_key')

    def testGetValue(self):
        kvp1=KVP('test_key', 'test_value')
        self.assertEqual(kvp1.get_value(), 'test_value')
        kvp2=KVP('test_nested_key', 'test_nested_value')
        kvps=KVPList()
        kvps.append(kvp2)
        kvp3=KVP('test_nest',kvps)
        self.assertTrue(kvp3.get_value())

    def testNestedDetection(self):
        kvp2=KVP('test_nested_key', 'test_nested_value')
        kvps=KVPList()
        kvps.append(kvp2)
        kvp3=KVP('test_nest',kvps)
        self.assertTrue(kvp3)
        self.assertTrue(kvp3.nested)

    def testGetNested(self):
        kvp2=KVP('test_nested_key', 'test_nested_value')
        kvps=KVPList()
        kvps.append(kvp2)
        kvp3=KVP('test_nest',kvps)
        self.assertTrue(kvp3)
        self.assertTrue(kvp3.is_nested())
        kvp4=KVP('test','test')
        self.assertFalse(kvp4.is_nested())

    def testCollisions(self):
        pass

class testKeyValuePairList(unittest.TestCase):
    def testMint(self):
        kvp=KVP('test', 'test')
        kvps=KVPList()
        kvps.append(kvp)
        self.assertTrue(kvps)

    def testEmpty(self):
        kvps=KVPList()
        self.assertFalse(kvps)

class testFamily(unittest.TestCase):
#    def setUp(self):
#        self.family1=Family(descs=KVPList([KVP('1','1')]))
#        self.family2=Family(descs=KVPList([KVP('2','2')]))
#        self.family3=Family(descs=KVPList([KVP('3','3')]))
#        self.family4=Family(descs=KVPList([KVP('4','4')]))
#        self.family5=Family(descs=KVPList([KVP('5','5')]))
#        self.family6=Family(descs=KVPList([KVP('6','6')]))
#        self.family7=Family(descs=KVPList([KVP('7','7')]))
#        self.family8=Family(descs=KVPList([KVP('8','8')]))
#        self.family9=Family(descs=KVPList([KVP('9','9')]))
#        self.family10=Family(descs=KVPList([KVP('10','10')]))

    def testInitChildren(self):
        self.family10=None
        self.family9=None
        self.family8=None
        self.family7=None
        self.family6=None
        self.family5=None
        self.family4=None
        self.faimly3=None
        self.family2=None
        self.family1=None

        self.family10=Family(descs=KVPList([KVP('10','10')]))
        self.family9=Family(descs=KVPList([KVP('9','9')]))
        self.family8=Family(descs=KVPList([KVP('8','8')]))
        self.family7=Family(descs=KVPList([KVP('7','7')]))
        self.family6=Family(descs=KVPList([KVP('6','6')]))
        self.family5=Family(descs=KVPList([KVP('5','5')]))
        self.family4=Family(descs=KVPList([KVP('4','4')]),children=[self.family9,self.family10])
        self.family3=Family(descs=KVPList([KVP('3','3')]),children=[self.family7,self.family8])
        self.family2=Family(descs=KVPList([KVP('2','2')]),children=[self.family5,self.family6])
        self.family1=Family(descs=KVPList([KVP('1','1')]),children=[self.family2,self.family3,self.family4])

        self.assertEquals(len(self.family1.children),3)
        self.assertEquals(len(self.family2.children),2)
        self.assertEquals(len(self.family3.children),2)
        self.assertEquals(len(self.family4.children),2)
        self.assertEquals(len(self.family5.children),0)
        self.assertEquals(len(self.family6.children),0)
        self.assertEquals(len(self.family7.children),0)
        self.assertEquals(len(self.family8.children),0)
        self.assertEquals(len(self.family9.children),0)
        self.assertEquals(len(self.family10.children),0)

    def testAddChild(self):
        self.family10=None
        self.family9=None
        self.family8=None
        self.family7=None
        self.family6=None
        self.family5=None
        self.family4=None
        self.faimly3=None
        self.family2=None
        self.family1=None

        self.family10=Family(descs=KVPList([KVP('10','10')]))
        self.family9=Family(descs=KVPList([KVP('9','9')]))
        self.family8=Family(descs=KVPList([KVP('8','8')]))
        self.family7=Family(descs=KVPList([KVP('7','7')]))
        self.family6=Family(descs=KVPList([KVP('6','6')]))
        self.family5=Family(descs=KVPList([KVP('5','5')]))
        self.family4=Family(descs=KVPList([KVP('4','4')]))
        self.family3=Family(descs=KVPList([KVP('3','3')]))
        self.family2=Family(descs=KVPList([KVP('2','2')]))
        self.family1=Family(descs=KVPList([KVP('1','1')]))

        self.family1.add_child(self.family2)
        self.family1.add_child(self.family3)
        self.family1.add_child(self.family4)
        self.family2.add_child(self.family5)
        self.family2.add_child(self.family6)
        self.family3.add_child(self.family7)
        self.family3.add_child(self.family8)
        self.family4.add_child(self.family9)
        self.family4.add_child(self.family10)

        self.assertEquals(len(self.family1.children),3)
        self.assertEquals(len(self.family2.children),2)
        self.assertEquals(len(self.family3.children),2)
        self.assertEquals(len(self.family4.children),2)
        self.assertEquals(len(self.family5.children),0)
        self.assertEquals(len(self.family6.children),0)
        self.assertEquals(len(self.family7.children),0)
        self.assertEquals(len(self.family8.children),0)
        self.assertEquals(len(self.family9.children),0)
        self.assertEquals(len(self.family10.children),0)

    def testInfinFamilyDetect(self):
        self.family10=None
        self.family9=None
        self.family8=None
        self.family7=None
        self.family6=None
        self.family5=None
        self.family4=None
        self.faimly3=None
        self.family2=None
        self.family1=None

        self.family10=Family(descs=KVPList([KVP('10','10')]))
        self.family9=Family(descs=KVPList([KVP('9','9')]))
        self.family8=Family(descs=KVPList([KVP('8','8')]))
        self.family7=Family(descs=KVPList([KVP('7','7')]))
        self.family6=Family(descs=KVPList([KVP('6','6')]))
        self.family5=Family(descs=KVPList([KVP('5','5')]))
        self.family4=Family(descs=KVPList([KVP('4','4')]))
        self.family3=Family(descs=KVPList([KVP('3','3')]))
        self.family2=Family(descs=KVPList([KVP('2','2')]))
        self.family1=Family(descs=KVPList([KVP('1','1')]))

        self.family1.add_child(self.family2)
        self.family1.add_child(self.family3)
        self.family1.add_child(self.family4)
        self.family2.add_child(self.family5)
        self.family2.add_child(self.family6)
        self.family3.add_child(self.family7)
        self.family3.add_child(self.family8)
        self.family4.add_child(self.family9)
        self.family4.add_child(self.family10)
        with self.assertRaises(RecursionError):
            self.family5.add_child(self.family2)
        with self.assertRaises(RecursionError):
             self.family8.add_child(self.family1)


    def testFamilyPrint(self):
        self.family10=None
        self.family9=None
        self.family8=None
        self.family7=None
        self.family6=None
        self.family5=None
        self.family4=None
        self.faimly3=None
        self.family2=None
        self.family1=None

        self.family10=Family(descs=KVPList([KVP('10','10')]))
        self.family9=Family(descs=KVPList([KVP('9','9')]))
        self.family8=Family(descs=KVPList([KVP('8','8')]))
        self.family7=Family(descs=KVPList([KVP('7','7')]))
        self.family6=Family(descs=KVPList([KVP('6','6')]))
        self.family5=Family(descs=KVPList([KVP('5','5')]))
        self.family4=Family(descs=KVPList([KVP('4','4')]))
        self.family3=Family(descs=KVPList([KVP('3','3')]))
        self.family2=Family(descs=KVPList([KVP('2','2')]))
        self.family1=Family(descs=KVPList([KVP('1','1')]))

        self.family1.add_child(self.family2)
        self.family1.add_child(self.family3)
        self.family1.add_child(self.family4)
        self.family2.add_child(self.family5)
        self.family2.add_child(self.family6)
        self.family3.add_child(self.family7)
        self.family3.add_child(self.family8)
        self.family4.add_child(self.family9)
        self.family4.add_child(self.family10)

        self.assertEquals(len(self.family1.children),3)
        self.assertEquals(len(self.family2.children),2)
        self.assertEquals(len(self.family3.children),2)
        self.assertEquals(len(self.family4.children),2)
        self.assertEquals(len(self.family5.children),0)
        self.assertEquals(len(self.family6.children),0)
        self.assertEquals(len(self.family7.children),0)
        self.assertEquals(len(self.family8.children),0)
        self.assertEquals(len(self.family9.children),0)
        self.assertEquals(len(self.family10.children),0)
        self.assertTrue(self.family1.__repr__())
        self.assertTrue(self.family1.__str__())
        print("\n"+self.family1.__str__())

if __name__ == '__main__':
    unittest.main()
