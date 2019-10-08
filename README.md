# mwdsbe

[![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/download/releases/3.6.0/)
![t](https://img.shields.io/badge/status-stable-green.svg)
[![](https://img.shields.io/github/license/PhiladelphiaController/mwdsbe.svg)](https://github.com/PhiladelphiaController/mwdsbe/blob/master/LICENSE)

A Python toolkit for data related to minority, women, and disabled-owned (M/W/DS) businesses in Philadelphia.
The toolkit has two main use cases:

1. Formatting and geocoding the business data provided by the Office of Economic Opportunity, which
   is available for download at: https://phila.mwdsbe.com
1. Matching M/W/DS businesses from the registry to other City-related datasets, using "fuzzy" matching.

## Example

To load the formatted registry of M/W/

```python
>>> import mwdsbe

>>> registry = mwdsbe.load_registry()
>>> registry.head()
                           company_name    dba_name owner_first  ...        lat        lng                                      geometry
registry_id                                                      ...
0                119 Degrees Architects         NaN      Rafael  ...  39.964275 -75.163042  POINT (-75.16304190105227 39.96427495800303)
1                         12Bravo Group         NaN     JEFFREY  ...        NaN        NaN                                           NaN
2            1st Choice Financial Group    ProVisio    Kathrina  ...        NaN        NaN                                           NaN
3                     212 Harakawa Inc.  Two Twelve         Ann  ...        NaN        NaN                                           NaN
4                   215 Media Solutions         NaN      Dewain  ...        NaN        NaN                                           NaN

[5 rows x 20 columns]
```
