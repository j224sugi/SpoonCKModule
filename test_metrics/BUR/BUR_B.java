
class BUR_B extends BUR_A {

    protected int ba = 30;
    protected static int staticNum = 100;

    protected int moreCalculate() {
        return calculate(a) * ba;
    }

    public void doAnything() {
        calculate(a);
    }

}//Aのprotected数→３
//Aのaとcalculateを使用→0.667
