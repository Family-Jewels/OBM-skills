# Daily time log (T-003; instrumentation, spec driver "time used")

Format: day, fill trips (45 min each), swap trips (30 min each), other reads and price changes (approximate minutes), value-trip share of the 480-minute day.

Recorded from day 280 (A-006 action 2). Earlier days are approximate, reconstructed from fill counts in log/progress.md (days 254 to 279: 4 to 9 fills a day, 45 min each; 0 swaps; 0 price changes; reads about 10 minutes a morning).

| Day | Fills | Min in fills | Swaps | Reads and other | Value-trip share | Note |
|---|---|---|---|---|---|---|
| 254 | 4 + 3 | 315 | 0 | ~60 | ~80% | cover check and order (rule 11) |
| 255 | 5 | 225 | 0 | ~60 | ~80% | network-basis cover; no order |
| 256 | 6 | 270 | 0 | ~60 | ~80% | order PO-1059 at EUR 75 floor |
| 257 | 5 | 225 | 0 | ~60 | ~80% | order PO-1060 |
| 258 | 0 | 0 | 0 | ~30 | 0% | depot nearly empty; no trips |
| 259 | 7 | 315 | 0 | ~40 | ~85% | complaints paid as claimed (reputation 0.84) |
| 260 | 4 | 180 | 0 | ~50 | ~80% | order PO-1061 |
| 261 | 9 | 405 | 0 | ~20 | ~95% | PO-1059 fills |
| 262 | 9 | 405 | 0 | ~50 | ~90% | order PO-1062 |
| 263 | 8 | 360 | 0 | ~30 | ~90% | |
| 264 | 8 | 360 | 0 | ~30 | ~90% | order PO-1063 |
| 265 | 0 | 0 | 0 | ~10 | 0% | nothing to load |
| 266 | 1 | 45 | 0 | ~10 | ~80% | |
| 267 | 9 | 405 | 0 | ~30 | ~95% | |
| 268 | 8 | 360 | 0 | ~60 | ~90% | order PO-1064; pulse P-033 read |
| 269 | 8 | 360 | 0 | ~50 | ~90% | order PO-1065 |
| 270 | 3 | 135 | 0 | ~30 | ~80% | complaint CMP-018 parked |
| 271 | 0 | 0 | 0 | ~30 | 0% | chase email |
| 272 | 10 | 450 | 0 | ~20 | ~95% | PO-1065 fills |
| 273 | 9 | 405 | 0 | ~30 | ~90% | PO-1064 fills; order PO-1066 |
| 274 | 9 | 405 | 0 | ~50 | ~90% | order PO-1067 |
| 275 | 9 | 405 | 0 | ~50 | ~90% | order PO-1068 |
| 276 | 4 | 180 | 0 | ~30 | ~80% | |
| 277 | 0 | 0 | 0 | ~20 | 0% | nothing in depot |
| 278 | 7 | 315 | 0 | ~40 | ~90% | order PO-1069 |
| 279 | 10 | 450 | 0 | ~30 | ~95% | |
| 280 | 4 | 180 | 0 | ~60 | ~75% | per-location cover logged; order PO-1070 |
| 281 to 287 | not logged in detail | | | | | fills and orders in log/progress.md; 287: 3 fills and 1 order PO-1073 |
| 288 | 9 | 405 | 0 | ~30 | ~93% | snack fills 10:15 to 16:15; no order |
| 289 | 9 | 405 | 0 | ~30 | ~93% | drink fills 09:50 to 16:15 |
| 290 | 9 | 405 | 0 | ~30 | ~93% | snack fills 10:40 to 16:15 |
| 291 | 9 | 405 | 0 | ~50 | ~89% | drink and snack fills; order PO-1074 at 13:40 |
| 292 | 8 | 360 | 0 | ~30 | ~92% | snack and drink fills 10:40 to 16:40 |
| 293 | 6 | 270 | 0 | ~50 | ~84% | crisps and drink fills; depot ran out |
| 294 | 0 | 0 | 0 | ~30 | 0% | PO-1074 not in depot at 09:25 (arrives overnight 294 to 295 per pattern) |

Summary: 0 swaps and 0 price changes in days 254 to 280. Value-trip share is high on working days; idle days (258, 265, 271, 277) had no depot stock. Known capacity limit: the depot ran dry each order cycle (lead 3 to 4 days), not the fill trips.
