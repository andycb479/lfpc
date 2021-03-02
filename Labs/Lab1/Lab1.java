package Labs.Lab1;

//Variant 26.
//        VN={S, A, B, C}, VT={a, b, c, d},
//        P={
//        1. S-dA
//        2. A-aB
//        3. B-bC
//        4. C-cB
//        5. B-d
//        6. C-aA
//        7. A-b }

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

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


class Lab1 {
    public static void main(String[] args) throws IOException {

        String regularGrammar = "VN={S, A, B, C}, VT={a, b, c, d},\n" +
                "P={\n" +
                "1. S-dA\n" +
                "2. A-aB\n" +
                "3. B-bC\n" +
                "4. C-cB\n" +
                "5. B-d\n" +
                "6. C-aA\n" +
                "7. A-b }";
        Map<String, ArrayList<Value>> hmap = grammarToHash(regularGrammar);

        createGUI(hmap);

        String input = "dabcd";//dabcd,dabaad,dabaabcd
        String NonTerminal = "S";

        for (int i = 0; i < input.length(); i++) {
            NonTerminal = ParseValue(NonTerminal, input.charAt(i), hmap);
            if (NonTerminal == "$" && (input.length() - 1) - i != 0) {
                NonTerminal = null;
                break;
            }
        }
        if (NonTerminal == null || !NonTerminal.equals("$")) {
            System.out.println("Rejected");
        } else {
            System.out.println("Accepted");
        }
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


    static  Map<String, ArrayList<Value>> grammarToHash(String input) {

        Map<String, ArrayList<Value>> hmap = new HashMap<>();
        int pos = input.indexOf("P");
        String[] productions = input.substring(pos).split("\\.");
        for (int i = 1; i < productions.length; i++) {
            productions[i] = productions[i].replaceAll("\\s|[0-9]|\\{|}", "");

            if (hmap.containsKey(productions[i].charAt(0) + "")) {
                hmap.get(productions[i].charAt(0) + "").add(new Value(productions[i].charAt(2) + "", productions[i].length() == 4 ? productions[i].charAt(3) + "" : "$"));
            } else {
                ArrayList<Value> temp = new ArrayList<>();
                temp.add(new Value(productions[i].charAt(2) + "", productions[i].length() == 4 ? productions[i].charAt(3) + "" : "$"));
                hmap.put(productions[i].charAt(0) + "", temp);
            }

        }

        return hmap;
    }

    static void createGUI(Map<String, ArrayList<Value>> hmap) throws IOException {

        FileWriter myWriter = new FileWriter("graph.dot");

        String graph = "digraph finite_state_machine {\n" +
                "    rankdir=LR;\n" +
                "    size=\"8,5\"\n" +
                "    node [shape = circle];\n"+
                "    Empty [shape=doublecircle];\n";

        for (String key : hmap.keySet()) {
            for (Value value : hmap.get(key)) {
                graph += key + " -> " + (value.NonTerminal.equals("$") ? "Empty" : value.NonTerminal) + "[ label = \"" + value.Terminal + "\" ];\n";
            }
        }
        graph += "}";
        myWriter.write(graph);
        myWriter.close();

    }
}
