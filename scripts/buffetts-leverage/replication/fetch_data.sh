#!/bin/sh
# Downloads every raw input used by the replication into data/raw/.
# Generic User-Agent only; one request per second.
set -e
cd "$(dirname "$0")/data/raw"
UA="Mozilla/5.0"
for f in Betting-Against-Beta-Equity-Factors-Monthly Quality-Minus-Junk-Factors-Monthly; do
  curl -sL -A "$UA" -o "$f.xlsx" "https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/$f.xlsx"; sleep 1
done
for f in F-F_Research_Data_Factors F-F_Momentum_Factor; do
  curl -sL -A "$UA" -o "${f}_CSV.zip" "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/${f}_CSV.zip"; sleep 1
  unzip -o -q "${f}_CSV.zip"
done
P2=$(date +%s)
for t in BRK-A BRK-B; do
  curl -s -A "$UA" -o "yahoo_${t}_1d.json" "https://query1.finance.yahoo.com/v8/finance/chart/$t?period1=0&period2=$P2&interval=1d"; sleep 1
done
