# Generating the severity dataset

The severity dataset contains JIRA issues from open-source projects such as ActiveMq, Log4j, Spring JPA and Spring REST.

The dataset for predicting the severity level of an issue can be generated using the following command
`./createDataset.sh`
and the result will be stored in the `severityDataset.csv` file. The script uses the issues available at 
`resources/issues` and retrieves only the title and the severity level of an issue, all while maintaining a balanced data set.

## The components of the dataset

The distribution of the issues, in terms of their severity, is the following:

| Severity Level | Number of issues |
| -------------- | ---------------- |
| Trivial | 110 |
| Minor | 286 |
| Major | 240 |
| Critical | 415 |
| Blocker | 209 |

If the severity levels were to be mapped as follows:
<pre>
    Trivial, Minor, Major -> non-severe
    Critical, Blocker -> severe
</pre>
then the distribution will be the following:

| Severity Level | Number of issues |
| -------------- | ---------------- |
| non-severe | 636 |
| severe | 624 |

thus giving a more balanced data set which will generate a better model for predicting the severity level of a new entry.