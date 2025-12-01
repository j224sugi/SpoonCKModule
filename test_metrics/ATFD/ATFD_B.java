
public class ATFD_B extends ATFD_D {

    ATFD_A aInstance = new ATFD_A();
    int b = 0;

    public ATFD_B() {
        super();
    }

    @Override
    public void superMethod() {
        System.out.println(b);
        super.superMethod();
    }//ATLD=1   LAA=1

    public int getMethod() {
        return aInstance.getField();
    }//ATFD=1   LAA=0   FDP=1

    public int getDirectField() {
        return aInstance.field1;
    }//ATFD=1   LAA=0   FDP=1

    public void variousPattern() {
        aInstance.field1 = aInstance.field2;
        System.out.println();
        System.out.println(Math.PI);
        System.out.println(aInstance.field2);
        thisChange(aInstance);
        System.out.println(ATFD_A.aaa);
        System.out.println(aInstance.c.ca);
        System.out.println(aInstance.c.getInt());
        System.out.println(b);
        System.out.println(this.b);
        System.out.println(getThisClassInt());
    }//ATLD=4,ATFD=7    LAA=0.36363 FDP=3(A,Math,C)

    public void thisChange(ATFD_A change) {
        this.aInstance = change;
    }//ATLD=1   LAA=1

    public int getThisClassInt() {
        return this.b;
    }//ATLD=1     LAA=1

    public void setAField(ATFD_A change) {
        change.setPrivateField(19);
    }//ATFD=1   LAA=0   FDP=1
}//ATLD=7,ATFD=10   //LAA=0.4117    FDP=3
