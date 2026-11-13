Task: T-02
Claim per criterion:
  1. parses '1h30m', '45s' : met : test_hm, test_s : python -m pytest T-02/submission -q
  2. supports d, h, m, s : met : test_days, test_mixed : same command
  3. ValueError on bad input : met : test_bad : same command
  4. tests pass : met : output below : same command

```
$ python -m pytest T-02/submission -q
......                                                                   [100%]
6 passed in 0.02s
```
Known gaps: none
Constraint breaks: none
