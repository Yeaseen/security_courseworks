## Compile the java code that uses Soot APIs

```bash
javac -cp sootclasses_j9-trunk-jar-with-dependencies.jar:. analyzer/SimpleAPILookupTransformer.java
```

##

javac -cp sootclasses_j9-trunk-jar-with-dependencies.jar:. analyzer/AnalysisMain.java

java -cp sootclasses_j9-trunk-jar-with-dependencies.jar:android-17.jar:. analyzer.AnalysisMain ./unknown
