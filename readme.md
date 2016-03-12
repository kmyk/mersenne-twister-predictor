# Mersenne Twister Predictor

Predict MT19937 PRNG, from preceding 624 generated numbers.

## usage

``` sh
    $ cat foo | tail $[624 * 4] | ./predict.py > bar
```

## reference

thanks to

-   <http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/mt.html>
-   <http://homepage1.nifty.com/herumi/diary/1505.html#18>
-   <http://d.hatena.ne.jp/oupo/20141016/>
