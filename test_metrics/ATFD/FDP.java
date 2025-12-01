
class FDP {

    ATFD_A a = new ATFD_A();
    ATFD_B b = new ATFD_B();
    ATFD_C c = new ATFD_C(10);
    ATFD_D d = new ATFD_D();

    public void getFDP(){
        a.getField();
        System.out.println(a.field1);
        b.getThisClassInt();
        b.getThisClassInt();
        b.getDirectField();
        c.getInt();
    }//ATFD=6 ATLD=0 FDP=3

    public void getFDP2(){
        c.getInt();
        d.getData();
    }//ATFD=2 ATLD=0 FDP=2
}//ATFD=8 FDP=4
