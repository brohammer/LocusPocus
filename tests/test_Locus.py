import pytest
import numpy as np

from itertools import chain
from locuspocus import Locus

@pytest.fixture
def simple_Locus():
    return Locus(1,100,200,attrs={'foo':'bar'}) 

def test_initialization(simple_Locus):
    # numeric chromosomes
    assert simple_Locus.chromosome == 1
    assert simple_Locus.start == 100
    assert simple_Locus.end == 200
    assert len(simple_Locus) == 101

def test_as_dict(simple_Locus):
    simple_Locus_dict = {
            'chromosome': 1, 
            'start': 100, 
            'end': 200, 
            'source': 'locuspocus', 
            'feature_type': None, 
            'strand': '+', 
            'frame': None, 
            'name': None, 
            '_frozen': True, 
            '_LID': None
    }
    assert simple_Locus.as_dict() == simple_Locus_dict

def test_frozen(simple_Locus):
    try:
        # This should throw an exception
        simple_Locus.chromosome = 2
    except Exception as e:
        return True


def test_setitem(simple_Locus):
    try:
        # This should throw an exception
        simple_Locus['foo'] = 'baz'
    except Exception as e:
        return True


def test_getitem(simple_Locus):
    assert simple_Locus['foo'] == 'bar'

def test_default_getitem(simple_Locus):
    assert simple_Locus.default_getitem('name', 'default') == 'default'

def test_start(simple_Locus):
    assert simple_Locus.start == 100

def test_end(simple_Locus):
    assert simple_Locus.end == 200

def test_coor(simple_Locus):
    assert simple_Locus.coor == (100, 200)

def test_upstream(simple_Locus):
    assert simple_Locus.upstream(50) == 50

def test_downstream(simple_Locus):
    assert simple_Locus.downstream(50) == 250

def test_name(simple_Locus):
    assert simple_Locus.name is None

def test_eq(simple_Locus):
    another_Locus = Locus(1, 110, 220)
    assert simple_Locus == simple_Locus
    assert simple_Locus != another_Locus

def test_loci_eq(testRefGen):
    '''
        Test the equals operator
    '''
    x = testRefGen['GRMZM2G018447']
    y = testRefGen['GRMZM2G018447']
    assert x == y

def test_loci_lt_by_chrom(testRefGen):
    x = Locus('1',1,1)
    y = Locus('2',1,1)
    assert x < y

def test_loci_gt_by_chrom(testRefGen):
    x = Locus('1',1,1)
    y = Locus('2',1,1)
    assert y > x

def test_loci_lt_by_pos(testRefGen):
    x = Locus('1',1,100)
    y = Locus('1',2,100)
    assert x < y

def test_loci_gt_by_pos(testRefGen):
    x = Locus('1',1,100)
    y = Locus('1',2,200)
    assert y > x

def test_len(simple_Locus):
    assert len(simple_Locus) == 101
    assert len(Locus(1, 100, 100)) == 1

def test_lt(simple_Locus):
    same_chrom_Locus = Locus(1, 110, 220)
    diff_chrom_Locus = Locus(2, 90, 150)
    assert simple_Locus < same_chrom_Locus
    assert simple_Locus < diff_chrom_Locus

def test_gt(simple_Locus):
    same_chrom_Locus = Locus(1, 90, 150)
    diff_chrom_Locus = Locus(2, 90, 150)
    assert simple_Locus > same_chrom_Locus
    assert diff_chrom_Locus > simple_Locus


def test_repr(simple_Locus):
    assert repr(simple_Locus) == "Locus(chromosome=1, start=100, end=200, source='locuspocus', feature_type=None, strand='+', frame=None, name=None)"

def test_hash(simple_Locus):
    assert hash(simple_Locus) == 1470741785701407904

