
public class ATFD_A {

    public static int aaa = 0;
    ATFD_C c = new ATFD_C(10);
    int field1;
    int field2;
    private int privateField;

    public int getField() {
        return this.field1;
    }

    public int getPrivateField(int number) {
        return privateField;
    }

    public void setPrivateField(int number) {
        this.privateField = number;
    }
}//ATFD=0,ATLD=3,FDP=0
