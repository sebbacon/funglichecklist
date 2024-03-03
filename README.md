# Checklist of the British & Irish Basidiomycota

This repository contains data from to the _Checklist of the British & Irish Basidiomycota_.

I believe the website version was last updated in 2020, and the website is no longer under development.

I needed personal research project: specifically, to map obselete species names to their current canonical name.

That mapping is available as [`flattened_synonyms_to_root_canonical.csv`](./flattened_synonyms_to_root_canonical.csv).


# About this repo

The data is scraped from the website at [https://basidiochecklist.science.kew.org/](https://basidiochecklist.science.kew.org/) using the `scrape.py` script; all the raw HTML is stored in the `data/` directory.

A subset of the data available on the website (for example, I've skipped _Description_ fields where available) is then turned in to JSON with the `parse.py` script. That data is available at [`checklist.json`](./checklist.json).

That JSON is processed to make the final lookup table with `postprocess.py`

# About the source data

## Original source reference
CHECKLIST OF THE BRITISH & IRISH BASIDIOMYCOTA
N.W. Legon & A. Henrici
with A.M. Ainsworth, P.J. Roberts, B.M. Spooner & R. Watling
database designed by J.A. Cooper and supported by P.M. Kirk

## License

The original website was published under a Creative Commons Attribution-Non-Commercial-Share Alike 2.0 license by the [FRDBI](http://www.frdbi.info), who must be acknowledged under any derived works.

This data is released under the same license, and all derived works must be, too.
