#!/bin/sh

resultFile="severityDataset.csv"

# extract the summary and the severity level
python filterColumns.py ../../issues/activeMq.csv activeMq.csv
python filterColumns.py ../../issues/log4j.csv log4j.csv
python filterColumns.py ../../issues/springJpa.csv springJpa.csv
python filterColumns.py ../../issues/springRest.csv springRest.csv
python filterColumns.py ../../issues/maven.csv maven.csv

# copy data from the issues files

# copy the header
head -n 1 < "log4j.csv" > $resultFile

# shellcheck disable=SC2129
grep "Major" < "log4j.csv" | head -n 170 >> $resultFile
# shellcheck disable=SC2129
grep -v "Major" < "log4j.csv" | tail -n +2 >> $resultFile

grep "Major" < "springRest.csv" | head -n 70 >> $resultFile
grep -v "Major" < "springRest.csv" | tail -n +2 >> $resultFile

# grep "Critical" < "activeMq.csv" | head -n 150 >> $resultFile
grep "Critical" < "activeMq.csv" >> $resultFile
grep -v "Critical" < "activeMq.csv" | tail -n +2 >> $resultFile

tail -n +2 < "springJpa.csv" >> $resultFile

grep "Blocker" < "maven.csv" | head -n 25 >> $resultFile

# remove project specific words
sed "s/\(log4j-to-slf4j\)\|\(log4j\)\|\(slf4j\)\|%.\|\(spring\)\|\(@\)\|\(activeMq\)\|\(jpa\)\|\(active mq\)\|\(maven\)\|\(mvn\)//gi" < $resultFile > "temp.csv"
mv "temp.csv" $resultFile

# clean up
rm log4j.csv activeMq.csv springRest.csv springJpa.csv maven.csv
