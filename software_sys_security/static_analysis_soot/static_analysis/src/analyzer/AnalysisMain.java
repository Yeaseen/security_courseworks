package analyzer;

import java.io.*;
import java.util.*;

import soot.*;

public class AnalysisMain{

	public static String CLASSPATH;
	public static String OUTPUT;

	public static void main(String[] args){
		
		String arg1 = args[0];
		System.out.println("argument 0===> "+arg1);
		CLASSPATH = arg1 + "/";
		System.out.println("initial CLASSPATH===> "+CLASSPATH);
		String filename = arg1.substring(arg1.lastIndexOf('/')+1);
		OUTPUT = "output" + "_" + filename;
				
		File directory = new File(".");
		String pwd = "";
		try{
			pwd = directory.getAbsolutePath();
		}catch(Exception e){
			System.out.println(e.getMessage());
			System.err.println("java -cp sootclass_xx.jar:android-xx.jar:. lab2.AnalysisMain processed_file_dir");
			System.exit(-1);
		}
		
		System.out.println("Processing class " + filename + " under " + CLASSPATH + ", output directory:" + OUTPUT);
		
		AnalysisMain analysis = new AnalysisMain();
		analysis.run();
		
	}


	private void run(){
		
		simpleAPILookup();
	}

	public void simpleAPILookup() {

		System.out.println("looking up APIs...");

		SimpleAPILookupTransformer simpleAPILookupTransformer = new SimpleAPILookupTransformer();
		Transform transform = new Transform("jtp.SimpleAPILookupTransformer",	simpleAPILookupTransformer);
		PackManager.v().getPack("jtp").add(transform);

		List<String> sootArgs = new ArrayList<String>();

		sootArgs.add("-output-format");
		sootArgs.add("J");

		sootArgs.add("-soot-class-path");
		sootArgs.add(CLASSPATH + ":android-17.jar");

		System.out.println("soot-class=======>"+CLASSPATH + ":android-17.jar");

		sootArgs.add("-process-dir");
		sootArgs.add(CLASSPATH);
		System.out.println("process-dir=======> "+CLASSPATH);

		sootArgs.add("-output-dir");
		sootArgs.add(OUTPUT);
		System.out.println("Output directory=======> "+OUTPUT);

		String[] soot_args = new String[sootArgs.size()];
		for (int i = 0; i < sootArgs.size(); i++) {
			soot_args[i] = sootArgs.get(i);
		}

		soot.Main.main(soot_args);

		
		LinkedHashMap<String, List<String>> methodToAPIs = simpleAPILookupTransformer.getMethodToAPIs();

		Set<String> keySet = methodToAPIs.keySet();
		Iterator<String> iter = keySet.iterator();
		while (iter.hasNext()) {
			String method = iter.next();
			List<String> apis = methodToAPIs.get(method);
			
			System.out.println(method + " calls APIs: ");
			for (String api : apis) {
				
				System.out.println(api);
			}
			System.out.println();
		}
	}
}
