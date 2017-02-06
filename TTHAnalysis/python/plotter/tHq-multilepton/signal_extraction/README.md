# tHq signal extraction procedure

### Produce datacards:

```
python makeShapeCardsTHQ.py \
--savefile report_thq_3l.root \
tHq-multilepton/signal_extraction/mca-thq-3l-mcdata-frdata_limits.txt \
tHq-multilepton/cuts-thq-3l.txt \
thqMVA_ttv_3l:thqMVA_tt_3l 40,-1,1,40,-1,1 \
tHq-multilepton/signal_extraction/systsEnv.txt \
-P treedir/mixture_jecv6prompt_datafull_jul20/ \
-P treedir/tHq_production_Jan11/ \
--tree treeProducerSusyMultilepton \
--s2v -j 8 -l 12.9 -f \
--xp data --asimov \
-F sf/t treedir/tHq_eventvars_Jan18/evVarFriend_{cname}.root \
--Fs {P}/2_recleaner_v5_b1E2 \
--mcc ttH-multilepton/lepchoice-ttH-FO.txt \
--neg \
-o 3l \
--od tHq-multilepton/signal_extraction/cards \
-L tHq-multilepton/functionsTHQ.cc \
--2d-binning-function "10:tHq_MVAto1D_3l_10" \
-v 2
```

- Change from `--savefile report.root` to `--infile report.root` to rerun quickly with a different binning.
- Binning function in `tHq-multilepton/functionsTHQ.cc`. This turns the 2d histogram of mva1 vs mva2 into a 1d histogram for shape fitting in combine.
- Keep track of reporting of empty bins and adjust binning function accordingly.

This produces two files for each point: `..input.root` and `..card.txt`.

Note that the standard selection is hardcoded in `tHq-multilepton/makecards.sh`.

### Run the limit calculation:

You'll need to set your environment to a release area with `combine` available, e.g. like so:

```
cd ~stiegerb/combine/; cmsenv ; cd -;
```

Run on a single datacard you can use combine directly:

```
combine -M Asymptotic --run blind --rAbsAcc 0.0005 --rRelAcc 0.0005 ttH_3l.card.txt
```

or use `make_limit.sh cards/ttH_3l.card.txt` to do everything in one go.

In case of several datacards, combine them first with `combineCards.py *card.txt > combined.txt`.

Then the "Expected 50.0%" is the number to be quoted.

### Processing several Ct/CV points

Use `runAllLimits.py` to run on all the cards in one directory and produce a .csv file with the Ct/CV points, the expected limit, and the one and two sigma bands.

Use `combineChannels.py` to combine the corresponding cards for each point in a list of input directories. Typically you'd run something like this:

```
python combineAllCards.py cards_Jan31/2lss-mm/ cards_Jan31/2lss-em/ cards_Jan31/2lss-ee/ cards_Jan31/3l/ -o comb_4chan
```

This will produce combined cards in a new directory (specified with the `-o` option) and also copy the root files and original cards into it.

You can then use `runAllLimits.py` to produce the combined limits.