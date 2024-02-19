package analyzer;

import java.util.*;

import soot.*;
import soot.jimple.*;

/*
 * SimpleAPILookupTransformer extends BodyTransformer and aims to collect all the APIs called in a program.
 */
public class SimpleAPILookupTransformer extends BodyTransformer{
	
	//methodToAPIs is A HashMap to store analysis result. 
	//The key is a method's signature. The format of signature is <declaring_class: return_type method_name(parameter_type,...)>, e.g., <test.Unknown: void <init>(java.lang.String,java.lang.String)>
	//The corresponding value is a list of API signatures. These APIs are called in this method.
	private LinkedHashMap<String, List<String>> methodToAPIs = new LinkedHashMap<String, List<String>>();
	
	//Override internalTransform() which will be triggered by Soot framework to perform custom analysis for each method.
	//The first parameter is the instance of a method body. 
	protected void internalTransform(Body body, String string, Map map) {
		
		//Obtain the SootMethod instance associated with a method body
		SootMethod method = body.getMethod();
		System.out.println("Analyzing method: " + method);
		
		List<String> apis = new ArrayList<String>();	
		
		//Obtain an Iterator of the statements in the method body
		Iterator<Unit> iter = body.getUnits().iterator();
		
		//Iterate all statements and record any API invocation statement.
		while(iter.hasNext()){
			
			Stmt s = (Stmt)iter.next();
			
			//Check if current statement is an InvokeStmt
			//i.e. function call without a return value
			
				
				//Check if the declaring class is defined in the Application under analysis
				//If not, method m is an API
				
				
			//Check if current statement is a DefinitionStmt with right-handed side being an InvokeExpr
			//i.e. function call with a return value
			

				//Check if the declaring class is defined in the Application under analysis
				//If not, method m is an API
								
			
		}
		
		//Store the analysis result into the HashMap
		methodToAPIs.put(method.getSignature(), apis);
		
	}
	
	public LinkedHashMap<String, List<String>> getMethodToAPIs(){
		return this.methodToAPIs;
	}

}
