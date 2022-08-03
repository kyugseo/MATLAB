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
 
## 3. Control Flow
 
 * if statement
 * while loop

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

```
import java.util.Scanner;
public class main {

    public static void main(String[] args) {
        Scanner input =  new Scanner(System.in);
        boolean isOnRepeat  = true;
        while (isOnRepeat){
            System.out.println("Playing current song");
            System.out.println("Would you like to off the repeat? If so, answer yes");
            String userInput = input.next();

            if (userInput.equals("yes")){
                isOnRepeat = false;
            }
        }
        System.out.println("Playing next song");
    }

}

```

### Creating multiple choice questions:
```

import java.util.Scanner;
public class main {

    public static void main(String[] args) {
        String question = "How is the weather today?";
        String choiceOne = "Sunny";
        String choiceTwo = "Rainy";
        String choiceThree = "Cloudy";
        String correctAnswer = choiceTwo;

        System.out.println(question);// write a print statement asking the question:
        System.out.println(choiceOne+"\n"+choiceTwo+"\n"+choiceThree);// write a print statement giving  the answer option

        Scanner input =  new Scanner(System.in); // Have the user input
        String userInput = input.next(); // Retrieve the user's input

        if (correctAnswer.equals(userInput)) // If the user's input matchs to correct Answer,
        {
            System.out.println("Congratulation! Your answer is correct.");// Then user is correct, and we want to print out congrats message to the user.
        }
        else // If the user's input does not match to the correct answer,
        {
            System.out.println("The answer is wrong. The correct answer is "+correctAnswer);// Then the user is incorrect, and we want to print out user is incorrect.
        }

    }
}

```
## 4. Debugging in Java

* Syntax error:
  A syntax error occurs when a programmer writes an incorrect line of code.
* Logic error?
  A logic error is a bug in a program that causes it to operate incorrectly, but not to terminate abnormally.
* Breakpoint:
  A breakpoint is an intentional stopping point put into a program for debugging purposes


## 5. Function
