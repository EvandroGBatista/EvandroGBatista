import pytest
import viola
import sys, os
import pandas as pd
import filecmp
from io import StringIO
HERE = os.path.abspath(os.path.dirname(__file__))
HEADER = """##fileformat=VCFv4.1
##contig=<ID=chr1,length=195471971>
##contig=<ID=chr2,length=182113224>
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END">
##INFO=<ID=CIGAR,Number=A,Type=String,Description="CIGAR alignment for each alternate indel allele">
##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakend">
##INFO=<ID=EVENT,Number=1,Type=String,Description="ID of event associated to breakend">
##INFO=<ID=HOMLEN,Number=.,Type=Integer,Description="Length of base pair identical homology at event breakpoints">
##INFO=<ID=HOMSEQ,Number=.,Type=String,Description="Sequence of base pair identical homology at event breakpoints">
##INFO=<ID=SVINSLEN,Number=.,Type=Integer,Description="Length of insertion">
##INFO=<ID=SVINSSEQ,Number=.,Type=String,Description="Sequence of insertion">
##INFO=<ID=LEFT_SVINSSEQ,Number=.,Type=String,Description="Known left side of insertion for an insertion of unknown length">
##INFO=<ID=RIGHT_SVINSSEQ,Number=.,Type=String,Description="Known right side of insertion for an insertion of unknown length">
##INFO=<ID=CONTIG,Number=1,Type=String,Description="Assembled contig sequence">
##INFO=<ID=BND_DEPTH,Number=1,Type=Integer,Description="Read depth at local translocation breakend">
##INFO=<ID=MATE_BND_DEPTH,Number=1,Type=Integer,Description="Read depth at remote translocation mate breakend">
##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="Somatic mutation">
##INFO=<ID=SOMATICSCORE,Number=1,Type=Integer,Description="Somatic variant quality score">
##INFO=<ID=JUNCTION_SOMATICSCORE,Number=1,Type=Integer,Description="If the SV junctino is part of an EVENT (ie. a multi-adjacency variant), this field provides the SOMATICSCORE value for the adjacency in question only">
##INFO=<ID=INV3,Number=0,Type=Flag,Description="Inversion breakends open 3' of reported location">
##INFO=<ID=INV5,Number=0,Type=Flag,Description="Inversion breakends open 5' of reported location">
##FORMAT=<ID=PR,Number=.,Type=Integer,Description="Spanning paired-read support for the ref and alt alleles in the order listed">
##FORMAT=<ID=SR,Number=.,Type=Integer,Description="Split reads for the ref and alt alleles in the order listed, for reads where P(allele|read)>0.999">
##FILTER=<ID=MaxDepth,Description="Normal sample site depth is greater than 3x the median chromosome depth near one or both variant breakends">
##FILTER=<ID=MinSomaticScore,Description="Somatic score is less than 30">
##FILTER=<ID=MaxMQ0Frac,Description="For a small variant (<1000 bases) in the normal sample, the fraction of reads with MAPQ0 around either breakend exceeds 0.4">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INS,Description="Insertion">
##ALT=<ID=DUP:TANDEM,Description="Tandem Duplication">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	mouse1_N	mouse1_T
"""
class TestToBedpe:
    #manta_path = os.path.join(HERE, 'data/manta1.inv.vcf')
    #result = viola.read_vcf(manta_path)
    body = """chr1	82550461	test1	G	<DEL>	.	MinSomaticScore	END=82554225;SVTYPE=DEL;SVLEN=-3764;IMPRECISE;CIPOS=-51,52;CIEND=-51,52;SOMATIC;SOMATICSCORE=10	PR:SR	21,0:10,0	43,4:15,3
chr1	22814216	test2	T	<INV>	.	MinSomaticScore	END=92581131;SVTYPE=INV;SVLEN=69766915;IMPRECISE;CIPOS=-51,51;CIEND=-89,90;SOMATIC;SOMATICSCORE=11;INV5	PR	24,0	35,5
chr1	60567906	test3	T	<DEL>	.	MinSomaticScore	END=60675940;SVTYPE=DEL;SVLEN=-108034;CIPOS=-44,44;CIEND=-38,39;SOMATIC;SOMATICSCORE=18	PR	23,0	44,6
chr1	69583190	test4	T	<DEL>	.	PASS	END=69590947;SVTYPE=DEL;SVLEN=-7757;IMPRECISE;CIPOS=-123,123;CIEND=-135,136;SOMATIC;SOMATICSCORE=47	PR	21,0	20,12
"""
    b = StringIO(HEADER + body)
    result = viola.read_vcf(b)
    def test_to_bedpe_like(self):
        self.result.to_bedpe(os.path.join(HERE, 'data/out.bedpe'))
        assert filecmp.cmp(os.path.join(HERE, 'data/out.bedpe'), os.path.join(HERE, 'data/expected.bedpe'))

    def test_to_bedpe_like_with_info(self):
        self.result.to_bedpe(os.path.join(HERE, 'data/out.svlen.bedpe'), custom_infonames=['svlen'])
        assert filecmp.cmp(os.path.join(HERE, 'data/out.svlen.bedpe'), os.path.join(HERE, 'data/expected.svlen.bedpe'))