# ADL Piano MIDI 

The ADL Piano MIDI is a dataset of 11,086 piano pieces from different genres. This dataset is based on the [Lakh MIDI dataset](https://colinraffel.com/projects/lmd/), which is a collection on 45,129 unique MIDI files that have been matched 
to entries in  the [Million Song Dataset](http://millionsongdataset.com/). Most pieces in the Lakh MIDI dataset have multiple 
instruments, so for each file we extracted only the tracks with instruments from the "Piano Family" (MIDI program numbers 1-8). 
This process generated a total of 9,021 unique piano MIDI files. Theses 9,021 files were them combined with other 
approximately 2,065 files scraped from publicly-available sources on the internet. All the files in the final collection were 
de-duped according to their MD5 checksum. 

We plan to keep adding piano pieces to this dataset.

## Citing this Dataset

This dataset was presented in [this paper](https://arxiv.org/abs/2008.07009), so if you use it, please cite:

```
@article{ferreira_aiide_2020,
  title={Computer-Generated Music for Tabletop Role-Playing Games},
  author={Ferreira, Lucas N and Lelis, Levi HS and Whitehead, Jim},
  booktitle = {Proceedings of the 16th AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment},
  series = {AIIDE'20},
  year={2020},
}
