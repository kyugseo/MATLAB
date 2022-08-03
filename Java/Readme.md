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
 
 ## 2. Foundation of Java
 
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

### Defining function:
A function is a series of finite steps that accomplish some task.

### parameter in Java : 
1. find out the total meal price when the listedprice is 15, tiprate is 20 percent and the taxrate is 8 percent of the price.
2. find out the total meal price when the listedprice is 25, tiprate is 20 percent and the taxrate is 8 percent of the price.
```
public class Main {

    public static void calculateTotalMealPrice( double tipRate, double taxRate, double listedMealPrice) {
        double tip = tipRate * listedMealPrice;
        double tax = taxRate * listedMealPrice;
        double result = tip + tax + listedMealPrice;

        System.out.println("Your total is $"+result);
    }

    public static void main(String[] args) {
        calculateTotalMealPrice(0.2,0.08,15);
        calculateTotalMealPrice(0.2,0.08,25);
    }

}
```
### using return type 
similarly, calculating the total meal price, however this time is for 5 people and find out the individual price for the meal when listed price of the meal is 100, the tip is 0.2 and taxrate is 0.08 of the total.

```
public class Main {

    public static double calculateTotalMealPrice( double listedMealPrice,double tipRate, double taxRate){
        double tip = tipRate * listedMealPrice;
        double tax = taxRate * listedMealPrice;
        double result = tip + tax + listedMealPrice;
        return result;
    }

    public static void main(String[] args) {
        double groupMealPrice = calculateTotalMealPrice(100,0.2,0.08);
        System.out.println(groupMealPrice);
        
        double individualMealPrice = groupMealPrice/5 ;
        System.out.println(individualMealPrice);
    }

}
```

### using built-in function:
Example of built-in function:
 1. Math.pow 
 2. System.out.println();
 3. .equals();
```
public class Main {

    public static void main(String[] args) {
        double result = Math.pow(2,5);
        System.out.println(result);
    }

}

``` 

### function application:
Calcualte the salary.
* input 1: number of hours the employee works per week
* input 2: amount of money the employee makes per hours
* input 3: number of vacation days (1 day of vacation = 8 hours unpaid)
* output: employee's gross annual salary
! Do not need to worry about tax for this example:

```
import java.util.Scanner;
public class Main {
    public static double calculateYearlySalary(int workHourperWeek, double amountPerHour, int vacationDays){
        if (workHourperWeek<0){
            return -1;
        }
        if (amountPerHour<0) {
            return -1;
        }
        double totalYearlySalary = workHourperWeek * 52 * amountPerHour ;
        double unpaid = vacationDays * 8 * amountPerHour;
        return  totalYearlySalary -unpaid ;
    }
    public static void main(String[] args) {

        System.out.println("Type number of hours the employee works per week: ");
        Scanner input = new Scanner(System.in);
        int workHourperWeek = input.nextInt();
        System.out.println("Type amount of money the employee makes per hours: ");
        double amountPerHour = input.nextDouble();
        System.out.println("Type number of vacation days: ");
        int vacationDays = input.nextInt();

        double totalYearlySalary = calculateYearlySalary(workHourperWeek, amountPerHour,vacationDays);
        System.out.println("The employee's yearly salary is $"+totalYearlySalary);
    }

}

```

OUTPUT: 

```
Type number of hours the employee works per week: 
40
Type amount of money the employee makes per hours: 
35
Type number of vacation days: 
2
The employee's yearly salary is $72800.0
 
Process finished with exit code 0
```
