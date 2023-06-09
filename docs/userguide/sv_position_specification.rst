.. _sv_position_specification:

==========================================
Specification of SV positions in Viola
==========================================

The specification of SV positions varies from SV caller to SV caller.
It can be misleading to know exactly which genomic coordinates the SV of interest is located in.

Viola normalises the output of different SV callers and provides a well-defined specification.

Here we will explain how Viola normalises the position of SVs, with graphical examples for better understanding.

----------------------------------------
Deletion
----------------------------------------

First, we'll start from "Deletion".

.. image:: ../_static/sv_position_figures/del_image.png

The top of the figure is the reference sequence.

When "Deletion" occurs, two breakends appear. In this figure, one breakend is position 20 and another is 26 (middle). 

These two breakends consists one breakpoint (bottom).

.. image:: ../_static/sv_position_figures/del_vcf.png

This "Deletion" event is recorded in VCF format, as shown above.
Normally, there are two ways of writing down a "Deletion" event; breakend-based recording and breakpoint-based recording.

Gridss, for example, employs breakend-based recording system. Since two breakends arise from one "Deletion" event, the VCF has two lines of SV record (top).
Manta, Delly, and Lumpy uses breakpoint-based recording for Deletion, so only one line indicates the event.

.. image:: ../_static/sv_position_figures/del_viola.png

Viola object like :ref:`viola.Vcf<vcf>` and :ref:`viola.Bedpe<bedpe>` stores SV position in the table named ``positions``. 
The figure shown just above is the content of ``positions`` table.

The positions in this table is breakend-based, such that the ``pos1`` and ``pos2`` columns indicate the genomic coordinates of two breakends.
Strands for each breakend are written in ``strand1`` and ``strand2`` fields, where '+' means 3' half is missing, and vice versa.

Whether the SV records will be two lines or one line depends on the SV caller by which the input VCF is made.

If you want to convert breakend-based notation into breakpoint-based one, consider using :doc:`viola.Vcf.breakend2breakpoint()<../reference/api/viola.Vcf.breakend2breakpoint>`.


.. image:: ../_static/sv_position_figures/del_bedpe.png

Viola supports BEDPE output (See :doc:`viola.Vcf.to_bedpe()<../reference/api/viola.Vcf.to_bedpe>`). The BEDPE specification is written in `bedtools documentation`_.

.. _bedtools documentation: https://bedtools.readthedocs.io/en/latest/content/general-usage.html

For further understandings, we will show how Viola exports BEDPE exactly.

- ``end1`` and ``end2`` columns of BEDPE are exactly same as ``pos1`` and ``pos2`` columns of Viola's ``positions`` table.
- ``start1`` and ``start2`` columns are 0-origin position, so the following formula holds: ``start1`` + 1 = ``end1``, ``start2`` + 1 = ``end2``


----------------------------
Duplication
----------------------------

Next, let's move on "Duplication", especially "Tandem Duplication" where a certain segment is duplicated exactly next to the other.

.. image:: ../_static/sv_position_figures/dup_image.png

In this case, the breakend of position 25 and 21 are connecting to produce "Tandem Duplication" breakpoint (middle and bottom).

.. image:: ../_static/sv_position_figures/dup_vcf.png

.. image:: ../_static/sv_position_figures/dup_viola.png

.. image:: ../_static/sv_position_figures/dup_bedpe.png

Corresponding VCF, ``positions`` table, and BEDPE format are shown above.


-----------------------------
Inversion
-----------------------------

Regarding to the VCF, "Inversion" is the most confusing thing, since all SV callers output with different conventions!

.. image:: ../_static/sv_position_figures/inv_image.png

This is the "Inversion" events we'll explain in depth below. There are two breakpoints in this figure.

.. image:: ../_static/sv_position_figures/inv_vcf.png

This is the VCF records for each SV caller.
Gridss employs breakend-based notation here, too. 
Manta originally outputs breakend-based records of “Inversion", but these can be converted to breakpoint-based VCFs by using scripts coded by Manta's developers.
Manta outputs the start position as 20 and the end position as 25, regardless of the "Inversion" strand; Lumpy is similar, but the output is on one line. In contrast, Delly adds 1 to the start and end positions for negative strands.

.. image:: ../_static/sv_position_figures/inv_viola.png

On the viola, in "Inversion", we were keen to express the SV position on a break-end basis.
With regard to Lumpy, we have divided "Inversion" into two lines to fit our principles.

.. image:: ../_static/sv_position_figures/inv_bedpe.png

For BEDPE output, the same method as for "Deletion" is also used here.

--------------------
Translocation
--------------------

.. image:: ../_static/sv_position_figures/tra_image.png

|
In the SV callers supported by Viola (Manta, Delly, Lumpy, and Gridss), translocation is recorded in almost the same way, although Delly outputs only one row for one SV event while the others report two lines for one SV event (See figure below).

.. image:: ../_static/sv_position_figures/tra_vcf.png

|
Below is the ``positions`` table and BEDPE output that correspond to the above VCF. Viola interprets the ``ALT`` field (in this case, ``A[chr2:15[``) into ``+`` or ``-`` symbols to represent the orientations of each breakend.

.. image:: ../_static/sv_position_figures/tra_viola.png

.. image:: ../_static/sv_position_figures/tra_bedpe.png

--------------------
Single Breakends
--------------------

Some breakends do not have mate breakends and are called "single breakends".

.. image:: ../_static/sv_position_figures/bnd_image.png

|
According to the specification of VCFv4.2, single breakends are expressed as following figure.

.. image:: ../_static/sv_position_figures/bnd_vcf.png

|
Viola only use ``chrom1``, ``pos1``, and ``strand1`` entries to define a single breakend event and fill "None" or "NaN" values at ``chrom2``, ``pos2``, and ``strand2`` entries that are not necessary.

.. image:: ../_static/sv_position_figures/bnd_viola.png

|
In the BEDPE file created by Viola, this event will be output as the figure below.

.. image:: ../_static/sv_position_figures/bnd_bedpe.png

|
The ``chrom2``, ``start2``, ``end2``, and ``strand2`` entries will be blank to keep compatibility with other tools.

.. note::
    The single breakends can be defined as the manual SV classification using :doc:`viola.Vcf.breakend2breakpoint<../reference/api/viola.Vcf.breakend2breakpoint>` function. This function converts breakend-based SV records into breakpoint-based ones and infers the SV type at the same time. If the BND SVs do not have mate BND, the inferred SV type remains “BND”, while the BND SVs with mate BND can be interpreted as either deletion, duplication, inversion, insertion, or translocation. As a result, the single breakends can be differentiated against other SV types by the infefred SV type.