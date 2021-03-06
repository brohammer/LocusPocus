#!/usr/bin/python3

from locuspocus.locusdb import MemLocusDB
from . import LocusBase

class MemLocus(LocusBase,MemLocusDB):

    def __init__(
        self,
        chromosome: str,
        start: int,
        end: int,

        source: str = 'locuspocus',
        feature_type: str = 'locus',
        strand: str = '+',
        frame: int = None,
        name: str = None,

        # Extra locus stuff
        attrs: dict = None,
        parent = None,
        children = None

    ):
        super().__init__()
        # this starts a transaction
        with self._db:
            cur = self._db.cursor()
            # insert the core feature data
            cur.execute(
                '''
                INSERT INTO loci 
                    (chromosome,start,end,source,feature_type,strand,frame,name)
                    VALUES (?,?,?,?,?,?,?,?)
                ''',(
                # chrom/start/end are required, so cast them
                (str(chromosome),int(start),int(end),
                 source,feature_type,strand,frame,name))
            )
            # get the fresh LID
            (LID,) = cur.execute('SELECT last_insert_rowid()').fetchone()
            if LID is None: #pragma: no cover
                # I dont know when this would happen without another exception being thrown
                raise ValueError(f"{locus} was not assigned a valid LID!")
            # Check to see if the locus is a primary feature
            cur.execute(
                '''
                INSERT INTO positions 
                (LID,start,end,chromosome) 
                VALUES (?,?,?,?)
                ''',
                (LID,start,end,chromosome)
            )
            self._LID = LID

            # Add the key val pairs
            if attrs is not None:
                for key,val in attrs.items():
                    self[key] = val          

            # Handle Parent Child Relationships
            self.parent = parent
            self.children = children

 
