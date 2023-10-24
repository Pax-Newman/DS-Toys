# Topic Clustering

An unsupervised clustering algorithm for clustering text documents by pre-defined topics. 

![](https://raw.githubusercontent.com/sebischair/Lbl2Vec/main/images/Document_assignment_example.png)


## Usage

```
python main.py topic_distance data/mydocs.csv 'MyColumnName' 'all-MiniLM-L6-v2' classified_docs.csv
                Clustering     Input data       Target col     sentence trans-    output filepath
                  method        filepath          in csv        former model

cont.
--topic basketball:Basketball,NBA,LeBron --topic soccer:Soccer,Messi,FIFA
        topic name:keywords.....         add as many topics and keywords as you want!
```

## Credits

 - [Lbl2Vec](https://github.com/sebischair/Lbl2Vec) for creating the original algorithm
