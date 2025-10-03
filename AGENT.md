My Electrical Company is changing their billing pattern, and this project utilizes a Jupyter Notebook to calculate the difference between the two options.

## Billing Options

* Flat Rate Billing
  * Time Period: All Day
    * Summer Price / kWh
      * Dates: June 1 - Sep. 30
      * Price: $0.10380
    * Winter Price / kWh
      * Dates: Oct. 1 - May 31
      * Price: $0.08570
* Time of Use Billing
  * On Peak Time Period: 5 p.m. - 9 p.m., Monday-Friday
    * Summer Price / kWh
      * Dates: June 1 - Sep. 30
      * Price: $0.21277
    * Winter Price / kWh
      * Dates: Oct. 1 - May 31
      * Price: $0.18331
  * Off Peak Time Period: All other Times
    * Summer Price / kWh
      * Dates: June 1 - Sep. 30
      * Price: $0.21277
    * Winter Price / kWh
      * Dates: Oct. 1 - May 31
      * Price: $0.18331

## Technical Details
This project should utilize a Jupyter Notebook

A Nix Shell should setup the python environment, and utilize direnv.

`uv` should be used for managing python dependencies.