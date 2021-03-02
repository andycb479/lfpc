package Labs.Lab2;

import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

class Value {
    public String Terminal;
    public String NonTerminal;

    public Value(String terminal, String nonTerminal) {
        Terminal = terminal;
        NonTerminal = nonTerminal;
    }

    public Value(String terminal) {
        Terminal = terminal;
        NonTerminal = "$";
    }
}

//Variant 26
//        AF=(Q, , , q0, F),
//        Q = { q0, q1, q2 , q3},
//         = { a, b, c }, F = { q3}.
//         (q0, a ) = q1 ,
//         (q1, b ) = q1 ,
//         (q1, a ) = q2,
//         (q0, a ) = q0,
//         (q2, c) = q3,
//         (q3, c) = q3

class Main {
    public static void main(String[] args) throws IOException {

        String regularGrammar = "VN={S, B, C}, VT={a, b, c},\n" +
                //q0 = S, q1 = A, q2 = B, q3 = C;
                "P={\n" +
                "1. S-aA\n"+
                "1. S-aS\n"+
                "1. A-aB\n"+
                "1. A-bA\n"+
                "1. B-cC\n"+
                "1. C-cC\n";

        Map<String, ArrayList<Value>> hmap = grammarToHash(regularGrammar);
        Map<String, ArrayList<Value>> newHmap = new HashMap<>();
        String[] terminals = getTerminals(regularGrammar);
        String start = "S", finish = "C";

        addState(hmap,newHmap,terminals,start);
        checkFinalState(newHmap,finish);
        createGUI(newHmap);

        String input = "abaccc";
        String NonTerminal = start;
        for (int i = 0; i < input.length(); i++) {
            NonTerminal = ParseValue(NonTerminal, input.charAt(i), newHmap);
            if (NonTerminal == "$" && (input.length() - 1) - i != 0) {
                NonTerminal = null;
                break;
            }
        }
        if (NonTerminal == null || (!NonTerminal.equals("$") && !NonTerminal.contains(finish))){
            System.out.println("Rejected");
        } else{
            System.out.println("Accepted");
        }

    }

    private static void addState(Map<String, ArrayList<Value>> hmap, Map<String, ArrayList<Value>> newHmap, String[] terminals,String state) {

        for(String terminalKey: terminals){
            String newState = getTransitionState(hmap,state,terminalKey);
            if(newState.equals("")) continue;

            if(newHmap.containsKey(state)){
                newHmap.get(state).add(new Value(terminalKey , newState));
            }
            else{
                ArrayList<Value> temp = new ArrayList<>();
                temp.add(new Value(terminalKey,newState));
                newHmap.put(state,temp);
            }

            if(!newHmap.containsKey(newState)){
                addState(hmap,newHmap,terminals,newState);
            }
        }
    }

    private static String getTransitionState(Map<String, ArrayList<Value>> hmap, String input, String terminal) {

        char[] nonTerminals = input.toCharArray();
        ArrayList<String> set = new ArrayList<>();
        String out = "";

        for(char nonTerminal: nonTerminals){
            for(Value value: hmap.get(nonTerminal+"")){
                if(value.Terminal.equals(terminal) && !set.contains(value.NonTerminal)) {
                    set.add(value.NonTerminal);
                }
            }
        }
        Collections.sort(set);
        out = String.join("", set);
        return out;

    }

    private static void checkFinalState(Map<String, ArrayList<Value>> hmap, String finalState) {

        String[] temp = hmap.keySet().toArray(new String[hmap.keySet().size()]);

        for (int i = 0; i < temp.length ; i++) {
            if(temp[i].contains(finalState) || temp[i].equals(finalState)){
                hmap.get(temp[i]).add(new Value("$","$"));
            }
        }

    }

    private static String[] getTerminals(String input) {
        String terminal = input.substring(input.indexOf("VT={"));
        terminal=terminal.substring(0,terminal.indexOf("}"));
        String[] out = terminal.substring(4).replace(" ","").split(",");
        return out;
    }

    static  Map<String, ArrayList<Value>> grammarToHash(String input) {
        Map<String, ArrayList<Value>> hmap = new LinkedHashMap<>();
        int pos = input.indexOf("P");
        String[] productions = input.substring(pos).split("\\.");
        for (int i = 1; i < productions.length; i++) {
            productions[i] = productions[i].replaceAll("\\s|[0-9]|\\{|}", "");

            if(productions[i].length()>6){
                hmap.get(productions[i].charAt(0) + "").add(new Value("$", "$"));
            }
            else{
                if (hmap.containsKey(productions[i].charAt(0) + "")) {
                    hmap.get(productions[i].charAt(0) + "").add(new Value(productions[i].charAt(2) + "", productions[i].length() == 4 ? productions[i].charAt(3) + "" : "$"));
                } else {
                    ArrayList<Value> temp = new ArrayList<>();
                    temp.add(new Value(productions[i].charAt(2) + "", productions[i].length() == 4 ? productions[i].charAt(3) + "" : "$"));
                    hmap.put(productions[i].charAt(0) + "", temp);
                }
            }
        }

        return hmap;
    }

    static void createGUI(Map<String, ArrayList<Value>> hmap) throws IOException {

        FileWriter myWriter = new FileWriter("graph.dot");

        String graph = "digraph finite_state_machine {\n" +
                "    rankdir=LR;\n" +
                "    size=\"8,5\"\n" +
                "    node [shape = circle];\n";

        for (String key : hmap.keySet()) {
            for (Value value : hmap.get(key)) {
                if(value.NonTerminal.equals("$") && value.Terminal.equals("$")){
                    graph+= key+ " [shape=doublecircle];\n";
                }
                else{
                    graph += key + " -> " + (value.NonTerminal.equals("$") ? "Empty" : value.NonTerminal) + "[ label = \"" + value.Terminal + "\" ];\n";
                }
            }
        }
        graph += "}";
        myWriter.write(graph);
        myWriter.close();

    }

    static String ParseValue(String NonTerminal, char terminal, Map<String, ArrayList<Value>> hmap) {
        if (NonTerminal == null) {
            return null;
        }
        for (Value value : hmap.get(NonTerminal)) {
            if (value.Terminal.charAt(0) == terminal) {
                return value.NonTerminal;
            }
        }
        return null;
    }

}





