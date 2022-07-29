# Learning Java

This contains the foundation of Java programming languages.

## 1. Getting started with Java

### What is Java? 
Java is a set of computer software that provides a system for developing application software and deploying it in a cross-platform computing environment. 
+[For more information](https://en.wikipedia.org/wiki/Java_(software_platform)) 


### What we need to use Java?
 - downloading Java on to the computer (Java development kit)
 - exploring command line 

    |   Description | Window      | Mac     | Linux     |
    | ------------- | ------------- | -------- |-------- |
    | Directory listing|dir |ls |ls-l|
    | Rename a file| ren| mv |mv|
    |Change the current directory|cd|cd|cd|
    |Copying a file|copy|cp -R|cp|
    |To create a new directory/folder|md|mkdir|mkdir|
    
  - exploring IDE (intergrated development environment)
 
 ## 2. Foundtation of Java
 
 ### Primitive data type
  *  boolean : true / false
  *  int : integer
  *  double : floating-point numbers
  *  char : single letter or symbol


```
public class main {

    public static void main(String[] args) {
        int studentAge = 15;
        double studentGPA = 3.45;
        boolean hasPerfectAttandance = true;
        char studentFirstInitial = 'K';
        char studentLastInitial = 'M';
        System.out.println("student's GPA is " +studentGPA+"and she/he is " +studentAge+" years old.")
```
 
 ### String in Java
  String is reference data type.
 * index of strings:   Java String class charAt() method returns a char value at the given index number. The index number starts from 0 to n-1. and n is the length of the string. 

### Input and output in Java 
1. Import java.util.Scanner;
2. write the code for asking user that you want to get? (for example, System.out.println("what do you want to update it to?");)
3. Store the input value in the the new variable  (for example, Scanner input =  new Scanner(System.in);)
4. Update the new data to the old data if needed (for example, studentGPA = input.nextDouble();)

```
import java.util.Scanner;
 public class main {

    public static void main(String[] args) {
        int studentAge = 15;
        double studentGPA = 3.45;
        boolean hasPerfectAttandance = true;
        String studnetfirstName = "Kyungseo";
        String studentlastName = "Moon";
        char studentFirstInitial = studnetfirstName.charAt(0);
        char studentLastInitial = studentlastName.charAt(0);


        System.out.println(studnetfirstName +" " +studentlastName+" has a GPA of "+studentGPA);
        System.out.println("what do you want to update it to?");
        Scanner input =  new Scanner(System.in);
        studentGPA = input.nextDouble();
        System.out.print(studnetfirstName +" "+ studentlastName +
                " now has a GPA of "+studentGPA);
    }
 }
  
 ```
 
 ## Control Flow

```
import java.util.Scanner;
public class main {

    public static void main(String[] args) {
        System.out.println("Pick a number between 1 and 10");
        Scanner input =  new Scanner(System.in);
        int inputtedNum = input.nextInt();
        if (inputtedNum < 5){
            System.out.println("Enjoy the good luck a friend brings you!");
        } else {
            System.out.println(" Your shoe selection will make you happy today!");
        }
    }
}
```
