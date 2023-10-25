# Topic Clustering

An unsupervised clustering algorithm for clustering text documents by pre-defined topics. 

![](https://raw.githubusercontent.com/sebischair/Lbl2Vec/main/images/Document_assignment_example.png)

## Installation

```bash
python -m pip install 'git+https://github.com/Pax-Newman/DS-Toys.git#egg=Topic%20Clustering&subdirectory=Topic%20Clustering'
```


## Usage

```
topic_cluster topic_distance data/mydocs.csv 'MyColumnName' 'all-MiniLM-L6-v2' classified_docs.csv
  root cmd      Clustering     Input data      Target col     sentence trans-    output filepath
                  method        filepath         in csv        former model

args cont.
--topic basketball:Basketball,NBA,LeBron --topic soccer:Soccer,Messi,FIFA
        topic name:keywords.....         add as many topics and keywords as you want!
```

## Credits

 - [Lbl2Vec](https://github.com/sebischair/Lbl2Vec) for creating the original algorithm
