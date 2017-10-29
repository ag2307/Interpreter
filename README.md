# Interpreter
Build on python :blush:
* ### Version Summary:
  - **`ver0`** - Complete   (Sample running code in folder)
  - **`ver1`** - Complete   (Sample running code in folder)
  - **`ver2`** - Complete   (Sample running code in folder)
  - **`ver3`** - Incomplete (Sample code in folder)
  
* This interpreter is based on Python Object Oriented Programming and uses autolinking of objects to their functions (saying in lame terms). All the **`__init__`** methods and **`build`** methods are used to parse the blocks of code sequentially.
  The **`eval`** method in the above interpreter works similar to python **`eval`** method and evaluates the parsed tree/structure of the code.
* Basic **toy language** which is parsed and interpreted using **python** is as follows:
```
  n:=2;
  a:=n*2+1;
  while n>0 do
  	while a>0 do
  		print("yo ",a);
  		a:=a-1;
  	done;
  	n:=n-1;
  done;
  if a==0 then
  	print("Machaya");
  else
  	print("Kuch nhi machaya");
  fi;
```
  * Each assignment statement should use `:=` for assignment and contains `;` for termination.
  * If-Else Statement:
    - **`Condition`** in between **`if`** and **`then`**
    - Statements in between **`then`** and **`fi`**
    - **`fi`** should be followed by a **`;`**
  * While Statement:
    - **`Condition`** in between **`while`** and **`do`**
    - Statements in between **`do`** and **`done`**
    - **`done`** should be followed by a **`;`**
  * Print Statement:
    - Works same as **`python`** print statement and can print multiple arguments at once.
  * Println Statement:
    - **`println`** statement can be used to print a new line character just like **Java**
    
* Good Tutorials :bookmark::
  - [Almost same toy language but different code structure](http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1)
  - [Brilliantly explained blog](https://ruslanspivak.com/lsbasi-part1/)
